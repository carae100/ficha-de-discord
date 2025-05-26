import json
import discord
import re
from pathlib import Path
from discord.ext import commands
from typing import Dict, List, Any, Union
from .types import Config, Ficha, Efeito, DadosFicha

class SistemaFichas(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.config: Config = bot.config
        self.characters_dir: Path = Path('data/characters')
        self.characters_dir.mkdir(parents=True, exist_ok=True)

    # ========== MÉTODOS PRINCIPAIS ==========
    async def criar_ficha(self, ctx: commands.Context, nome: str, ids_permitidos: str) -> None:
        """Cria nova ficha com verificação completa"""
        try:
            # Verificação de permissões
            if not await self.verificar_mestre(ctx):
                return

            # Criar estrutura inicial
            categoria = await self.get_categoria(ctx.guild)
            canal = await self.criar_canal_ficha(ctx.guild, nome, categoria)
            dados = self.construir_dados_iniciais(nome, canal.id, ids_permitidos)

            # Salvar e confirmar
            self.salvar_ficha(dados['id'], dados)
            await self.enviar_confirmacao(ctx, canal, dados['id'])
            
        except Exception as e:
            await self.tratar_erro(ctx, e)

    # ========== SISTEMA DE BUFFS ==========
    def calcular_escalonavel(
        self, 
        valor: List[Union[List[Union[str, float]], float]], 
        recursos: Dict[str, Dict[str, float]]
    ) -> float:
        """Tipos 5-8: Efeitos escalonáveis (implementação completa)"""
        recursos_limites = valor[:-1]
        valor_max = valor[-1]
        intensidades: List[float] = []

        for recurso_limite in recursos_limites:
            recurso, limite = recurso_limite
            r = recursos[recurso]
            
            if r['max'] <= 0:
                intensidade = 0.0
            else:
                proporcao = r['atual'] / r['max']
                intensidade = self.calcular_intensidade(limite, proporcao)
                
            intensidades.append(intensidade)
            
        return valor_max * (sum(intensidades) / len(intensidades))

    # ========== MÉTODOS AUXILIARES ==========
    async def get_categoria(self, guild: discord.Guild) -> discord.CategoryChannel:
        """Obtém ou cria a categoria de fichas"""
        return discord.utils.get(guild.categories, name=self.config['channel_category']) or \
            await guild.create_category(self.config['channel_category'])

    def construir_dados_iniciais(
        self, 
        nome: str, 
        channel_id: int, 
        ids_permitidos: str
    ) -> Ficha:
        """Constrói a estrutura completa da ficha"""
        with open('data/templates/default_ficha.json', 'r', encoding='utf-8') as f:
            template: Ficha = json.load(f)
            
        return {
            **template,
            "id": self.gerar_id(nome),
            "nome": nome,
            "channel_id": str(channel_id),
            "permissoes": self.processar_ids(ids_permitidos)
        }

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SistemaFichas(bot))