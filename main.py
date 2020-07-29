#! /usr/bin/env python
# coding: 'utf-8'

import schedule
import datetime
import time
import os
import subprocess
import ast
from trackingctl import trackingctl

# 実行job関数
def job():
	#前のターン（？）のデータを比較用に取得（変数）
	with open('tasker') as f:
		status_b = f.read()

	#追跡データを文字列として取得
	trackingctl('2')
	with open('tasker') as g:
		status = g.read()

	#fとgを辞書に戻す（通知用）
	dicf = ast.literal_eval(status_b)
	dicg = ast.literal_eval(status)

	#件数に変動がない（追加や削除ではない）場合のみ通知
	if len(dicf) == len(dicg):

		#更新されたステータスを表示（あとで条件式考える）
		for dic, dic_b in zip(dicg, dicf):
			input_text = dic + '\n' + dicg[dic]['Date'] + '\n' + dicg[dic]['StatusDescription'] + '\n' + dicg[dic]['Details']
			input_text_b = dic_b + '\n' + dicf[dic_b]['Date'] + '\n' + dicf[dic_b]['StatusDescription'] + '\n' + dicf[dic_b]['Details']
			print('----')
			print(datetime.datetime.now())
			print(dicf[dic_b]['StatusDescription'])
			print(dicg[dic]['StatusDescription'])
			if dicg[dic]['StatusDescription'] == dicf[dic_b]['StatusDescription']:
				pass
			else:
				subprocess.run('termux-notification', shell=True, input=input_text, text=True)
				subprocess.run('termux-vibrate', shell=True, text=True)


#30分毎のjob実行を登録
schedule.every(10).minutes.do(job)

# jobの実行監視、指定時間になったらjob関数を実行
while True:
	schedule.run_pending()
	time.sleep(10)
