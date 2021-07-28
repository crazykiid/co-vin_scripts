'''
Script: Get Beneficiaries
By: CrazyKID (GitHub: @crazykiid)
'''
from os import system
import requests, time, json, hashlib

system('clear')
print('## Script: Get Beneficiaries ##\n')
mobile = input('Enter Phone Number:')

def getOTP(mobile):
  URL = "https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP"
  header = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36' } 
  data = { 'mobile' : mobile }

  result = requests.post(URL, headers=header, data=json.dumps(data))
  if result.ok:
    response_json = result.json()
    return response_json["txnId"]
  else:
    print(result.reason)

def confirmOTP(otp, txnid):
  otp_hash = hashlib.sha256(otp.encode('utf-8')).hexdigest()
  #print(txnid)
  #print(otp_hash)
  URL = "https://cdn-api.co-vin.in/api/v2/auth/public/confirmOTP"
  header = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36' } 
  data = { 'otp' : otp_hash, 'txnId' : txnid }
  result = requests.post(URL, headers=header, data=json.dumps(data))
  if result.ok:
    response_json = result.json()
    return response_json
  else:
    print(result.reason)

def getBeneficiaries(token):
  auth = "Bearer "+token
  #print(auth)
  URL = "https://cdn-api.co-vin.in/api/v2/appointment/beneficiaries"
  header = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 'Authorization' : auth } 
  #auth = 
  result = requests.get(URL, headers=header)
  if result.ok:
    response_json = result.json()
    return response_json
  else:
    print(result.reason)
    
    
otp_txnid = getOTP(mobile)
if otp_txnid:
  #print(otp_txnid)
  otp = input('Enter OTP:')
  token = confirmOTP(otp, otp_txnid)
  if token:
    print("Token:\n"+token["token"])
    beneficiaries = getBeneficiaries(token["token"])
    print(beneficiaries)