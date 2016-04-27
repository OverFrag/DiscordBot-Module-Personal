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
		cursor.execute('''CREATE TABLE IF NOT EXISTS module_user ( discord_id INT PRIMARY KEY NOT NULL, steam_id INT UNIQUE ,qlstat_id INT UNIQUE )''')
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
			switch_command = self.get_parameters('iam',message)
			if switch_command[0] == 'qlstats-id':
				try:
					ql_id = int(switch_command[1])
				except ValueError:
					msg = [
						'Your QL-Stats ID is not numeric'
					]
				else:
					if ql_id > 1000000:
						msg = [
							'Your Ql-Stats ID is out of range'
						]
					else:
						user_data = self.__get_user_by_id(message.author.id)
						cursor = self.container.db.cursor()
						if user_data == None:
							try:
								cursor.execute("INSERT INTO module_user (discord_id, qlstat_id) VALUES (?,?)" , (message.author.id,ql_id ) )
							except sqlite3.Error as e:
								msg = [
									"Error occured while updating userdata: "+str(e)
								]
							else:
								msg = [
									"Successfully stored your Data"
								]
						else:
							try:
								cursor.execute("UPDATE module_user SET qlstat_id=? WHERE discord_id="+message.author.id, ql_id)
							except sqlite3.Error as e:
								msg = [
									"Error occued while updating userdata: "+str(e)
								]
							else:
								msg = [
									"Successfully updated your data"
								]
				finally:
					await self.container.client.send_message(message.channel, '\n'.join(msg))

	def __get_user_by_id(self,disc_id):
		cursor = self.container.db.cursor()
		cursor.execute("SELECT * FROM module_user WHERE discord_id=?", disc_id)
		return cursor.fetchone()

	def __get_qlstats_by_id(self,ql_id):
		req =urllib.request.urlopen('http://qlstats.net:8080/player/'+str(ql_id)+'.json')
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