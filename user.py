from discordbot.module import Module
import discord
import datetime

import sys
import os
import sqlite3
import urllib.request
import json


class UserMgmt(Module):
	name = 'discordbot-usermgmt'

	def bot(self):
		#Create if not exist user-table
		cursor = self.container.db.cursor()
		cursor.execute('''CREATE TABLE IF NOT EXISTS user ( id CHAR(50) PRIMARY KEY NOT NULL, qlstat_id INT, twitch_account CHAR(50) )''')
		self.container.db.commit()

	async def on_message(self, message: discord.Message):
		if self.is_my(message):
			return False

		user_data = self.__get_user_by_id(message.author.id)

		if self.has_command('whoami', message):
			if user_data == None:
				msg = [
					'Cannot find any data, please use !help for more information'
				]
			else:
				msg = self.__get_qlstats_by_id(user_data[1])
			await self.container.client.send_message(message.channel, '\n'.join(msg))

		if self.has_command('iam', message):
			msg = [
			]
			await self.container.client.send_message(message.channel, '\n'.join(msg))

	def __get_user_by_id(self,disc_id):
		cursor = self.container.db.cursor()
		cursor.execute("SELECT * FROM user WHERE id='%s'" % disc_id)
		return cursor.fetchone()

	def __get_qlstats_by_id(self,ql_id):
		req =urllib.request.urlopen('http://qlstats.net:8080/player/'+ql_id+'.json')
		data = json.loads(req.read().decode('utf-8'))
		#print(data)
		roundKDR = str(round(data[0]['overall_stats']['overall']['k_d_ratio'],3))
		try:
			ift_elo = 'iFT - ELO : '+str(int(data[0]['elos']['ft']['b_r']))+' **±** '+ str(int(data[0]['elos']['ft']['b_rd']))
		except KeyError:
			ift_elo = 'iFT - ELO : No data available'
		try:
			ictf_elo = 'iCTF - ELO : '+str(int(data[0]['elos']['ctf']['b_r']))+' **±**'+ str(int(data[0]['elos']['ctf']['b_rd']))
		except:
			ictf_elo = 'iCTF - ELO : No data available'
		msg = [
			'**QL-Stats**',
			'Nick : ' + data[0]['player']['nick'],
			'Last Played : ' + data[0]['overall_stats']['overall']['last_played_fuzzy'],
			'Kill-Death Ratio : ' + roundKDR,
			ift_elo,
			ictf_elo,
			'Games played (Wins / Losses) : ' + str(data[0]['games_played']['overall']['games']) + ' (' + str(data[0]['games_played']['overall']['wins']) + '/' + str(data[0]['games_played']['overall']['losses'])  + ' )',
		]
		return msg