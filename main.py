import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    service = Service(executable_path=r"C:\Users\steve\Desktop\Python\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to send email
def send_email(recipient_email, subject, body):
    sender_email = "steven@semurai.se"
    sender_password = "akbmdhgbnsmtfeiq"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
            server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_website_changes(event, context):
    url = event['url']
    email = event['email']

    driver = get_driver()
    
    # Your logic to fetch and compare website content
    # If changes are detected:
    send_email(email, "Change detected on website you're tracking! :)", f"A change was detected on {url}")
    
    # Cleanup
    driver.quit()

# Note: You'll need to adapt how the `url` and `email` are passed to the function, 
# potentially using Cloud Function's event parameter or environment variables.