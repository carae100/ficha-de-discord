from discord.ext import commands

class PrefixosFichas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name='ficha')
    async def ficha(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("❌ Subcomando inválido!")
    
    @ficha.command(name='criar')
    async def criar(self, ctx, nome: str, ids_permitidos: str):
        if not self.is_master(ctx.author):
            return
        await ctx.invoke(self.bot.get_command('criar_ficha'), nome, ids_permitidos)
    
    @ficha.command(name='editar')
    async def editar(self, ctx, ficha: str, campo: str, *, valor: str):
        if not self.is_master(ctx.author):
            return
        await ctx.invoke(self.bot.get_command('editar_ficha'), ficha, campo, valor)
    
    @ficha.command(name='refresh')
    async def refresh(self, ctx):
        if not self.is_master(ctx.author):
            return
        await ctx.invoke(self.bot.get_command('refresh_geral'))
    
    @commands.command(name='desativar_bot')
    async def desativar(self, ctx):
        if not self.is_master(ctx.author):
            return
        await ctx.send("🛑 Bot sendo desativado...", delete_after=5)
        await self.bot.close()
    
    def is_master(self, user):
        return str(user.id) == str(self.bot.config['master_id'])

async def setup(bot):
    await bot.add_cog(PrefixosFichas(bot))