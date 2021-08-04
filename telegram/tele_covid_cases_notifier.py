
'''
Script: Telegram Covid Cases Notifier - India
By: CrazyKID (GitHub: @crazykiid)
'''
import time, requests, json, sys
from bs4 import BeautifulSoup as bs


# sent telegram notification
def notify(message=None):
  TELEGRAM_TOKEN = '1779941360:AAFKVrwGb54f0gxtDUxvl_DN8gJKmxRj3IE'
  TELEGRAM_CHANNEL = '@in_covidinfo'
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

def run(c="india"):
  source = 'https://www.worldometers.info'
  source_link = source + '/coronavirus/country/'+c+'/'
  source_data = []
  try:
    # get html
    response = requests.get(source_link)
    # parse
    soup = bs(response.text, 'html.parser')
    # search
    search = soup.find( class_ = "content-inner" )
    # get country
    country_raw = search.select_one('div h1')
    country = country_raw.get_text().strip()
    source_data.append(country)
    # get country flag url
    flag_raw = search.select_one('div h1 div img')
    flag = source+flag_raw.get('src')
    source_data.append(flag)
    # get date
    date_raw = search.select('div div')
    date = ""
    count_a = 1
    for j in date_raw:
      if count_a > 2:
        break
      elif count_a == 2:
        date = j.get_text()
      else:
        pass
      count_a += 1
    source_data.append(date)
    # get case count
    case_raw = search.select('div div div div span')
    count = 1
    cases = []
    for i in case_raw:
      if count > 3:
        break
      i = i.get_text()
      cases.append(i)
      count += 1
    source_data.append(cases)
  except requests.exceptions.RequestException as e: 
    print(e)
  return source_data


print('## Script: Covid Cases Notifier - India ##\n')
# start
data = []
last_update = ""
l = 0
frequency = 1800 # 30 min
while True:
  rmline(l)
  l = 0
  wait = frequency
  data = run()
  if data:
    if data[2] != last_update:
      print('Status: new update found')
      message = f'<b>Coronavirus Cases - {data[0]}</b>\n\nCases: <b>{data[3][0]}</b>\nDeaths: <b>{data[3][1]}</b>\nRecovered: <b>{data[3][2]}</b>\n\n({data[2]})'
      status = notify(message)
      if status["ok"]:
        print('(telegram notification sent)')
        last_update = data[2]
      else:
        print('(telegram notification failed)')
      wait = 3
    else:
      print(f'Status: no update found \n(will recheck after {frequency} sec)')
    l += 2
  else:
    message = 'something went wrong, try again!'
    print('(+message+)')
    status = notify(message)
    l += 1
  time.sleep(wait)