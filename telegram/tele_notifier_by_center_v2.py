'''
Script: Telegram Covin Notifier v2 - By Center(s)
By: CrazyKID (GitHub: @crazykiid)
'''
from os import system
from datetime import datetime, timedelta
import requests, time, sys, json
import pytz

# get time, date
def gtd(var=None):
  tz_in = pytz.timezone('Asia/Kolkata')   
  now = datetime.now(tz_in)
  if var == "time":
    return now.strftime("%H:%M:%S")
  elif var == "date":
    return now.strftime("%d-%m-%Y")
  elif var == "date_next":
    next = now + timedelta(days=1)
    return next.strftime("%d-%m-%Y")
  else:
    return now

# send telegram notification
def notify(message=None):
  TELEGRAM_TOKEN = '1779941360:AAFKVrwGb54f0gxtDUxvl_DN8gJKmxRj3IE'
  TELEGRAM_CHANNEL = '@my_vac_notifier'
  payload = {
    'chat_id': TELEGRAM_CHANNEL,
    'text': message,
    'parse_mode': 'HTML'
  }
  response = requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=TELEGRAM_TOKEN), data=payload).content
  return json.loads(response.decode('utf-8'))

# remove line
def rmline(n=1):
  while n > 0:
    sys.stdout.write("\033[K")
    sys.stdout.write("\033[F")
    n -= 1

# run process
def run(centers=[], set_gap=60):
  system('clear')
  print('## Script: Telegram Covin Notifier v2 - By Center(s) ##')
  total = len(centers)
  given_date = str(gtd("date_next"))
  print(f'\nObject: check session availability of {total} centers for {given_date}\nUpdate: after every {set_gap} sec')
  l = 0
  print('Status: running')
  while True:
    # if given date and current date are same
    if given_date == gtd("date"):
      break
    rmline(l)
    l = 0
    wait = set_gap
    print(f'Queue : {len(centers)} left')
    print('Result:')
    l += 2
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
          wait = 1
          break
        else:
          print(f'{gtd("time")} - no session available for {centerid}')
          l += 1
      else:
        pass
    if not centers:
      rmline(l+1)
      print(f'Status: stopped\nQueue : {len(centers)} left')
      break
    time.sleep(wait)
  return True

system('clear')
# introduction
print('## Script: Telegram Covin Notifier v2 - By Center(s) ##')
centers = input('\nEnter center code(s):')
centers = centers.split(',')
centers = [x.strip(' ') for x in centers]
gap = int(input("Time gap (in seconds):"))

# start
while True:
  today = str(gtd("date"))
  # invoke run process
  status = run(list(centers), gap)
  if status:
    # waiting for next day
    while True:
      now = gtd("date")
      if today == now:
        print("Result: nothing left for today, waiting for next day")
        time.sleep(60)
        rmline()
      else:
        break