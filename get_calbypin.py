'''
Script: Get Calander By Pincode(s)
By: CrazyKID (GitHub: @crazykiid)
'''
from os import system
import requests, time

system('clear')
script = '## Script: Get Calander By Pincode(s) ##\n'
print(script)
pins = input('Enter pincode(s):')
pincodes = pins.split(',')
given_date = input('Enter date (dd-mm-yyyy):')
gap = int(input("Time gap (in seconds):"))

while True:
  system('clear')
  print(script)
  for pincode in pincodes:
    pincode = pincode.strip()
    print(f'## Results for pincode "{pincode}"')
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode, given_date)
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'} 
    result = requests.get(URL, headers=header)
    if result.ok:
      response_json = result.json()
      if response_json["centers"]:
        for center in response_json["centers"]:
          print(f'>> Center: {center["name"]} (ID:{center["center_id"]})')
          for session in center["sessions"]:
            print(f'   {session["date"]} Dose1:{session["available_capacity_dose1"]} Dose2:{session["available_capacity_dose2"]} ({center["fee_type"]})')
      else:
        print(">> no session available\n")
    else:
      print(result.reason)
  time.sleep(gap)