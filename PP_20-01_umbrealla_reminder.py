# Umbrella Reminder
# Chapter 13 showed you how to use the requests module to scrape data from https://weather.gov. Write a program that runs just before you wake up in the morning
# and checks whether rain is in the forecast for that day. If so, have the program text you a reminder to pack an umbrella before leaving the house.

import requests
import datetime
import time
import json
from pathlib import Path

p = Path('weather_credentials.txt')
credentials = p.read_text()
credentials = credentials.splitlines()
API_key = credentials[0]
NFTY_server = credentials[1]

city_name = 'Warsaw'
country_code = 'PL'
last_check_date = None


while True:
    dt = datetime.datetime.now()
    if dt.hour == 7 and dt.minute == 59 and dt.date() != last_check_date:
        print("Checking the weather...")
        last_check_date = dt.date()
        response = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&appid={API_key}')
        response_data = json.loads(response.text)
        lat = response_data[0]['lat']
        lon = response_data[0]['lon']
        response = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}')
        response_data = json.loads(response.text)
        #print(json.dumps(response_data, indent=4))
        for forecast in response_data['list']:
            forecast_date = datetime.datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S')
            if forecast_date.date() == dt.date():
                print(forecast['dt_txt'], forecast['weather'][0]['main'])
                weather = forecast['weather'][0]['main']
                if weather == "Rain" or weather == "Drizzle":
                    requests.post(NFTY_server, "Take an umbrella!")
                    print("Rain warning sent.")
                    break
            else:
                break
    else:     
        if dt.minute < 10:
            minutes = '0' + str(dt.minute)
        else:
            minutes = dt.minute
        print(f"{dt.hour}:{minutes} Nothing to do.")
    time.sleep(20)








