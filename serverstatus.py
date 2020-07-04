#!/usr/bin/python3

import os
import requests as req
import subprocess

from datetime import datetime, timedelta, timezone


def h(*values: int) -> str:
    """
    Returns sizes in power of 1024.

    :param values: size in KiB (up to 2^30).
    """
    prefix = ['KiB', 'MiB', 'GiB']
    index = 0
    m = max(values)
    while m > 1024:
        m /= 1024
        index += 1

    if len(values) == 1:
        return '%.2f %s' % (m, prefix[index])
    else:
        return ['%.2f %s' % (v / 2 ** (10 * index), prefix[index]) for v in values]


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
temp = '%.2f' % (int(temp_str) / 1000)

cache = h(int(subprocess.check_output(
    ['du', '-s', '/home/mastodon/live/public/system/cache']
).split()[0]))
media = h(int(subprocess.check_output(
    ['du', '-s', '/home/mastodon/live/public/system/media_attachments']
).split()[0]))
disc_used_int, disc_avail_int = map(int, subprocess.check_output(
    ['df', '--output=used,avail', '/']
).split()[2:4])
disc_used, disc_total = h(disc_used_int, disc_used_int + disc_avail_int)

data_dic = {
    'status': f'[Status] {now_str}\n'
              f'System Volume: {disc_used}/{disc_total}\n'
              f'Media Usage: {media}\n'
              f'Cache Usage: {cache}\n'
              f'CPU Temp: {temp}\u00b0C',
    'visibility': 'unlisted',
}

r = req.post(apiurl, data=data_dic, headers=header)

dir = os.path.dirname(__file__)
path = os.path.join(dir, 'serverstatus', 'log.txt')
with open(path, 'a') as f:
    f.write(f'time: {now_str}, status: {r.status_code}\n')
