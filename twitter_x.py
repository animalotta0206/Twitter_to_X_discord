import discord
import json
import datetime
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option

client = discord.Client()
#slash = SlashCommand(client, sync_commands=True)
slash = SlashCommand(client, sync_commands=False)

support_guild = '[サポートサーバーに参加する](https://discord.gg/pFgBSt6MPX)'
no_x = 'Twitter_to_X/no_x.json'
no_x_u = 'Twitter_to_X/no_x_u.json'

@slash.slash(name="stop_x", description="指定したチャンネルで、botが反応しないように設定します。")
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

@slash.slash(name="start_x", description="指定したチャンネルのbotの反応を再開します。")
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
    
client.run("MTE0MTM5MzAwNTUxMzgxMDA0MQ.GyZpN0.shro1p8KIR9PyQTRh-PmdPIGsMM1DmRDS55C0I")