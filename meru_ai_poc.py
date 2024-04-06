import csv
import email
import imaplib
import os
import smtplib
import sys
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

################################################################################
############### Environment Variables & Secrets ################################

current_base_directory = os.path.dirname(
    sys.executable if getattr(sys, "frozen", False) else __file__
)
current_parent_directory = os.path.dirname(current_base_directory)

secrets_path = os.path.join(current_base_directory, "secrets.env")
load_dotenv(secrets_path)

genai_options_path = os.path.join(current_base_directory, "genai_options.csv")

email_address = os.getenv("email_address")
google_app_password = os.getenv("google_app_password")
meru_ai_gmail_label = "meru-ai-replies"

attempt_interval_in_seconds = os.getenv("attempt_interval_in_seconds")
days_interval = os.getenv("days_interval")

################################################################################
################################################################################


def meru_ai_reply_to_email(from_email, to_address, reply_subject, parsed_body):

    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_address
    message["Subject"] = "Re: " + reply_subject
    message.attach(MIMEText(parsed_body, "plain"))

    session = smtplib.SMTP("smtp.gmail.com", 587)
    session.starttls()
    session.login(from_email, google_app_password)

    text = message.as_string()

    session.sendmail(from_email, to_address, text)
    session.quit()
    print(
        "Email sent from "
        + from_email
        + "to "
        + to_address
        + "with subject: "
        + reply_subject
    )


genai_options = []

with open(genai_options_path) as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        genai_options.append(row)

print("Initiating Meru AI PoC...")

interval_in_minutes = round(int(attempt_interval_in_seconds) / 60, 1)

try:

    while True:

        gmail_host = "imap.gmail.com"
        mail = imaplib.IMAP4_SSL(gmail_host)
        mail.login(email_address, google_app_password)
        mail.select("INBOX")

        print(
            f"Meru AI is checking the inbox every "
            + str(interval_in_minutes)
            + " minutes..."
        )

        current_date = datetime.now()
        date_since = current_date - timedelta(int(days_interval))
        date_str = date_since.strftime("%d-%b-%Y")

        first_option = True

        for option in genai_options:

            if first_option == True:
                first_option = False
                continue

            fetched_data = None

            if option[0] == "1":
                result, fetched_data = mail.search(
                    None, '(SINCE "' + date_str + '" FROM "' + option[1].strip() + '")'
                )
            elif option[0] == "2":
                result, fetched_data = mail.search(
                    None,
                    '(SINCE "' + date_str + '" SUBJECT "' + option[1].strip() + '")',
                )
            elif option[0] == "3":

                email_filter = option[1].split(";")[0].strip()
                section = option[1].split(";")

                if len(section) == 2:
                    subject_filter = section[1].strip()
                elif len(section) > 2:
                    subject_filter = " ".join(section[1:]).strip()
                else:
                    raise Exception(
                        "There is an issue with the filter_type 3 values. Please ensure that you have the correct format. Remember to split the email address and subject value with the ';' symbol."
                    )

                result, fetched_data = mail.search(
                    None,
                    '(SINCE "'
                    + date_str
                    + '" FROM "'
                    + email_filter
                    + '" SUBJECT "'
                    + subject_filter
                    + '")',
                )

            if len(fetched_data[0].split()) > 0:

                if option[0] == "1":
                    print(
                        "Detected the email for this filter : "
                        + '(SINCE "'
                        + date_str
                        + '" FROM "'
                        + option[1].strip()
                        + '")'
                    )
                elif option[0] == "2":
                    print(
                        "Detected the email for this filter : "
                        + '(SINCE "'
                        + date_str
                        + '" SUBJECT "'
                        + option[1].strip()
                        + '")'
                    )
                elif option[0] == "3":
                    print(
                        "Detected the email for this filter : "
                        + '(SINCE "'
                        + date_str
                        + '" FROM "'
                        + email_filter
                        + '" SUBJECT "'
                        + subject_filter
                        + '")'
                    )

                for num in fetched_data[0].split():

                    typ, response_data = mail.fetch(num, "(RFC822)")

                    if isinstance(response_data[0], tuple):

                        msg = email.message_from_bytes(response_data[0][1])
                        subject = msg["subject"]
                        from_email = (
                            msg["From"]
                            .split("<")[len(msg["From"].split("<")) - 1]
                            .split(">")[0]
                        )

                        text_body = None

                        try:
                            beautiful_soup = BeautifulSoup(
                                response_data[0][1].decode(), "html.parser"
                            )
                            text_body = beautiful_soup.find("div").text
                        except:
                            text_body = None

                        if text_body == None:

                            if msg.is_multipart():
                                for part in msg.walk():
                                    ctype = part.get_content_type()
                                    cdispo = str(part.get("Content-Disposition"))

                                if ctype == "text/plain" and "attachment" not in cdispo:
                                    text_body = part.get_payload(decode=True)

                            else:
                                text_body = msg.get_payload(decode=True)

                        if text_body == None:
                            continue

                        genai = ChatGoogleGenerativeAI(model="gemini-pro")
                        result = genai.invoke(option[2] + text_body)

                        generated_email = result.content

                        try:

                            result, data = mail.fetch(num, "(UID)")
                            uid = data[0].decode().split("(UID ")[1].split(")")[0]

                            result = mail.uid("COPY", uid.encode(), meru_ai_gmail_label)
                            if result[0] == "OK":
                                mov, data = mail.uid(
                                    "STORE", uid.encode(), "+FLAGS", "(\Deleted)"
                                )
                                mail.expunge()

                                print(
                                    "This email has been moved to the Meru AI Replies inbox successfully."
                                )

                        except Exception as e:
                            print(e)

                        try:
                            meru_ai_reply_to_email(
                                email_address, from_email, subject, generated_email
                            )
                        except Exception as e:
                            print(e)

        mail.logout()
        sleep(int(attempt_interval_in_seconds))

except Exception as e:
    print(e)
    input("An error has occurred. Please close the window and restart the program.")

finally:

    try:
        mail.logout()
    except:
        pass
