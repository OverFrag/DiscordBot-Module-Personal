from discordbot.module import Module
import discord
import datetime


class UserMgmt(Module):
    name = 'discordbot-usermgmt'

    def __init__(self):
    	# At init i have to open the user.db-File if it's exist.
    	# Else i have to create the file and init the db 
        pass

    async def on_message(self, message: discord.Message):
        if self.is_my(message):
            return False

        if self.has_command('whoami', message):
            msg = [
            ]
            await self.container.client.send_message(message.channel, '\n'.join(msg))

        if self.has_command('iam', message):
            msg = [
            ]
            await self.container.client.send_message(message.channel, '\n'.join(msg))
