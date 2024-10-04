import requests
from datetime import datetime, date
import smtplib
import time

BOISE_LAT = 43.615021
BOISE_LNG = -116.202316

def is_overhead():
    response_iss = requests.get("http://api.open-notify.org/iss-now.json")
    response_iss.raise_for_status()
    data = response_iss.json()

    iss_lat = float(data['iss_position']['latitude'])
    iss_lng = float(data['iss_position']['longitude'])

    #ISS is within 2 miles of Boise
    if iss_lat < 43.64 and iss_lng < -116.22 or iss_lat > 43.592 and iss_lng > -116.18:
        return True

def is_night():
    parameters = {
        "lat": BOISE_LAT,
        "lng": BOISE_LNG,
        "time_format": 24
    }

    response = requests.get(url="https://api.sunrisesunset.io/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = data["results"]["sunrise"].split(":")[0]
    sunset = data["results"]["sunset"].split(":")[0]

    now = datetime.now().hour
    if now > sunset and now < sunrise:
        return True
while True:
    #Every 10 minutes
    time.sleep(600)
    if is_overhead() and is_night():
        #Gmail server info can be replaced with different email ID
        connection = smtplib.SMTP('smtp.gmail.com', 587)
        connection.starttls()
        #Enter personal information here--Not entered for public template sharing
        connection.login('EMAIL_USER', 'EMAIL_PASSWORD')
        from_addr = 'EMAIL_ADDRESS'
        to_addr = 'EMAIL_ADDRESS'
        subject = 'The International Space Station is within 2 miles of Boise! Look up!!'
