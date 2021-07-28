'''
Script: Telegram Covin Notifier - By Center(s)
By: CrazyKID (GitHub: @crazykiid)
'''
from os import system
from datetime import datetime
import requests, time, sys

def notify(message):
  TELEGRAM_TOKEN = '1779941360:AAFKVrwGb54f0gxtDUxvl_DN8gJKmxRj3IE'
  TELEGRAM_CHANNEL = '@my_vac_notifier'
  payload = {
    'chat_id': TELEGRAM_CHANNEL,
    'text': message,
    'parse_mode': 'HTML'
  }
  request = requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=TELEGRAM_TOKEN), data=payload).content

system('clear')
print('## Script: Telegram Covin Notifier - By Center(s) ##')
centers = input('Enter center code(s):')
centers = centers.split(',')
given_date = input('Enter date (dd-mm-yyyy):')
gap = int(input("Time gap (in seconds):"))

print('Status: running...')
while True:
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  for centerid in centers:
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByCenter?center_id={}&date={}".format(centerid, given_date)
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'} 
    result = requests.get(URL, headers=header)
    if result.ok:
      response_json = result.json()
      if response_json:
        center = response_json["centers"]
        for session in center["sessions"]:
          message = f'<b>{center["name"]} (ID: {center["center_id"]})</b>\nPincode: <b>{center["pincode"]}</b>\nDate: <b>{session["date"]}</b>\nVaccine: <b>{session["vaccine"]}</b>\nType: <b>{center["fee_type"]}</b>\n\n<b>Available Capacity</b>\nDose1: <b>{session["available_capacity_dose1"]}</b>\nDose2: <b>{session["available_capacity_dose2"]}</b>'
          notify(message)
          centers.remove(centerid)
      else:
        sys.stdout.write("\033[K")
        print(f'{current_time} - no session available')
        sys.stdout.write("\033[F")
  if not centers:
    sys.stdout.write("\033[K")
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")
    print('Status: stopped')
    print(f'{current_time} - script ended')
    break
  time.sleep(gap)