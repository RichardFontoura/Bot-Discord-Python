import nextcord, os, datetime, pytz
from nextcord.ext import commands
from nextcord.ui import View
from dados import categoriaticket, canaldelogticket

class View(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="Criar Ticket", style=nextcord.ButtonStyle.blurple, custom_id="view_1234"
    )
    async def create(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        c = interaction.guild.get_channel(categoriaticket)
        t = await c.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            overwrites={
                interaction.guild.default_role: nextcord.PermissionOverwrite(view_channel=False),
                interaction.user: nextcord.PermissionOverwrite(view_channel=True)
            }
        )
        em = nextcord.Embed(
            title="Ticket",
            description="Este é o seu ticket."
        )
        await t.send(content=f"{interaction.user.mention}", embed=em, view=Edit())

        await interaction.response.send_message(f"Ticket está {t.mention} criado", ephemeral=True)

    @nextcord.ui.button(
        label="Abrir Ticket de Suporte", style=nextcord.ButtonStyle.green, custom_id="support"
    )
    async def support(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        c = interaction.guild.get_channel(categoriaticket)
        t = await c.create_text_channel(
            name=f"support-{interaction.user.name}",
            overwrites={
                interaction.guild.default_role: nextcord.PermissionOverwrite(view_channel=False),
                interaction.user: nextcord.PermissionOverwrite(view_channel=True)
            }
        )
        em = nextcord.Embed(
            title="Ticket de Suporte",
            description="Este é o seu ticket de suporte."
        )
        await t.send(content=f"{interaction.user.mention}", embed=em, view=Edit())

        await interaction.response.send_message(f"Ticket de suporte está {t.mention} criado", ephemeral=True)

    @nextcord.ui.button(
        label="Abrir Ticket de Bug", style=nextcord.ButtonStyle.red, custom_id="bug"
    )
    async def bug(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        c = interaction.guild.get_channel(categoriaticket)
        t = await c.create_text_channel(
            name=f"bug-{interaction.user.name}",
            overwrites={
                interaction.guild.default_role: nextcord.PermissionOverwrite(view_channel=False),
                interaction.user: nextcord.PermissionOverwrite(view_channel=True)
            }
        )
        em = nextcord.Embed(
            title="Ticket de Bug",
            description="Este é o seu ticket de bug."
        )
        await t.send(content=f"{interaction.user.mention}", embed=em, view=Edit())

        await interaction.response.send_message(f"Ticket de bug está {t.mention} criado", ephemeral=True)


class Edit(nextcord.ui.View):
    def __init__(self, log_channel_id=canaldelogticket, log_file_name="log.txt"):
        super().__init__(timeout=None)
        self.log_channel_id = log_channel_id
        self.log_file_name = log_file_name

        self.brazil_tz = pytz.timezone('America/Sao_Paulo')

    @nextcord.ui.button(
        label="Fechar Ticket", style=nextcord.ButtonStyle.danger, custom_id="view_12345"
    )
    async def create(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message(f"O Ticket está sendo fechado...", ephemeral=True)
        
        messages = await interaction.channel.history().flatten()
        
        now = datetime.datetime.now(self.brazil_tz)
        
        log_file = open(self.log_file_name, "a")
        log_file.write(f"Mensagens do ticket #{interaction.channel.name} ({now.strftime('%Y-%m-%d %H:%M:%S')})\n")
        for message in messages:
        
            if message.author.bot:
                continue
            
            log_file.write(f"[{message.created_at.astimezone(self.brazil_tz).strftime('%Y-%m-%d %H:%M:%S')}] {message.author.name}: {message.content}\n")
        log_file.close()

        log_channel = interaction.guild.get_channel(self.log_channel_id)
        if log_channel:
            with open(self.log_file_name, "rb") as log_file:
                await log_channel.send(file=nextcord.File(log_file, self.log_file_name))

        await interaction.channel.delete()
        os.remove(self.log_file_name)


class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(View())
        self.bot.add_view(Edit())
    
    @nextcord.slash_command(name = 'setup3', description="Ticket Setup", default_member_permissions=8)
    async def setup3(self, interaction: nextcord.Interaction):
        em = nextcord.Embed(
            title='Sistema de suporte',
            description='Aqui você podera entra em contato com o suporte do servidor',
            colour=nextcord.Color.red()
        )
        em.set_author(name='Lobo', icon_url='https://cdn.discordapp.com/attachments/1062539072658219048/1063895217675182140/Akemi_an_island_seen_from_afar_with_smoke_rising_from_the_middl_3a2f32d7-0c89-42ca-8702-f30b4d9c4f17.png')
        em.set_image(url='https://cdn.discordapp.com/attachments/1062539072658219048/1063895217675182140/Akemi_an_island_seen_from_afar_with_smoke_rising_from_the_middl_3a2f32d7-0c89-42ca-8702-f30b4d9c4f17.png')
        em.set_footer(text='WereWolf ticket suporte', icon_url='https://cdn.discordapp.com/avatars/788525047361961995/5549112f45bdacf7dee52ab98e9c7d67.png?size=1024')
        em.set_thumbnail(url='https://cdn.discordapp.com/attachments/1062539072658219048/1063895217675182140/Akemi_an_island_seen_from_afar_with_smoke_rising_from_the_middl_3a2f32d7-0c89-42ca-8702-f30b4d9c4f17.png')
        await interaction.channel.send(embed=em)
        
        await interaction.channel.send(view=View())
        await interaction.response.send_message("Bem-sucedido", ephemeral=True)
     
def setup(bot):
    bot.add_cog(Ticket(bot))