import streamlit as st
from flask import Flask, jsonify
from flask_migrate import Migrate, upgrade
from db import db, Request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

# Database set-up to track requests
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:6fGMA/AHC8!A-UH@localhost/website-tracker"

db.app = app
db.init_app(app)
migrate = Migrate(app, db)


# Function to configure and return a Selenium WebDriver
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    service = Service(executable_path=r"C:\Users\steve\Desktop\Python\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to fetch website content using Selenium
def fetch_site_content(url, driver):
    driver.get(url)
    time.sleep(5)  # Wait for the dynamic content to load
    return driver.page_source

# Function to compare content
def compare_content(old_content, new_content):
    return old_content != new_content

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

# Streamlit UI
def main():
    st.title("Track changes to any website!")
    url = st.text_input("Enter the website URL:")
    email = st.text_input("Enter your email address:")
    check_interval = st.number_input("Check interval in seconds:", min_value=30, value=60)
    start_button = st.button("Start Monitoring")

    if start_button:
        with st.empty():
            with st.spinner('Give us a second...'):
                driver = get_driver()
                original_content = fetch_site_content(url, driver)
                if original_content:
                    st.success("Monitoring started. You will receive an email if a change is detected.")

                    # Send to database
                    with app.app_context():
                        web_request = Request()
                        web_request.email = email
                        web_request.url = url
                        db.session.add(web_request)
                        db.session.commit()

                    while True:
                        time.sleep(check_interval)
                        new_content = fetch_site_content(url, driver)
                        if compare_content(original_content, new_content):
                            with app.app_context():
                                # Send mail if there are any changes
                                send_email(email, "Change detected on website you're tracking! :)", f"A change was detected on {url}")
                                original_content = new_content  # Update the original content to the new content after change detection
                else:
                    st.error("Failed to fetch website content. Please check the URL and try again.")
                driver.quit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        upgrade()

    main()