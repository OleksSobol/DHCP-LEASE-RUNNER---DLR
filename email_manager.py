import datetime
import smtplib
import os
import requests
from email.message import EmailMessage


class EmailSender:
    def send_email_with_attachment(self, body=""):
        url = "https://icanhazdadjoke.com/"
        headers = {"Accept": "application/json"}

        try:
            # Get the current date in the format '01-29-24'
            current_date = datetime.datetime.now().strftime('%m-%d-%y')
            formatted_datetime = datetime.datetime.now().strftime('%H:%M:%S %m-%d-%Y')

            # Construct the log file paths
            base_directory = os.path.dirname(__file__)
            logs_directory = os.path.join(base_directory, 'logs')
            log_file_path1 = os.path.join(logs_directory, f'{current_date} - dhcp_server_lease_runner.log')
            log_file_path2 = os.path.join(logs_directory, f'{current_date} - whole_dhcp_server_lease_runner.log')

            # Create an EmailMessage object
            msg = EmailMessage()

            # Recipients
            recipients = ['EMAILS']
            # recipients = ['osobol@theglobal.net']
            # Set email details
            msg['Subject'] = f'Dynamic Lease Runner (DLR) Log for {current_date}'
            msg['From'] = "dlr@theglobal.net"
            msg['To'] = ", ".join(recipients)
            msg.set_content(body + (f"Email sent: {formatted_datetime} "))

            # Attach the log files
            for log_file_path in [log_file_path1, log_file_path2]:
                try:
                    with open(log_file_path, 'rb') as log_file:
                        msg.add_attachment(log_file.read(), maintype='text', subtype='plain',
                                           filename=os.path.basename(log_file_path))
                except Exception as e:
                    msg.set_content(f"Failed to attach log file: {e} \nEmail sent: {formatted_datetime}")

            # Send the message via SMTP server.
            s = smtplib.SMTP('theglobal-net.mail.protection.outlook.com', port=25)
            s.send_message(msg)
            s.quit()
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")

