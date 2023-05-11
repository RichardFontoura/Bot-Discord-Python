import nextcord, datetime
from nextcord import Interaction, SlashOption, ChannelType, slash_command
from nextcord.ext import commands, application_checks
from dados import servidor

class slashcommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='criar_embed', description='Cria uma Embed.', guild_ids=[servidor])
    @application_checks.has_permissions(administrator=True)
    async def embed_create(self,
    ctx:Interaction,
    canal: nextcord.abc.GuildChannel = nextcord.SlashOption(channel_types=[ChannelType.text], name='canal', description='Selecione um canal', required=False),
    autor: str = nextcord.SlashOption(name='autor', description='Diz o autor da mensagem', required=False),
    icone_do_autor: nextcord.Attachment = nextcord.SlashOption(name='icone_do_autor', description='Selecione uma imagem para icone', required=False),
    icone_do_autor_url: str = nextcord.SlashOption(name='icone_do_autor_url', description='Selecione um link para a imagem para o icone', required=False),
    titulo: str = nextcord.SlashOption(name='titulo', description='Diz o titulo da embed', required=False),
    descrição: str = nextcord.SlashOption(name='descrição', description='Diz o texto da embed', required=False),
    rodapé: str = nextcord.SlashOption(name='rodapé', description='Diz o rodapé', required=False),
    icone_de_rodapé: nextcord.Attachment = nextcord.SlashOption(name='icone_de_rodapé', description='Selecione uma imagem para o rodapé', required=False),
    icone_de_rodapé_url: str = nextcord.SlashOption(name='icone_de_rodapé_url', description='Selecione um link para a imagem para o rodapé', required=False),
    imagem: nextcord.Attachment = nextcord.SlashOption(name='imagem', description='Selecione uma imagem',  required=False),
    imagem_url: str = nextcord.SlashOption(name='imagem_url', description='Selecione o link de uma imagem',  required=False),
    thumbnail: nextcord.Attachment = nextcord.SlashOption(name='thumbnail', description='Selecione uma imagem para a thumbnail', required=False),
    thumbnail_url: str = nextcord.SlashOption(name='thumbnail_url', description='Selecione o link de uma imagem para a thumbnail', required=False),
    cor: str = nextcord.SlashOption(name='cor', description='Diga uma cor no formato Hex', required=False),
    ):

        embed = nextcord.Embed()
        if not canal:
            canal = ctx.channel

        if autor is not None and icone_do_autor is not None:
            embed.set_author(name=autor, icon_url=icone_do_autor)
        elif autor is not None and icone_do_autor is None:
            embed.set_author(name=autor)
        elif autor is None and icone_do_autor is not None:
            pass
        if autor is not None and icone_do_autor_url is not None:
            embed.set_author(name=autor, icon_url=icone_do_autor_url)
        elif autor is not None and icone_do_autor_url is None:
            embed.set_author(name=autor)
        elif autor is None and icone_do_autor_url is not None:
            pass
        if titulo:
            embed.title=titulo
        if descrição:
            embed.description=descrição
        if icone_de_rodapé is not None and icone_de_rodapé is not None:
            embed.set_footer(text=rodapé, icon_url=icone_de_rodapé)
        elif rodapé is not None and icone_de_rodapé is None:
            embed.set_footer(text=rodapé)
        elif rodapé is None and icone_de_rodapé is not None:
            pass
        if icone_de_rodapé_url is not None and icone_de_rodapé_url is not None:
            embed.set_footer(text=rodapé, icon_url=icone_de_rodapé_url)
        elif rodapé is not None and icone_de_rodapé_url is None:
            embed.set_footer(text=rodapé)
        elif rodapé is None and icone_de_rodapé_url is not None:
            pass
        if imagem:
            embed.set_image(url=imagem)
        if imagem_url:
            embed.set_image(url=imagem_url)
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        if thumbnail_url:
            embed.set_thumbnail(url=thumbnail_url)
        if cor:
            embed.colour=int("0x" + cor, 16)
        if not autor and not titulo and not descrição and not rodapé and not thumbnail and not thumbnail_url and not cor:
            await ctx.response.send_message("Por favor insira um comando valido !!!", ephemeral=True)
        else:
            await canal.send(embed=embed)
            await ctx.response.send_message(f"Embed enviada para #{canal}", ephemeral=True)


    @nextcord.slash_command(name="excluir", description="Exclui mensagens")
    @application_checks.has_guild_permissions(administrator=True)
    async def excluir(self, interaction: nextcord.Interaction, quantidade: int = SlashOption(name="quantidade", description="Diga a quantidade de mensagens")):
        if quantidade > 1000:
            await interaction.response.send_message('Não posso excluir mais de 1000 mensagens', ephemeral=True)
        else:
            new_count = {}
            messages = await interaction.channel.history(limit=quantidade).flatten()
            for message in messages:
                if str(message.author) in new_count:
                    new_count[str(message.author)] += 1
                else:
                    new_count[str(message.author)] = 1

            deleted_messages = 0
            new_string = []
            for author, message_deleted in list(new_count.items()):
                new_string.append(f"**{author}**: {message_deleted}")
                deleted_messages += message_deleted
            new_message = '\n'.join(new_string)
            await interaction.channel.purge(limit=quantidade)
            await interaction.response.send_message(f"Foram excluidas `{deleted_messages} mensagens`\n\n{new_message}", ephemeral=True)


    @nextcord.slash_command(name="ban", description="Da ban em um membro.")
    @application_checks.has_permissions(administrator=True)
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx: Interaction, member: nextcord.Member, reason="Nenhuma razão dada"):
        await member.ban(reason=reason)
        embed=nextcord.Embed(color=nextcord.Color.green())
        embed.add_field(name="Membro banido.", value=f"Motivo: {reason}")
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text = "Monika-tan", icon_url = "https://cdn.discordapp.com/avatars/1067061035527327835/cc224e27f3c3f514171828c378e64cc4.png?size=1024")
        await ctx.send(embed=embed)
        print("Commando executado com sucesso.")

    @ban.error
    async def banerror(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Por favor, preencha todos os argumentos necessários!")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Você não tem as permissões necessárias para executar este comando!")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("Membro não encontrado!")

    @nextcord.slash_command(name="kick", description="Expulsa um membro.")
    @application_checks.has_permissions(administrator=True)
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx: Interaction, member: nextcord.Member, reason="Nenhuma razão dada"):
        await member.kick(reason=reason)
        embed=nextcord.Embed(color=nextcord.Color.green())
        embed.add_field(name="Membro expulso.", value=f"Motivo: {reason}", inline=False)
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text = "Monika-tan", icon_url = "https://cdn.discordapp.com/avatars/1067061035527327835/cc224e27f3c3f514171828c378e64cc4.png?size=1024")
        await ctx.send(embed=embed)
        print("Commando executado com sucesso.")

    @kick.error
    async def kickerror(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Por favor, preencha todos os argumentos necessários!")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Você não tem as permissões necessárias para executar este comando!")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("Membro não encontrado!")


    @nextcord.slash_command(name='nick', description='Troca o nick do usuario.')
    @commands.has_permissions(administrator=True)
    async def setnick(self, ctx, member : nextcord.Member = None , *, nick = "by lobo"):
        if member == None:
            await ctx.send("**❌ Você precisa mencionar alguem**")
        else:
            await member.edit(nick=nick)
            await ctx.send(f"✅ Eu mudei o apelido {member.name} para {nick}")


    @nextcord.slash_command(name='spam', description='Começa o spam de mensagens')
    @commands.has_permissions(administrator=True)
    async def spam(self, interaction: nextcord.Interaction,
    mensagem: str = SlashOption(name='mensagem', description='Diga qual mensagem deseja Spam'), 
    quantidade: int = SlashOption(name="quantidade", description="Diga a quantidade de mensagens")
    ):
        msg=mensagem
        amount=quantidade
        global stop
        stop = False
        i = 0
        while not stop and i < amount:
            await interaction.send(msg)
            i += 1
            
    @nextcord.slash_command(name='stop_spam', description='Termina com o spam de mensagens')
    @commands.has_permissions(administrator=True)
    async def stop(self, interaction):
        global stop
        stop = True
        await interaction.send('Spam parado com sucesso', ephemeral=True)

    @nextcord.slash_command(name='eco', description='Diz algo usando o bot')
    @commands.has_permissions(administrator=True)
    async def eco(self, ctx: nextcord.Interaction,
    msg: str = SlashOption(name='mensagem', description='Diga a mensagem que quer enviar')
    ):

        await ctx.channel.send(msg)
        await ctx.response.send_message("Mensagem enviada", ephemeral=True)

    
def setup(bot):
    bot.add_cog(slashcommands(bot))
