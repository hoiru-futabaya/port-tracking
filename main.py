#! /usr/bin/env python3
# coding: 'utf-8'

import json
import urllib.request
import pprint

number = input('追跡番号を入力:')
url = 'http://nanoappli.com/tracking/api/' + number + '.json'
res = urllib.request.urlopen(url)
data = json.loads(res.read().decode('utf-8'))

#最新のステータスを取得
newest = next(iter(reversed(data['statusList'])))
pprint.pprint(newest)
