from deta import App
import requests
import os
from fastapi import FastAPI
import json

app = App(FastAPI())

@app.get("/")
def http():
    print("running on HTTP")
    print("running save_iss")
    save_iss()
    print("iss pos saved from cron")


@app.lib.cron()
def cron_job(event):
    print("running on a schedule")
    print("running save_iss")
    save_iss()
    print("iss pos saved from cron")


def save_iss():
    try:
        iss_data_response = requests.get('http://api.open-notify.org/iss-now.json')
        iss_data = iss_data_response.json()
        print(iss_data)
        params = {
            'name': 'iss',
            'token': os.getenv('TTOKEN')
        }

        response = requests.post('https://api.tinybird.co/v0/events', data=json.dumps(iss_data), params=params)
        print(response.status_code)
    except Exception as e:
        print('--exception')
        print(str(e))
