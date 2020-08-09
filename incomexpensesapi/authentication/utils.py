from django.core.mail import EmailMessage


class Util:

    #static method attribute
    @staticmethod
    def send_email(data) :
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['email_to']],  # to field receives an array
            )
        email.send()
