import discord
import json
import datetime
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option

Intents = discord.Intents.default()
Intents.members = True
client = discord.Client(intents=Intents)
#slash = SlashCommand(client, sync_commands=True)
slash = SlashCommand(client, sync_commands=False)

bot_master = 862605548389269525
support_guild = '[サポートサーバーに参加する](https://discord.gg/pFgBSt6MPX)'
no_x = 'Twitter_to_X/no_x.json'
no_x_u = 'Twitter_to_X/no_x_u.json'

@slash.slash(name="help", description="このbotのヘルプを表示します。")
async def help(ctx: SlashContext):
    user = client.get_user(bot_master)
    embed=discord.Embed(title="bot-help", description="コマンドの実行はスラッシュコマンドのみサポートされています。", color=0x00d5ff)
    embed.set_author(name="Twitterって言ったら𝕏って訂正してくるクソbot#6945", icon_url="https://cdn.discordapp.com/avatars/1141393005513810041/f44de0e5883a9812e440af18ccbd73e5.png?size=4096")
    embed.add_field(name="/stop_x", value="指定したチャンネルで、botが反応しないように設定します。", inline=True)
    embed.add_field(name="/start_x", value="指定したチャンネルで、botが反応しないように設定されている場合にその設定を解除することができます。", inline=True)
    embed.add_field(name="/stop_your_x", value="このコマンドを実行すると、コマンド実行者への反応を停止することができます。", inline=False)
    embed.add_field(name="/start_yor_x", value="このコマンドを実行すると、コマンド実行者への反応を再開することができます。", inline=True)
    embed.add_field(name="サポートサーバーのご案内", value="サポートサーバーでは、製作者に直接お問い合わせすることができます。\n[サポートサーバーに参加](https://discord.gg/pFgBSt6MPX)", inline=False)
    embed.set_footer(text=f"bot制作者「{user.display_name}」", icon_url=f"https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.png?size=1024")
    await ctx.send(embed=embed)

@slash.slash(name="get_setting_user", description="現在の設定状況を取得します。(個人設定)")
async def get_setting_user(ctx: SlashContext):
    with open(no_x_u, 'r') as f:
        check_d = json.load(f)
    if ctx.author.id in check_d:
        data1 = "True"
    else:
        data1 = "False"
    try:
        embed=discord.Embed(color=0x00e1ff)
        embed.set_author(name=f"{ctx.author.name}", icon_url=f"https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png?size=1024")
        embed.add_field(name="botの反応設定", value=f"`{data1}`", inline=True)
        embed.add_field(name="DevMode", value="`Flase`", inline=True)
        await ctx.author.send(content=f"<@{ctx.author.id}>さんの個人設定", embed=embed)
        await ctx.send("DMに個人設定の情報を送信しました。")
    except Exception as e:
        await ctx.send("DMの送信ができませんでした。")

@slash.slash(name="stop_x", description="指定したチャンネルで、botが反応しないように設定します。", options=[
    {
        "name":"channel",
        "description":"botの反応を停止するチャンネルを選択してください。",
        "type": 7,
        "required": True
    }])
async def twitter_url_to_x(ctx: SlashContext, channel: discord.TextChannel):
    if ctx.author.guild_permissions.administrator == False:
        await ctx.send("このコマンドの実行には管理者権限が必要になります。")
        return
    with open(no_x, 'r') as f:
        banlist = json.load(f)
    if channel.id in banlist:
        await ctx.send("指定したチャンネルは既に登録済みです。\n再開するにはコマンド`/start_x`を実行してください。")
        return
    banlist.append(channel.id)
    with open(no_x, 'w') as f:
        json.dump(banlist, f)
    embed=discord.Embed(color=0x006eff)
    embed.add_field(name="無効化したチャンネル", value=f"<#{channel.id}>", inline=False)
    await ctx.send("設定が完了しました。", embed=embed)

@slash.slash(name="start_x", description="指定したチャンネルのbotの反応を再開します。", options=[
    {
        "name":"channel",
        "description":"botの反応を再開するチャンネルを選択してください。",
        "type": 7,
         "required": True
    }])
