'''
Script: Covin Center Information Generator
By: CrazyKID (GitHub: @crazykiid)
'''
import time, requests, json, sys, os
import sqlite3

# Table Setup
def tableSetup(db):
  conn = ''
  try:
    # Connecting to sqlite
    conn = sqlite3.connect(db)
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    # SQL
    sql = """CREATE TABLE IF NOT EXISTS CENTER (
      center_id INT PRIMARY KEY,
      name TEXT,
      address TEXT,
      state_name TEXT,
      district_name TEXT,
      block_name TEXT,
      pincode INT,
      lat INT,
      long INT,
      time_from TEXT,
      time_to TEXT,
      fee_type TEXT
    )"""
    # Execute
    cursor.execute(sql)
    # Commit changes
    conn.commit()
    os.system('clear')
    #print('Center table created')
  except sqlite3.Error as e:
    os.system('clear')
    print(f"Error {e.args[0]}")
    sys.exit(1)
  finally:
    if conn:
      # Terminate the connection
      conn.close()

# Save Data
def insertCenter(db, data = ''):
  conn = ''
  try:
    # Connecting to sqlite
    conn = sqlite3.connect(db)
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    # Preparing SQL queries to INSERT a record into the database.
    sql = '''INSERT INTO CENTER (
      center_id,
      name,
      address,
      state_name,
      district_name,
      block_name,
      pincode,
      lat,
      long,
      time_from,
      time_to,
      fee_type
    ) VALUES (
      ?,?,?,?,?,?,?,?,?,?,?,?
    )'''
    # Execute
    cursor.execute(sql, data)
    # Commit changes
    conn.commit()
  except sqlite3.Error as e:
    os.system('clear')
    print(f"Error {e.args[0]}")
    sys.exit(1)
  finally:
    if conn:
      # Terminate the connection
      conn.close()

# Main
def main():
  # Database file location
  db = os.path.dirname(os.path.realpath(__file__))+'/covin.sqlite3'
  tableSetup(db)
  centerid = 1
  given_date = "31-08-2021"
  while True:
    os.system('clear')
    print('fetching...')
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByCenter?center_id={}&date={}".format(centerid, given_date)
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'} 
    result = requests.get(URL, headers=header)
    if result.ok:
      response_json = result.json()
      if response_json:
        center = response_json["centers"]
        json_formatted_str = json.dumps(center, indent=2)
        os.system('clear')
        print(json_formatted_str)
        data = [
          center['center_id'],
          center['name'],
          center['address'],
          center['state_name'],
          center['district_name'],
          center['block_name'],
          center['pincode'],
          center['lat'],
          center['long'],
          center['from'],
          center['to'],
          center['fee_type']
        ]
        insertCenter(db, data)
        time.sleep(1)
      else:
        pass
        #print(f'CenterID: {centerid} (not found)')
        #time.sleep(1)
    else:
      print('error')
    centerid += 1
    
# start
main()