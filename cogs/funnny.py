import nextcord, random
from nextcord import Interaction
from nextcord.ext import commands
from dados import servidor

class funnny(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name = 'xique', description = 'Teste de comandos', guild_ids=[servidor])
    async def xique(self, interaction: nextcord.Interaction):
        await interaction.response.send_message('Xique de cria')

    @nextcord.slash_command(name = 'avatar', description = 'Rouba o avatar do seu amiguinho', guild_ids=[servidor])
    async def avatar(self, interaction:nextcord.Interaction, user: nextcord.Member = None):
        if not user:
            user = interaction.message.author
        em = nextcord.Embed(title=str(user), color=0xAE0808)
        em.set_image(url=user.avatar.url)
        await interaction.send(embed=em)

    @nextcord.slash_command(name='sigma', description='🍷🗿', guild_ids=[servidor])
    async def sigma(self, ctx: nextcord.Interaction,):
        em = nextcord.Embed(title='🍷🗿', color=nextcord.Color.from_rgb(0,0,255))
        em.set_image(url='https://media.tenor.com/qOI3iBvktYcAAAAd/giga-chad.gif')

        await ctx.send(embed=em)

    @nextcord.slash_command(name='sonhar', description='Eles tão deixando a gente sonhar', guild_ids=[servidor])
    async def sonhar(self, ctx: nextcord.Interaction):
        em = nextcord.Embed(color=nextcord.Color.from_rgb(0,0,255))
        em.set_image(url='https://cdn.discordapp.com/attachments/1067244075746611232/1070111649761087589/ronaldinho-gaucho.gif')

        await ctx.send(embed=em)

    @nextcord.slash_command(name='hashashin', description='🥷', guild_ids=[servidor])
    async def hashashin(self, ctx: nextcord.Interaction):
        em = nextcord.Embed(color=nextcord.Color.from_rgb(0,0,255))
        em.set_image(url='https://cdn.discordapp.com/attachments/1067244075746611232/1070111576989900830/assassins-creed-revelation.gif')

        await ctx.channel.send(embed=em)
        await ctx.response.send_message("Hiden one", ephemeral=True)

    @nextcord.slash_command(name= 'love', description='Quer namorar comigo?')
    async def love(self,ctx:Interaction, membro:nextcord.Member):
        embed = nextcord.Embed(
            description=f'{ctx.user.mention} quer namorar com {membro.mention}',
            color= 0xc6c6f5
        )
        embed.set_image(url='https://media.tenor.com/h9UfXaa2JsEAAAAC/ronaldinho-quer-namorar-comigo.gif')

        await ctx.send(embed=embed)

    @nextcord.slash_command(name= 'f', description='💜 Pressione F para prestar seu respeito')
    async def f(self,ctx:Interaction, membro:nextcord.Member):
        hearts = ['❤', '💛', '💚', '💙', '💜']

        embed = nextcord.Embed(
            title=f'Press **F**',
            description=f'{ctx.user.mention} Prestou o seu respeito a {membro.mention} {random.choice(hearts)}',
            color= 0xc6c6f5
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(funnny(bot))
