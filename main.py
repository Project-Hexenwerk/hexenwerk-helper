import disnake
from disnake.ext import commands
import json
from enum import Enum
import bot_token
from disnake import TextInputStyle
import spell_embeds
import requests
from bs4 import BeautifulSoup
import re

spellslist = []
devtoollist = []

spell_request = requests.get('https://github.com/Project-Hexenwerk/hexenwerk-datapack/wiki/Spells')
spell_request = BeautifulSoup(spell_request.content, 'html.parser')

spell_h3s = spell_request.find_all('h3')
for spell_h3 in spell_h3s:
    if not "Pages 10" in spell_h3.text and not "Footer navigation" in spell_h3.text and not "\n" in spell_h3.text:
        spellslist.append(spell_h3.text.lower())
    print("Successfully scraped spells:" + str(spellslist))

devtool_request = requests.get('https://github.com/Project-Hexenwerk/hexenwerk-datapack/wiki/Developer-Features')
devtool_request = BeautifulSoup(devtool_request.content, 'html.parser')

devtool_h3s = devtool_request.find_all('h3')
for devtool_h3 in devtool_h3s:
    if not "Pages 10" in devtool_h3.text and not "Footer navigation" in devtool_h3.text and not "\n" in devtool_h3.text:
        devtoollist.append(devtool_h3.text.lower())
    print("Successfully scraped devtool:" + str(devtoollist))
          

bot = commands.Bot(
    command_prefix='!',
    sync_commands_debug=True,
    test_guilds = [1078622940561690665,911599951476314122]
)

### ON READY ###
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


### SLASH COMMANDS ###
# /HELP
@bot.slash_command(title="help",description="Shows all available bot commands")
async def help(inter: disnake.ApplicationCommandInteraction):
    
    embed = disnake.Embed(
        title="Help",
        description="</help:1078987304124813332>: Shows this message\n</invite:1078987304124813333>: Allows you to invite me to your server\n</bisect:1078990494408917002>: Shows information about Bisect Hosting",
        color=disnake.Colour.purple(),
    )
    await inter.response.send_message(embed=embed,ephemeral=True)

# /INVITE
@bot.slash_command(title="invite",description="Allows you to invite this bot to your server")
async def invite(inter: disnake.ApplicationCommandInteraction):
    embed = disnake.Embed(
        title="Invite",
        description="You can invite me to your server by clicking [here](https://discordapp.com/oauth2/authorize?&client_id=1078981768062976080&scope=bot&permissions=2734351710273) :D",
        color=disnake.Colour.purple(),
    )

    await inter.response.send_message(embed=embed,ephemeral=True)
    
# /BISECT
@bot.slash_command(title="bisect",description="Shows information about Bisect Hosting")
async def bisect(inter: disnake.ApplicationCommandInteraction):
    embed = disnake.Embed(
        title="Bisect Hosting",
        description="Bisect hosting is a minecraft server hosting company, offering minecraft servers for any of your needs at a cheap price! They offer full custom jar support and an amazing 24/7 support with an average response time of only 14 minutes. in case you ever need help setting anything up! \nGet 25% of your first month at Bisect Hosting by clicking [here](https://bisecthosting.com/flynecraft)!",
        color=disnake.Colour.purple(),
    )

    await inter.response.send_message(embed=embed,ephemeral=True)

# /SPELL
spell = commands.option_enum(spellslist)
@bot.slash_command(title="spell",description="Shows information about specific spells!")
async def spell(inter: disnake.ApplicationCommandInteraction, spell: spell):
        for spell_h3 in spell_h3s:
            if spell_h3.text.lower() == str(spell):
                p = spell_h3.find_next("p")
                img = spell_h3.find_next('img')
        
        spell_but_fancy = re.sub(r'\b[a-z]', lambda m: m.group().upper(),spell)

        embed = disnake.Embed(
            title = spell_but_fancy,
            description = p.text,
            color = disnake.Colour.purple()
        )

        if not spell == "custom":
            embed.set_thumbnail(url=img['src'])

        # embed.set_footer(
        #     text = ("https://github.com/Project-Hexenwerk/hexenwerk-datapack/wiki/Spells#" + str(spell.replace(" ","-").lower())),
        #     icon_url = "https://media.discordapp.net/attachments/1078640052386664488/1080131335936557056/github-mark-white1.png",
        # )

        await inter.response.send_message(embed = embed)

# /devtool
devtool = commands.option_enum(devtoollist)
@bot.slash_command(title="devtool",description="Shows information about specific spells!")
async def devtool(inter: disnake.ApplicationCommandInteraction, devtool: devtool):
        for devtool_h3 in devtool_h3s:
            if devtool_h3.text.lower() == str(devtool):
                p = devtool_h3.find_next("p")

        if not "hexenwerk." in devtool:
            print(devtool)
            print(devtool_h3.text.lower())
            devtool_name_but_fancy = re.sub(r'\b[a-z]', lambda m: m.group().upper(),devtool)
        else:
            devtool_name_but_fancy = devtool

        embed = disnake.Embed(
            title = devtool_name_but_fancy,
            description = p.text,
            color = disnake.Colour.purple()
        )

        await inter.response.send_message(embed = embed)

bot.run(bot_token.token)
