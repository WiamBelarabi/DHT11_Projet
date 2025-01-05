from django.core.mail import send_mail
from django.conf import settings
from .models import Dht11
from .serializers import DHT11serialize
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from twilio.rest import Client
import requests
from .models import Dht11, Incident
person_counter = 0
def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response
@api_view(["GET", "POST"])
def Dlist(request):
    global person_counter

    if request.method == "GET":
        all = Dht11.objects.all()
        data_ser = DHT11serialize(all, many=True)  # Les données sont sérialisées en JSON
        return Response(data_ser.data)

    elif request.method == "POST":
        serial = DHT11serialize(data=request.data)

        if serial.is_valid():
            serial.save()
            derniere_temperature = Dht11.objects.last().temp
            print(derniere_temperature)

            #alertes
            if derniere_temperature > 25:
                Incident.objects.create(temperature=derniere_temperature)

                if person_counter == 0:
                    #alerte whatsapp
                    account_sid = 'AC9a44f63eaaccb841d7c27c5bc38bd8e5'
                    auth_token = '7fba83fffe62851072a2bb2f19a4cb4c'
                    client = Client(account_sid, auth_token)
                    message_whatsapp = client.messages.create(
                        from_='whatsapp:+14155238886',
                        body='La température dépasse le seuil, veuillez intervenir immédiatement pour vérifier et corriger cette situation',
                        to='whatsapp:+212762374139'
                    )
                    #alerte telegrame
                    telegram_token = '7062029872:AAGDu-hzpcuBcLyiRekV3HCiMW8n5DFUcnk'
                    chat_id = '6791282158'  # Remplacez par votre ID de chat
                    telegram_message = 'La température dépasse le seuil , veuillez intervenir immédiatement pour vérifier et corriger cette situation'
                    send_telegram_message(telegram_token, chat_id, telegram_message)
                    #alert mail
                    subject = 'Alerte'
                    message = 'La température dépasse le seuil, veuillez intervenir immédiatement pour vérifier et corriger cette situation'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = ['wiambelarabi10@gmail.com']
                    send_mail(subject, message, email_from, recipient_list)
                elif person_counter == 1:
                    # alerte whatsapp
                    account_sid = 'AC9a44f63eaaccb841d7c27c5bc38bd8e5'
                    auth_token = '7fba83fffe62851072a2bb2f19a4cb4c'
                    client = Client(account_sid, auth_token)
                    message_whatsapp = client.messages.create(
                        from_='whatsapp:+14155238886',
                        body='La température dépasse le seuil, veuillez intervenir immédiatement pour vérifier et corriger cette situation',
                        to='whatsapp:+212762374139'
                    )
                    # alerte telegrame
                    telegram_token = '7062029872:AAGDu-hzpcuBcLyiRekV3HCiMW8n5DFUcnk'
                    chat_id = '6791282158'  # Remplacez par votre ID de chat
                    telegram_message = 'La température dépasse le seuil , veuillez intervenir immédiatement pour vérifier et corriger cette situation'
                    send_telegram_message(telegram_token, chat_id, telegram_message)
                    # alert mail
                    subject = 'Alerte'
                    message = 'La température dépasse le seuil, veuillez intervenir immédiatement pour vérifier et corriger cette situation'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = ['wiambelarabi10@gmail.com']
                    send_mail(subject, message, email_from, recipient_list)

                person_counter += 1

            if derniere_temperature < 25:
                person_counter = 0
            return Response(serial.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
