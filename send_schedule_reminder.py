import csv
import os
import logging
from datetime import datetime, date, timedelta
from send_msg import Email


# local variables
CSV_FILE = 'schedules/lectures.csv'
EMAIL_TO = os.environ.get('EMAIL_TO')
EMAIL_FROM = os.environ.get('EMAIL_FROM')

if EMAIL_TO is None :
    logging.error("EMAIL_TO not setup on Environment Variables")
    exit(1)

if EMAIL_FROM is None :
    logging.error("EMAIL_FROM not setup on Environment Variables")
    exit(1)

# date helpers
TODAY = datetime.today()
FUTURE = timedelta(days = 28)

with open(CSV_FILE, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader, None)
    msg_lines = []
    for line_date, line_who, line_msg in reader:
        date_dt = datetime.strptime(line_date, "%d/%m/%Y")
        dt_in_range = TODAY <= date_dt <= TODAY + FUTURE
        if dt_in_range:
            msg_lines.append({"date": line_date,
                              "who": line_who,
                              "msg": line_msg})


html_line = []
for line in msg_lines:
    table_line="<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                         line["date"],
                         line["who"],
                         line["msg"])
    html_line.append(table_line)
    logging.info(table_line)

html_table = "<table><tr><th>Date</th><th>Who</th><th>Description</th></tr>"
html_table = html_table + "".join(html_line) + "</table>"

msg = """Dear PTSC member, </br>
These are the tasks for the following weeks from Today: <br><br>

{}""".format(html_table)

send = Email()
send.message(EMAIL_FROM, EMAIL_TO, "PTSC Weekly task reminder", msg)

