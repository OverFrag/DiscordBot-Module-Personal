from discordbot.module import Module
import discord
import datetime


class UserMgmt(Module):
    name = 'discordbot-usermgmt'

    def __init__(self):
    	# At init i have to open the user.db-File if it's exist.
    	# Else i have to create the file and init the db 
    	db_file = '../../var/user.db'
        pass

    async def on_message(self, message: discord.Message):
        if self.is_my(message):
            return False

        if self.has_command('whoami', message):
            user_data = self.get_user_by_id(message.author.id)
            msg = [
            ]
            await self.container.client.send_message(message.channel, '\n'.join(msg))

        if self.has_command('iam', message):
            user_data = self.get_user_by_id(message.author.id)
            msg = [
            ]
            await self.container.client.send_message(message.channel, '\n'.join(msg))
    def get_user_by_id(self,disc_id):
        #SELECT * FROM user WHERE id=disc_id 
        pass
    def get_qlstats_by_id(self,ql_id):
        #
        pass
