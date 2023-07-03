from .models import Tick, Hostel
import uuid
from django.core.mail import EmailMessage
from random import randint


def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())  # Convert UUID format to a Python string.
    random = random.lower()  # Make all characters uppercase.
    random = random.replace("-", "")  # Remove the UUID '-'.
    # usage  = '%s-%s'%('TR',my_random_string(6))
    return random[0:string_length]  # Return the random string.


def generate_ticket(ticket_id):
    pass


def email_sending(to_mail, firstname, lastname, location, time, ref):
    body = f"""
    <html>
    <head></head>
    <body>
        <p><strong>Hello {firstname}, {lastname}</strong></p>
        <p>This is a confirmation of your ticket for Hilltop Encounters 2022</p>
        <h2>Ticket Summary</h2>
        <p>IN-PERSON CONFERENCE</p>
        <p><strong>Time:</strong> 2023-06-16 05:49:49+00:00</p>
        <p><strong>Location:</strong>  Awo mamma</p>
        <p> The Printable PDF ticket has been attached to this mail.</p>
        <p>Note: Remember to either have a printed copy or a downloaded copy of the ticket when going for the event as you might need to present it for Confirmation and or Check-in.</p>
        <p>Going with Friends is fun</p>
        
        <p>Let your friends know you are going</p>
        
        <p>for more info, visit the
        <a href='https://www.watchmancampus.org/'>watchman campus website</a>.

    </body>
    </html>
    """
    try:
        message = EmailMessage(
            subject="A Snapshot of Friendly Advice!", #"Your ticket for Hilltop Encounters 2023",
            body=body,
            from_email="captainvee7@gmail.com",
            to=[
                to_mail, "mosesvictor2015@gmail.com"
            ],
        )
        message.content_subtype = "html"
        message.attach_file(f"media/{firstname}-{ref}.jpg")
        message.send(fail_silently=False)
    except:
        return False
    return True
