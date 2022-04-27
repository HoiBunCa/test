import requests
import json
import pandas as pd
import numpy as np

#read csv file
df = pd.read_csv('check_fraud_data.csv')

a = []
b = []

for i in range(0, len(df)):
    a.append(np.NaN)  
    b.append(np.NaN)  

df['TrueName'] = a 
df['TrueDOB'] = b

url = "http://203.171.20.122:8081/API/ITRUST/IDSP"
for i in range(0, len(df)):
  payload = json.dumps({
    "ID": str(df['NationalCard'][i])
  })
  
  headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC8xMTUuMTQ2LjEyMy4xNVwvbWFuYWdlclwvcHVibGljIiwic3ViIjoiYjFmMDc3NDUtMmNmMS01OTQzLTgzM2QtZGVmNzc3OTA2MzQ0IiwiaWF0IjoxNjM0MDM0Njg3LCJleHAiOjE4OTMyMzQ2ODcsIm5hbWUiOiJUSU1BIn0.KHtvZTKCvK41ltacuyG_AwIYYxiR98ETjUb4GYWT8CY',
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  if 'data' in response.json():
    print('Name', response.json()['data']['customerName'])
    print('Name', response.json()['data']['dateOfBirth'])

    df['TrueName'][i] = response.json()['data']['customerName']
    df['TrueDOB'][i] = response.json()['data']['dateOfBirth']
    i = i + 1
  elif 'success' in response.json():
    i = i + 1


df.to_csv('newFileCraw.csv')


