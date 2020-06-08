#!/usr/bin/python3

import os
import requests as req
import subprocess

from datetime import datetime, timedelta, timezone


host = 'mstdn.mell0w-5phere.net'
apiurl = f'https://{host}/api/v1/statuses'

token = os.environ.get('API_TOKEN', '')
header = {'Authorization': f'Bearer {token}'}

timezone = timezone(timedelta(hours=9))
now = datetime.now(tz=timezone)
now_str = now.strftime('%Y-%m-%dT%H:%M:%S%z')
temp_str = subprocess.check_output(
    ['cat', '/sys/class/thermal/thermal_zone0/temp']
)
temp = int(temp_str) / 1000

data_dic = {
    'status': f'[Status] {now_str}\n'
              f'CPU Temp: {temp}\u00b0C',
    'visibility': 'unlisted',
}

r = req.post(apiurl, data=data_dic, headers=header)

dir = os.path.dirname(__file__)
path = os.path.join(dir, 'serverstatus', 'log.txt')
with open(path, 'a') as f:
    f.write(f'time: {now_str}, status: {r.status_code}\n')
