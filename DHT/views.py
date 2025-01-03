from django.shortcuts import render
from .models import Dht11  # Assurez-vous d'importer le modèle Dht11
from django.utils import timezone
import csv
from django.http import HttpResponse
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/table')  # Redirige vers la page après connexion
        else:
            return render(request, 'home.html', {'error': "Nom d'utilisateur ou mot de passe incorrect"})

    return render(request, 'home.html', {'error': error})
def logout_user(request):
    logout(request)
    return redirect('/')



from django.shortcuts import render
from django.utils import timezone
from .models import Dht11
from datetime import timedelta

def table(request):
    # Get the last record
    derniere_ligne = Dht11.objects.last()

    # Get the records for the last 7 days
    last_7_days = Dht11.objects.filter(dt__gte=timezone.now() - timedelta(days=7))

    if derniere_ligne:
        # Get the datetime of the last record
        derniere_date = derniere_ligne.dt

        # Calculate the time difference in minutes
        delta_temps = timezone.now() - derniere_date
        difference_minutes = delta_temps.seconds // 60
        temps_ecoule = f'il y a {difference_minutes} min'

        # Format in hours and minutes if more than 60 minutes
        if difference_minutes >= 60:
            heures = difference_minutes // 60
            minutes = difference_minutes % 60
            temps_ecoule = f'il y a {heures}h {minutes}min'

        # Prepare the context
        valeurs = {
            'date': temps_ecoule,
            'id': derniere_ligne.id,
            'temp': derniere_ligne.temp,
            'hum': derniere_ligne.hum
        }
    else:
        valeurs = {
            'date': 'Aucune donnée disponible',
            'id': None,
            'temp': None,
            'hum': None
        }

    # Prepare data for the last 7 days
    historique = [
        {
            'date': data.dt.strftime("%Y-%m-%d"),
            'temp': data.temp,
            'hum': data.hum
        }
        for data in last_7_days
    ]

    return render(request, 'value.html', {'valeurs': valeurs, 'historique': historique})


def download_csv(request):
    model_values = Dht11.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dht.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'temp', 'hum', 'dt'])
    liste = model_values.values_list('id', 'temp', 'hum', 'dt')
    for row in liste:
        writer.writerow(row)
    return response
def csv_jour(request):
    now = timezone.now()
    last_24_hours = now - timezone.timedelta(hours=24)
    model_values = Dht11.objects.filter(dt__range=(last_24_hours, now))
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dhtJOUR.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'temp', 'hum', 'dt'])
    liste = model_values.values_list('id', 'temp', 'hum', 'dt')
    for row in liste:
        writer.writerow(row)
    return response
def csv_semaine(request):
    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=7)
    print(datetime.timedelta(days=7))
    print(date_debut_semaine)
    model_values =  Dht11.objects.filter(dt__gte=date_debut_semaine)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dhtSEMAINE.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'temp', 'hum', 'dt'])
    liste = model_values.values_list('id', 'temp', 'hum', 'dt')
    for row in liste:
        writer.writerow(row)
    return response
def csv_mois(request):
    dht = Dht11.objects.all()
    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=30)
    print(datetime.timedelta(days=30))
    print(date_debut_semaine)
    model_values =  Dht11.objects.filter(dt__gte=date_debut_semaine)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dhtMOIS.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'temp', 'hum', 'dt'])
    liste = model_values.values_list('id', 'temp', 'hum', 'dt')
    for row in liste:
        writer.writerow(row)
    return response
#pour afficher navbar de template
def index_view(request):
    return render(request, 'index.html')

#pour afficher les graphes
def chartTEMP(request):
    tab=Dht11.objects.all()
    s={'tab':tab}
    return render(request,'ChartTemp.html',s)
def chartHUM(request):
    tab=Dht11.objects.all()
    s={'tab':tab}
    return render(request, 'ChartHum.html',s)

#pour récupérer les valeurs de température et humidité de dernier 24h
# et envoie sous forme JSO
# récupérer toutes les valeur de température et humidity sous forme un #fichier json
def chart_data(request):
    dht = Dht11.objects.all()

    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)

#pour récupérer les valeurs de température et humidité de dernier 24h
# et envoie sous forme JSON
def chart_hum_jour(request):
    now = timezone.now()
# Récupérer l'heure il y a 24 heures
    last_24_hours = now - timezone.timedelta(hours=24)
# Récupérer tous les objets de Module créés au cours des 24 dernières
    tab= Dht11.objects.filter(dt__range=(last_24_hours, now))
    s = {'tab': tab}
    return render(request, 'ChartHum.html', s)

# et envoie sous forme JSON
def chart_hum_semaine(request):
    dht = Dht11.objects.all()
    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=7)
    print(datetime.timedelta(days=7))
    print(date_debut_semaine)
    tab = Dht11.objects.filter(dt__gte=date_debut_semaine)
    s = {'tab': tab}
    return render(request, 'ChartHum.html', s)

#pour récupérer les valeurs de température et humidité de dernier moins
# et envoie sous forme JSON
def chart_hum_mois(request):
    dht = Dht11.objects.all()
    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=30)
    print(datetime.timedelta(days=30))
    print(date_debut_semaine)
    tab= Dht11.objects.filter(dt__gte=date_debut_semaine)
    s = {'tab': tab}
    return render(request, 'ChartHum.html', s)
def chart_temp_jour(request):
    now = timezone.now()
# Récupérer l'heure il y a 24 heures
    last_24_hours = now - timezone.timedelta(hours=24)
# Récupérer tous les objets de Module créés au cours des 24 dernières
    tab= Dht11.objects.filter(dt__range=(last_24_hours, now))
    s = {'tab': tab}
    return render(request, 'ChartTemp.html', s)
def chart_temp_semaine(request):
    dht = Dht11.objects.all()
    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=7)
    print(datetime.timedelta(days=7))
    print(date_debut_semaine)
    tab = Dht11.objects.filter(dt__gte=date_debut_semaine)
    s = {'tab': tab}
    return render(request, 'ChartTemp.html', s)
def chart_temp_mois(request):
    dht = Dht11.objects.all()
    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=30)
    print(datetime.timedelta(days=30))
    print(date_debut_semaine)
    tab= Dht11.objects.filter(dt__gte=date_debut_semaine)
    s = {'tab': tab}
    return render(request, 'ChartTemp.html', s)
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


import matplotlib.pyplot as plt
import numpy as np
from django.http import HttpResponse
from .models import Dht11



def sendtele():
    token = '6662023260:AAG4z48OO9gL8A6szdxg0SOma5hv9gIII1E'
    rece_id = 1242839034
    bot = telepot.Bot(token)
    bot.sendMessage(rece_id, 'la température depasse la normale')
    print(bot.sendMessage(rece_id, 'OK.'))