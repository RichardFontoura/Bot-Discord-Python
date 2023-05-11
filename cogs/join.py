import nextcord, datetime 
from nextcord.ext import commands
from dados import boasvindas
from dados import saida

class join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel=self.bot.get_channel(boasvindas)
        user=member
        em=nextcord.Embed(title="Bem vindo sobrevivente !!!", 
        description=f"{member.mention} entrou no servidor.", 
        color = nextcord.Color.from_rgb(255,192,203))
        em.set_thumbnail(url=user.avatar.url)
        em.timestamp = datetime.datetime.now()
        em.set_footer(text = "#", icon_url = "https://cdn.discordapp.com/avatars/1067061035527327835/cc224e27f3c3f514171828c378e64cc4.png?size=1024")
        await channel.send(embed=em)

        embe = nextcord.Embed(title=f'Seja muito bem vindo a {member.guild.name} !!!', 
        description='Não se esqueça de ler as nossas regras, respeitar os outros membros e o mais importante... Divirta-se !!!',
        color=nextcord.Color.from_rgb(255,192,203))
        embe.set_thumbnail(url='https://cdn.discordapp.com/attachments/861233300789657621/1068742721755426876/59d0856c4fe47d6843c1d34bc98d6920.jpg')
        embe.timestamp = datetime.datetime.now()
        embe.set_footer(text = "#", icon_url = "https://cdn.discordapp.com/avatars/1067061035527327835/cc224e27f3c3f514171828c378e64cc4.png?size=1024")
        await member.send(embed=embe)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel=self.bot.get_channel(saida)
        em=nextcord.Embed(title=f"{member.display_name} saiu do servidor {member.guild.name}",
        color = nextcord.Color.from_rgb(54, 192, 231))
        await channel.send(embed=em)
         

def setup(bot):
    bot.add_cog(join(bot))