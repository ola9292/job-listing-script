import requests
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()
my_email = os.getenv('EMAIL_ADDRESS') or os.environ.get('EMAIL_ADDRESS')
password = os.getenv('EMAIL_PASSWORD') or os.environ.get('EMAIL_PASSWORD')
smtp_address = os.getenv('SMTP_ADDRESS') or os.environ.get('SMTP_ADDRESS')

base_url = "https://api.adzuna.com/v1/api/jobs/gb/search/1"
url="jobs/uk/search/1"
app_id="9d08cc04"
app_key="3c75abae7e650a2763b3ad5864966061"

parameters = {
    'app_id':app_id,
    'app_key':app_key,
    'what':'software developer',
    'results_per_page':10,
    'location0':'UK',
    'location1' :'South East England'
}

def getJobs():
    response = requests.get(url=base_url, params=parameters)
    data = response.json()
    return data['results']

result = getJobs()
jobs = []
jobs.append(result)

# print(jobs)

def send_email():
    message = MIMEMultipart()
    message['From'] = my_email
    message['To'] = "olamide.kazeem@yahoo.com"
    message['Subject'] = "Latest Job Listings!"

    body = "Here are the latest job listings:\n\n"
    for job in getJobs():
        body += f"Title: {job['title']}\nURL: {job['redirect_url']}\n\n"

    message.attach(MIMEText(body, 'plain'))
    
    # Send email
    connection = smtplib.SMTP(smtp_address)
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(
        from_addr=my_email, 
        to_addrs="olamide.kazeem@yahoo.com", 
        msg=message.as_string()
    )
    connection.close()
    
if jobs != []:
    send_email()