import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

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

    if st.button("Start Monitoring"):
        driver = get_driver()
        original_content = fetch_site_content(url, driver)
        if original_content:
            st.success("Monitoring started. You will receive an email if a change is detected.")
            while True:
                time.sleep(check_interval)
                new_content = fetch_site_content(url, driver)
                if compare_content(original_content, new_content):
                    send_email(email, "Change detected on website you're tracking! :)", f"A change was detected on {url}")
                    original_content = new_content  # Update the original content to the new content after change detection
        else:
            st.error("Failed to fetch website content. Please check the URL and try again.")
        driver.quit()

if __name__ == "__main__":
    main()
