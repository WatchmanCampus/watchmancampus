from PIL import Image, ImageFont, ImageDraw
from .models import Tick, Hostel
import uuid
from django.core.mail import EmailMessage
from random import randint


def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())  # Convert UUID format to a Python string.
    random = random.lower()  # Make all characters uppercase.
    random = random.replace("-", "")  # Remove the UUID '-'.
    #usage  = '%s-%s'%('TR',my_random_string(6))
    return random[0:string_length]  # Return the random string.


def generate_ticket(firstname, lastname, gender, diocese, ref):
    fullname = f'{firstname} {lastname}'
    ticket = Tick.objects.get(ref=ref)
    hostel = Hostel.objects.filter(gender_type=gender, hostel_class='Regular', is_available=True)[0]
    hostel.booked.add(ticket.id)
    hostel.rooms_available -= 1
    hostel.save()

    img = Image.open('hilltop.jpg')
    font = ImageFont.truetype("arial.ttf", 30)
    edited = ImageDraw.Draw(img)
    edited.text((300, 300), fullname, (247, 19, 7), font=font)
    edited.text((300, 350), diocese, (247, 19, 7), font=font)
    edited.text((300, 400), hostel.name, (247, 19, 7), font=font)
    img_name = f'media/{firstname}-{ref}.jpg'
    img.save(img_name)
    img = Image.open(img_name)
    ticket.img = f'{firstname}-{ref}.jpg'
    ticket.save()

    return ticket.ref


def email_sending(to_mail, firstname, lastname, location, time, ref):
    body = f'''Hello {firstname}, {lastname}This is a confirmation of your ticket for Hilltop Encounters 2022
    Ticket Summary
    IN-PERSON CONFERENCE
    Time: {time}
    Location: {location}

    The Printable PDF ticket has been attached to this mail.

    Note: Remember to either have a printed copy or a downloaded copy of the ticket when going for the event as you might need to present it for Confirmation and or Check-in.
    Going with Friends is fun

    Let your friends know you are going
    '''
    try:
        message = EmailMessage(
            subject = 'Here is your ticket for Hilltop Encounters 2022',
            body = body,
            from_email = 'captainvee7@gmail.com',
            to = [to_mail, 'captainvee3@gmail.com', ],
        )
        message.attach_file(f'media/{firstname}-{ref}.jpg')
        message.send(fail_silently=False)
    except:
        return False
    return True
