import json
import discord
from discord.ext import commands
from types import Config

class MyBot(commands.Bot):
    def __init__(self):
        # Carregar configurações
        with open('config.json', 'r') as f:
            self.config: Config = json.load(f)
        
        # Configurar intents corretamente
        intents = discord.Intents.default()
        intents.message_content = True  # Habilitar acesso ao conteúdo das mensagens
        intents.members = True  # Necessário para ver membros
        
        super().__init__(
            command_prefix=self.config['prefix'],
            intents=intents
        )

    async def setup_hook(self):
        await self.load_extension('cogs.prefixos')
        await self.load_extension('cogs.characters')

bot = MyBot()

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user} (ID: {bot.user.id})')
    print('------')

if __name__ == '__main__':
    bot.run(bot.config['token'])