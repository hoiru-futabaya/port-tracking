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

#関数trackingctl(mode=a, carrier=b, number=c)という形式で指定。modeが2の場合残り2つの引数は指定しない

def trackingctl(mode, carrier ='', number = ''):

	if mode  == '1':
		#登録画面

		#trackingmoreから情報取得
		urlStr = ''
		requestData ="{\"tracking_number\": \"" + number + "\",\"carrier_code\":\"" + carrierjp[carrier] + "\"}"
		result = tracker.trackingmore(requestData, urlStr, "post")

		#追跡中の荷物を辞書で持っておく（運送会社: 伝票番号）
		trklist[number] = carrier
		with open('trklist', mode='w') as f:
			f.write(str(trklist))

		return result

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
		urlStr = "/" + carrierjp[carrier] + "/" + number
		requestData = ""
		result = tracker.trackingmore(requestData, urlStr, "codeNumberDelete")

		#辞書からも削除（運送会社: 伝票番号）
		trklist.pop(number)
		with open('trklist', mode='w') as f:
			f.write(str(trklist))

		return result
