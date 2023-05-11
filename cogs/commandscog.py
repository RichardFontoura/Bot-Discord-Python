import nextcord, asyncio
from nextcord.ext import commands

class commandscog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def avatar(self, ctx, *, user: nextcord.Member = None):
        if not user:
            user = ctx.message.author
        em = nextcord.Embed(title=str(user), color=0xAE0808)
        em.set_image(url=user.avatar.url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ping(self, ctx):
        embed=nextcord.Embed(title="Pong !!! 🏓", description=f"O Ping do servidor e:\n \n{round(self.bot.latency * 1000)} ms", color=0xFF5733)
        await ctx.send(embed=embed)

    @commands.command(name="limpar",description="Exclui mensagens",pass_context=True, usage="<Quantidade de mansagens que sera excluidas>")
    @commands.has_permissions(administrator=True)
    async def limpar(self, ctx, amount: int):        
      if amount > 1000 :
          message = await ctx.send('Não pode deletar mais de 1000 menssagens.')
          await asyncio.sleep(5)
          await message.delete()
      else:
          new_count = {}
          messages = await ctx.channel.history(limit=amount).flatten()
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
          await ctx.channel.purge(limit=amount+1)
          message = await ctx.send(f"Fora excuidas com sucesso `{deleted_messages} menssagens`\n\n{new_message}")
          await asyncio.sleep(5)
          await message.delete()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setnick(self, ctx, membro : nextcord.Member = None , *, nick = "by lobo"):
        if membro == None:
            await ctx.send("**❌ Você precisa mencionar alguem.**")
        else:
            await membro.edit(nick=nick)
            await ctx.send(f"**✅ Eu mudei o apelido {membro.name} para {nick}**")

    stop = False

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def spam(self, ctx, msg='.', *, amount=1):
        global stop
        stop = False
        i = 0
        while not stop and i < amount:
            await ctx.send(msg)
            i += 1

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def stop(self, ctx):
        global stop
        stop = True


def setup(bot):
    bot.add_cog(commandscog(bot))



















