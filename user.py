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

	def __init__(self):
		# At init i have to open the user.db-File if it's exist.
		# Else i have to create the file and init the db 
		db_file = '../../var/user.db'
		if not os.path.exists(db_file):
			file = open(db_file,'w')
			file.close()
			self.conn = sqlite3.connect(db_file)
			cursor = self.conn.cursor()
			cursor.execute('''CREATE TABLE user ( id CHAR(50) PRIMARY KEY NOT NULL, qlstat_id INT, twitch_account CHAR(50) )''')
			self.conn.commit()
		else:
			self.conn = sqlite3.connect(db_file)

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
				ql_id = str(user_data[1])
				req =urllib.request.urlopen('http://qlstats.net:8080/player/'+ql_id+'.json')
				data = json.loads(req.read().decode('utf-8'))
				roundKDR = ''
				msg = [
					'**QL-Stats**',
					'Nick : ' + data[0]['player']['nick'],
					'Last Played : ' + data[0]['overall_stats']['overall']['last_played_fuzzy'],
					'Kill-Death Ratio : ' + roundKDR,
					#'iFT - ELO : ',# + data[0]['elos']['ft']['b_r'].toString().split('.')[0] + ' **±** ',#+ data[0]['elos']['ft']['b_rd'].toString().split('.')[0],
					#'iCTF -ELO : ' + data[0]['elos']['ctf']['b_r'].toString().split('.')[0] + ' **±** '+ data[0]['elos']['ctf']['b_rd'].toString().split('.')[0],
					'Games played (Wins / Losses) : ' + str(data[0]['games_played']['overall']['games']) + ' (' + str(data[0]['games_played']['overall']['wins']) + '/' + str(data[0]['games_played']['overall']['losses'])  + ' )',
				]
			await self.container.client.send_message(message.channel, '\n'.join(msg))

		if self.has_command('iam', message):
			msg = [
			]
			await self.container.client.send_message(message.channel, '\n'.join(msg))
	def __get_user_by_id(self,disc_id):
		#SELECT * FROM user WHERE id=disc_id 
		cursor = self.conn.cursor()
		cursor.execute("SELECT * FROM user WHERE id='%s'" % disc_id)
		return cursor.fetchone()
	def __get_qlstats_by_id(self,ql_id):
		#
		pass
