import nextcord, os, json
from nextcord.ext import commands
from dados import cargo

intents = nextcord.Intents.all()
intents.members = True

if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemplate = {"Token": "", "Prefix": "*"}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)
token = configData["Token"]
prefix = configData["Prefix"]

bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)

@bot.event
async def on_ready():
    await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Game(name='Bot Python'))
    print('Estou executando como {0.user}'.format(bot))
    
@bot.event
async def on_member_join(member):
    role = nextcord.utils.get(member.guild.roles, name=cargo)
    await member.add_roles(role)

for fn in os.listdir("./cogs"):
    if fn.endswith(".py"):
        bot.load_extension(f"cogs.{fn[:-3]}")


bot.run(token)