import random
import datetime
import secrets, string

from django.core.mail import send_mail
from core import settings

def generate_code():
    code =random.randint(1000, 9999)   

    return code

def send_code(code,email):
    
        res = send_mail(
                        subject= "Код для подверждение",
                        message=f'{code}',
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[email,],
                        fail_silently=False,
                    )
        print(res)
        print("sent code",settings.EMAIL_HOST_USER)
        print(email)
        return True
    