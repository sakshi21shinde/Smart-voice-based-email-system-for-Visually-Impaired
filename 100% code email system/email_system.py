# speechrecognition==3.10.4


import imaplib
import email
import speech_recognition as sr
import pyttsx3
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from bs4 import BeautifulSoup

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level

def speak(text):
    """Function to play system audio without using MP3 files."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Function to listen to user input and recognize speech."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.record(source, duration=5)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            speak(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I could not understand. Please try again.")
          #  return ""
            return listen()  # Retry
        except sr.RequestError:
            speak("Could not connect to the speech recognition service.")
            #return ""
            return None

# Announce Project Name
speak("Voice Email System for Blind People")
print("Voice Email System for Blind People")

# Menu options
speak("Option 1. Compose your mail")
print("1. Compose Your Mail")

speak("Option 2. Check your inbox")
print("2. Check Your Inbox")

speak("Option 3. Delete your mail")
print("3. Delete Your Mail")

speak("Please speak your choice")
choice = listen()

if choice in ['1', 'one','when']:
    try:
        speak("Please enter subject")
        print("Please enter subject")
        subject = listen()
        
        speak("Please say the body of the mail")
        print("Please say the body of the mail")
        body = listen()
        
        speak("Please say the receiver's email ID")
        print("Receiver Email ID:")
        receiver_email = listen().replace(" ", "") + "@gmail.com"
        
        speak("Do you want to attach a file? Say yes or no")
        print("Do you want to attach a file? (Yes/No)")
        attach_choice = listen()
        
        msg = MIMEMultipart()
        msg['From'] = "sabalen252@gmail.com"
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, "plain"))
        
        if attach_choice in ["yes", "yeah"]:
            speak("Please say the file name you want to attach")
            print("Please say the file name")
            file_name = listen()
            file_path = f"C:/Users/Sakshi/OneDrive/Desktop/{file_name}.pdf"
            
            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={file_name}.pdf")
                msg.attach(part)
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("sabalen252@gmail.com", "pmkihcpfxrehstnp")
        server.sendmail("sabalen252@gmail.com", receiver_email, msg.as_string())
        server.quit()
        
        speak("Congratulations! Your mail has been sent.")
        print("Mail sent successfully!")
    except Exception as e:
        print("Error:", str(e))
        speak("An error occurred. Please try again.")

elif choice in ['2', 'two', 'to','Tu','2 2','Option 2. Check your inbox','Option 2']:
   # Connect to Gmail IMAP Server
    mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    mail.login('sabalen252@gmail.com', 'pmkihcpfxrehstnp')  # Use App Password

    # Select inbox
    mail.select("Inbox")

    # Count total emails
    status, total_mails = mail.search(None, 'ALL')
    total_count = len(total_mails[0].split())

    # Count unseen (unread) emails
    status, unseen_mails = mail.search(None, 'UNSEEN')
    unseen_count = len(unseen_mails[0].split()) if unseen_mails[0] else 0

    # Speak email counts
    speak(f"You have {total_count} total emails.")
    speak(f"You have {unseen_count} unread emails.")

    print(f"Total Emails: {total_count}")
    print(f"Unread Emails: {unseen_count}\n")

    # Fetch the latest 2 emails
    mail_ids = unseen_mails[0].split()[:5]
    
    if not mail_ids:
        print("No new emails found.")
    else:
        print(f"Fetching {len(mail_ids)} unread emails...")
    
    for num in mail_ids:
        status, email_data = mail.fetch(num, "(RFC822)")
        
        if not email_data or email_data[0] is None:
            print(f"Failed to fetch email {num}")
            continue
    
        raw_email = email_data[0][1]
        email_message = email.message_from_bytes(raw_email)  # Use message_from_bytes()
    
        sender = email_message["From"]
        subject = email_message["Subject"]
    
        speak(f"From: {sender}. Subject: {subject}.")
        print(f"From: {sender}")
        print(f"Subject: {subject}")
    
        # Extract email body
        body_text = None
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                charset = part.get_content_charset() or "utf-8"  # Handle encoding
                body_text = part.get_payload(decode=True).decode(charset, errors="ignore")
                break
    
        if body_text:
            preview_body = body_text[:200]  # Limit to 200 characters
            speak(f"Email Body Preview: {preview_body}")
            print(f"Body Preview:\n{preview_body}\n")
        else:
            print("No plain text content found.")
    
    mail.logout()

# except Exception as e:
#     print("Error:", str(e))
#     speak("An error occurred while checking emails.")

elif choice in ['3', 'three','tree']:
    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login('sabalen252@gmail.com', 'pmkihcpfxrehstnp')
        imap.select("INBOX")
        
        speak("Please speak the subject of the email you want to delete")
        subject_to_delete = listen()
        
        status, messages = imap.search(None, f'SUBJECT "{subject_to_delete}"')
        messages = messages[0].split()
        
        for mail_id in messages:
            imap.store(mail_id, "+FLAGS", "\\Deleted")
        
        imap.expunge()
        imap.close()
        imap.logout()
        speak("Your mail has been successfully deleted.")
    except Exception as e:
        print("Error:", str(e))
        speak("An error occurred while deleting the email.")

else:
    speak("Invalid choice. Please restart the system and try again.")