async def start_x(ctx: SlashContext, channel: discord.TextChannel):
    if ctx.author.guild_permissions.administrator == False:
        await ctx.send("このコマンドの実行には管理者権限が必要になります。")
        return
    with open(no_x, 'r') as f:
        banlist = json.load(f)
        
    if channel.id in banlist:
        banlist.remove(channel.id)
        with open(no_x, 'w') as f:
            json.dump(banlist, f)
        embed=discord.Embed(color=0x006eff)
        embed.add_field(name="解除したチャンネル", value=f"<#{channel.id}>", inline=False)
        await ctx.send(f'設定が完了しました。', embed=embed)
    else:
        embed=discord.Embed(title="設定のヘルプ", color=0x11ff00)
        embed.add_field(name="botの発言権が正しく付与されていますか？", value="リストに登録されていない場合、botがそのチャンネルを見る・メッセージを送る権限を持っていない可能性があります。\n権限の確認をしてみてください。", inline=True)
        embed.add_field(name="それでも解決しない場合は…", value=f"サポートサーバーまでお願いします。\n{support_guild}", inline=True)
        await ctx.send(f'指定したチャンネルは、リストに登録されていませんでした。', embed=embed)
        pass

@slash.slash(name="stop_your_x", description="botがあなたへの反応を停止します。")
async def stop_your_x(ctx: SlashContext):
    user = ctx.author.id
    with open(no_x_u, 'r') as f:
        data = json.load(f)
    if user in data:
        await ctx.send("既に停止済みです！\n反応を再開をするにはコマンド`/start_your_x`を実行してください。")
        return
    data.append(user)
    with open(no_x_u, 'w') as f:
        json.dump(data, f)
    embed=discord.Embed(color=0x006eff)
    embed.add_field(name="設定内容", value=f"`True -> False`", inline=False)
    await ctx.send("設定が完了しました。", embed=embed)

@slash.slash(name="start_your_x", description="指定したチャンネルのbotの反応を再開します。")
async def start_your_x(ctx: SlashContext):
    with open(no_x_u, 'r') as f:
        banlist = json.load(f)
        user = ctx.author.id
        
    if user in banlist:
        banlist.remove(user)
        with open(no_x_u, 'w') as f:
            json.dump(banlist, f)
        embed=discord.Embed(color=0x006eff)
        embed.add_field(name="設定内容", value=f"`False -> True`", inline=False)
        await ctx.send(f'設定が完了しました。', embed=embed)
    else:
        embed=discord.Embed(title="設定のヘルプ", color=0x11ff00)
        embed.add_field(name="botの発言権が正しく付与されていますか？", value="リストに登録されていない場合、botがそのチャンネルを見る・メッセージを送る権限を持っていない可能性があります。\n 管理者の方に権限の確認を依頼してみてください。", inline=True)
        embed.add_field(name="それでも解決しない場合は…", value=f"サポートサーバーまでお願いします。\n{support_guild}", inline=True)
        await ctx.send(f'指定したチャンネルは、リストに登録されていませんでした。', embed=embed)
        pass

@client.event
async def on_message(message):
    if message.author.bot:
        return
    with open(no_x, 'r') as f:
        load_channel = json.load(f)
        channel_id = message.channel.id
    with open(no_x_u, 'r') as f:
        load_user = json.load(f)
        user_id = message.author.id
    if channel_id in load_channel or user_id in load_user:
        return
    if message.content.find("Twitter") != -1 or message.content.find("twitter") != -1 or message.content.find("ツイッター") != -1 or message.content.find("ついったー") != -1:
        await message.reply("<:x_twitter:1141394760637100032>")
        
    if message.content.find("リツイート") != -1 or message.content.find("りついーと") != -1:
        await message.reply("Re POST")
        return
    if message.content.find("Tweet") != -1 or message.content.find("tweet") != -1 or message.content.find("ツイート") != -1 or message.content.find("ついーと") != -1:
        await message.reply("X's")
    if message.content.startswith("Twitterバード") or message.content.startswith("ラリー・バード"):
        image_path = 'Twitter_to_X/RIP_Twitter.png'
        image = discord.File(image_path)
        await message.reply(content="## R.I.P", file=image)
    if message.content.find("https://x.com/") != -1:
        await message.add_reaction('<:x_twitter:1141394760637100032>')
    

#サーバーログ
@client.event
async def on_guild_join(guild):
    channel = client.get_channel(1141425601887076402)
    embed=discord.Embed(title="新規bot参加", description=f"Botが「{guild.name}」に参加しました。", color=0x00ffe1)
    embed.set_footer(text=f"GuildID:{guild.id}", icon_url=guild.icon_url)
    embed.timestamp = datetime.datetime.utcnow()
    await channel.send(embed=embed)

@client.event
async def on_ready():
    game = discord.Game(f'© 2023 𝕏 Corp.')
    await client.change_presence(status=discord.Status.online, activity=game)
    print('ログインしました')
    print('------')
    print(client.user.name)  # Botの名前
    print(discord.__version__)  # discord.pyのバージョン
    print('------')
    
client.run("YOUR TOKEN HERE")
