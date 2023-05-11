import nextcord, io, os, asyncio
from nextcord.ext import application_checks, commands
from dados import canaldelogticket, cargo, aprovado, reprovado

class FichaView(nextcord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.canal_fichas_id = canaldelogticket
        self.response = None
        self.clicked = False

    @nextcord.ui.button(label="Criar ficha", style=nextcord.ButtonStyle.primary)
    async def criar_ficha(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        role = nextcord.utils.get(interaction.guild.roles, name=cargo)

        await interaction.response.defer()
        self.response = interaction.message

        await interaction.followup.send('Enviei as perguntas em sua DM para preservar sua privacidade!', ephemeral=True)

        dm_channel = await interaction.user.create_dm()

        def check(message):
            return message.author == interaction.user and message.channel == dm_channel

        await dm_channel.send('Qual é o seu Nome Completo (Player)?')
        nome2 = await self.bot.wait_for('message', check=check)

        idade2 = None
        while idade2 is None:
            await dm_channel.send('Qual é a sua Idade (Player)?')
            idade2_msg = await self.bot.wait_for('message', check=check)
            if idade2_msg.content.isdigit():
                idade2 = idade2_msg.content
            else:
                await dm_channel.send('Por favor, insira somente NUMEROS para a idade!!')

        await dm_channel.send('Qual é o seu Discord?')
        discord = await self.bot.wait_for('message', check=check)

        await dm_channel.send('Qual é sua Steam ID?')
        steam = await self.bot.wait_for('message', check=check)

        amigo_validas = ["Sim", "Não", "sim", "não", "S", "N", "nao"]
        amigo = None
        while amigo is None:
            await dm_channel.send('Você esta entrando em dupla com algum Campeão/Mago?')
            amigo_msg = await self.bot.wait_for('message', check=check)
            if amigo_msg.content.lower() in amigo_validas:
                amigo = amigo_msg.content.lower()
            else:
                await dm_channel.send('Por favor, insira uma resposta, sendo elas: SIM ou NÃO')

        await dm_channel.send('Qual é o Discord de seu amigo?')
        discorda = await self.bot.wait_for('message', check=check)
        
        await dm_channel.send('Qual é o Nome do seu personagem?')
        nome = await self.bot.wait_for('message', check=check)

        idade = None
        while idade is None:
            await dm_channel.send('Qual é a Idade do seu personagem?')
            idade_msg = await self.bot.wait_for('message', check=check)
            if idade_msg.content.isdigit():
                idade = idade_msg.content
            else:
                await dm_channel.send('Por favor, insira uma resposta valida para a idade do seu personagem.')

        await dm_channel.send('Qual é a Classe do seu personagem?')
        classe = await self.bot.wait_for('message', check=check)
        
        profissoes_validas = ["Alfaiate", "Alquimista", "Artesão", "Caçador", "Ferreiro", "Minerador", "Treinador", "alfaiate", "alquimista", "artesão", "caçador", "ferreiro", "minerador", "treinador"]
        profissao = None
        while profissao is None:
            await dm_channel.send('Qual é a Profissão do seu personagem?')
            profissao_msg = await self.bot.wait_for('message', check=check)
            if profissao_msg.content.lower() in profissoes_validas:
                profissao = profissao_msg.content.lower()
            else:
                await dm_channel.send('Por favor, insira uma resposta válida para a profissão do seu personagem. As profissões disponíveis são: Alfaiate, Alquimista, Artesão, Caçador, Ferreiro, Minerador e Treinador.')

        await dm_channel.send('Conte um pouco da história do seu personagem:')
        historia = await self.bot.wait_for('message', check=check)

        buffer = io.StringIO()
        buffer.write(f'Nome: {nome2.content}\n')
        buffer.write(f'Idade: {idade2}\n')
        buffer.write(f'Discord: {discord.content}\n')
        buffer.write(f'Steam ID: {steam.content}\n')
        buffer.write(f'Possui Amigo: {amigo}\n')
        buffer.write(f'Discord do Amigo: {discorda.content}\n')
        buffer.write(f'Nome Do Personagem: {nome.content}\n')
        buffer.write(f'Idade Do Personagem: {idade}\n')
        buffer.write(f'Classe: {classe.content}\n')
        buffer.write(f'Profissão: {profissao}\n')
        buffer.write(f'História: {historia.content}\n')

        with open(f'{nome.content}.txt', 'w') as f:
            f.write(buffer.getvalue())

            canal_fichas = self.bot.get_channel(self.canal_fichas_id)

        with open(f'{nome.content}.txt', 'rb') as f:
            ficha_file = nextcord.File(f)

            await canal_fichas.send(f'{role.mention} Ficha de {nome.content}:', file=ficha_file)
            await asyncio.sleep(1)
     
        os.remove(f'{nome.content}.txt')

        self.clicked = False
        await dm_channel.send(f'Sua ficha foi criada e enviada para {canal_fichas.mention}!')

        
class RPWL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name = 'ficha', description="Embed de ficha", default_member_permissions=8)
    @application_checks.has_permissions(administrator=True)
    async def ficha(self, interaction: nextcord.Interaction):
        view = FichaView(self.bot)
        em = nextcord.Embed(
            title='Sistema de suporte',
            description='Aqui você podera entra em contato com o suporte do servidor',
            colour=nextcord.Color.red()
        )
        em.set_image(url='https://cdn.discordapp.com/attachments/1062539072658219048/1063895217675182140/Akemi_an_island_seen_from_afar_with_smoke_rising_from_the_middl_3a2f32d7-0c89-42ca-8702-f30b4d9c4f17.png')
        await interaction.channel.send(embed=em)
        
        await interaction.channel.send(view=view)
        await interaction.response.send_message("Bem-sucedido", ephemeral=True)
    
    @nextcord.slash_command(name="aprovado", description="Comando para mandar a mensagem quando um player tiver a WL Aprovada")
    @commands.has_permissions(administrator=True)
    async def aprovado(self, ctx: nextcord.Interaction, member:nextcord.Member):
        
        canal = self.bot.get_channel(aprovado)

        await canal.send(f'Sua WL foi aprovada ✅! Seja muito bem vindo(a) {member.mention}\nFicamos muito felizes em ter você jogando conosco')
        await ctx.response.send_message(f"Mensagem enviada com sucesso para #{canal}", ephemeral=True)

    @nextcord.slash_command(name="reprovado", description="Comando para mandar a mensagem quando um player tiver a WL Reprovada")
    @commands.has_permissions(administrator=True)
    async def reprovado(self, ctx: nextcord.Interaction, member:nextcord.Member):
        
        canal = self.bot.get_channel(reprovado)

        await canal.send(f'Sua WL foi reprovada ❌ {member.mention}!\nMas nem tudo esta perdido, embreve a equipe da Staff abrira um Ticket para que você tenha uma segunda tentativa.')
        await ctx.response.send_message(f"Mensagem enviada com sucesso para #{canal}", ephemeral=True)


def setup(bot):
    bot.add_cog(RPWL(bot))
