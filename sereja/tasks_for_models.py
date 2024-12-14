from sereja.celery import app
from sereja.settings import *
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

@app.task(bind=True, default_retry_delay=60)
def send_mail_task(self, subject, message, from_email, recipients):
    mes = Mail(
    from_email=from_email,
    to_emails=recipients,
    subject=subject,
    html_content=message)
    #message = 'Hello from Django'
    #html_message = render_template(f'{template}.html', context)
    try:
        sg = SendGridAPIClient(EMAIL_HOST_PASSWORD)
        response = sg.send(mes)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as ex:
        self.retry(exc=ex)
