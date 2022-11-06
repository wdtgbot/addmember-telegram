#!/usr/bin/env python3

import sys
import os
import json
from datetime import datetime, timedelta

from telethon import sync, TelegramClient, events
from telethon.tl.types import InputPeerEmpty, UserStatusOffline, UserStatusRecently, UserStatusLastMonth, UserStatusLastWeek

from utils import *

with open('config.json', 'r', encoding='utf-8') as f:
	config = json.loads(f.read())

root_path = os.path.dirname(os.path.abspath(__file__))
folder_session = root_path + '/session/'
folder_data = root_path + '/data/'

accounts = config['accounts']

assert len(accounts) > 0

phone = accounts[0]
group_source = config['group_source']
group_target = config['group_target']
api_id = int(config['api_id'])
api_hash = config['api_hash']

client = TelegramClient(folder_session + phone, api_id, api_hash)
client.connect()
if not client.is_user_authorized():
	logging.error('Login fail, check first account ('+phone+'), need to run init_session')
	
else:
	# not need to join
	data = get_member_by_group_username(client, group_source)

	results = [] # list object member to save file

	today = datetime.now()
	last_week = today + timedelta(days=-7)
	last_month = today + timedelta(days=-30)
	for user in data:
		try:
			if not isinstance(user.username, type(None)):
				if str(user.username[-3:]).lower() == "bot":
					continue
				else:
					pass
			if isinstance(user.status, UserStatusRecently):
				date_online_str = 'online'
			else:
				if isinstance(user.status, UserStatusLastMonth):
					date_online = last_month
				if isinstance(user.status, UserStatusLastWeek):
					date_online = last_week
				if isinstance(user.status, UserStatusOffline):
					date_online = user.status.was_online

				date_online_str = date_online.strftime("%Y%m%d")
			tmp = {
				'user_id': user.id,
				'access_hash': user.access_hash,
				'username': user.username,
				"date_online": date_online_str
			}
			results.append(tmp)
		except BaseException:
			logging.error("Error get user")

	path_file = folder_data + str(group_source) + '.json'
	with open(path_file, 'w', encoding='utf-8') as f:
		json.dump(results, f, indent=4, ensure_ascii=False)
	client.disconnect()