#! /usr/bin/env python
# coding: 'utf-8'

import json
import urllib.request
import pprint
import trackingmoreclass
import os
import io,sys,ast

tracker = trackingmoreclass.track
result = ""
tasker = {}

with open('trklist') as f:\
	trklist = ast.literal_eval(f.read())

#trackingmoreの登録業者辞書（名前: code）
carrierjp = {'日本郵便': 'japan-post', '日通': 'nippon', 'クロネコヤマト': 'taqbin-jp', '佐川急便': 'sagawa'}

#↑のキーと値を入れ替えた辞書も作っておく
carrierR = {'japan-post': '日本郵便', 'nippon': '日通', 'taqbin-jp': 'クロネコヤマト', 'sagawa': '佐川急便'}

#インタプリタの引数で直接追跡モードに入る
if len(sys.argv) > 1:
	mode = '2'

else:
	#モード選択
	print('【登録 → 1　追跡 → 2　削除 → 3】')
	mode = input('>>')

if mode == '1':
	#登録画面
	print('【追跡する荷物の登録】')
	carrier = input('運送会社を入力: ')
	number = input('伝票番号を入力: ')

	#trackingmoreから情報取得
	urlStr = ''
	requestData ="{\"tracking_number\": \"" + number + "\",\"carrier_code\":\"" + carrierjp[carrier] + "\"}"
	result = tracker.trackingmore(requestData, urlStr, "post")

	#追跡中の荷物を辞書で持っておく（運送会社: 伝票番号）
	trklist[number] = carrier
	with open('trklist', mode='w') as f:
		f.write(str(trklist))
	print(result)

elif mode == '2':
	#追跡リストを表示
	for i in trklist:
		j = trklist[i]
		urlStr = "/" + carrierjp[j] + "/" + i
		requestData = ""
		result = tracker.trackingmore(requestData, urlStr, "codeNumberGet")
#		ast.literal_eval(result)
		title = '【' + j + ': ' + i + '】'
		print(title)
		track = next(iter(json.loads(result)['data']['origin_info']['trackinfo']))
		pprint.pprint(track)
		tasker[title] = track

	with open('tasker', mode='w') as f:
		f.write(str(tasker))


elif mode == '3':
	#削除対象を入力
	print('【リストから荷物を削除】')
	carrier = input('運送会社を入力: ')
	number = input('伝票番号を入力: ')
	urlStr = "/" + carrierjp[carrier] + "/" + number
	requestData = ""
	result = tracker.trackingmore(requestData, urlStr, "codeNumberDelete")

	#辞書からも削除（運送会社: 伝票番号）
	trklist.pop(number)
	with open('trklist', mode='w') as f:
		f.write(str(trklist))

	print(result)

