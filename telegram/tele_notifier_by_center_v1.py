'''
Script: Telegram Covin Notifier v1 - By Center(s)
By: CrazyKID (GitHub: @crazykiid)
'''
from os import system
from datetime import datetime
import requests, time, sys, pytz, json

# get time
def gtd(var=None):
  tz_in = pytz.timezone('Asia/Kolkata')   
  now = datetime.now(tz_in)
  if var == "time":
    return now.strftime("%H:%M:%S")
  else:
    return now

# remove line
def rmline(n=1):
  while n > 0:
    sys.stdout.write("\033[K")
    sys.stdout.write("\033[F")
    n -= 1

# send telegram notification
def notify(message):
  TELEGRAM_TOKEN = '1779941360:AAFKVrwGb54f0gxtDUxvl_DN8gJKmxRj3IE'
  TELEGRAM_CHANNEL = '@my_vac_notifier'
  payload = {
    'chat_id': TELEGRAM_CHANNEL,
    'text': message,
    'parse_mode': 'HTML'
  }
  response = requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=TELEGRAM_TOKEN), data=payload).content
  return json.loads(response.decode('utf-8'))


system('clear')
print('## Script: Telegram Covin Notifier v1 - By Center(s) ##')
centers = input('\nEnter center code(s):')
centers = centers.split(',')
centers = [x.strip(' ') for x in centers]
given_date = input('Enter date (dd-mm-yyyy):')
gap = int(input("Time gap (in seconds):"))
print('Result:')
l = 0
while True:
  rmline(l)
  l = 0
  wait = gap
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
          print(f'{gtd("time")} - session found for {centerid}')
          message = f'<b>{center["name"]} (ID: {center["center_id"]})</b>\nPincode: <b>{center["pincode"]}</b>\nDate: <b>{session["date"]}</b>\nVaccine: <b>{session["vaccine"]}</b>\nType: <b>{center["fee_type"]}</b>\n\n<b>Available Capacity</b>\nDose1: <b>{session["available_capacity_dose1"]}</b>\nDose2: <b>{session["available_capacity_dose2"]}</b>'
          status = notify(message)
          if status["ok"]:
            print('(telegram notification sent)')
            centers.remove(centerid)
          else:
            print(f'(telegram notification failed - error {status["error_code"]})')
            l += 2
          break
        wait = 0
        break
      else:
        print(f'{gtd("time")} - no session available for {centerid}')
        l += 1
    else:
      pass
  if not centers:
    print('Finished')
    break
  time.sleep(wait)