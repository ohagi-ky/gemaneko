# インストールしたdiscord.pyを読み込む
import discord
import config

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

# 接続に必要なオブジェクトを生成する
client = discord.Client(intents=intents)

game_directory = {}

# 起動時の処理
@client.event
async def on_ready(): 
    print('ログインしました')

# サーバーに参加したときの処理
@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send("ゲーム参加者管理Botの **ゲマネコ** ですにゃ🎮\nよろしくにゃ！\n/helpで使い方を教えるにゃ！")
            break


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):

    # メッセージ送信者がBotだった場合にスルーする
    if message.author.bot:
        return
    
    # /helpコマンドの処理(ヘルプメッセージの表示)
    if message.content.startswith('/help'):
        await message.channel.send(
            '/list - 登録されているゲームの一覧を表示するにゃ\n'
            '/add <ゲーム名> - ゲームを登録するにゃ\n'
            '/remove <ゲーム名> - ゲームを削除するにゃ\n'
            '/join <ゲーム名> - ゲームに参加するにゃ\n'
            '/leave <ゲーム名> - ゲームから離脱するにゃ\n'
            '/clear <ゲーム名> - ゲームの参加者を全員削除するにゃ\n'
            '/status <ゲーム名> - ゲームの参加者一覧を表示するにゃ\n'
            '/start <ゲーム名> - ゲームを開始して参加者を全員削除するにゃ\n'
            '/help - ヘルプメッセージを表示するにゃ'
        )
        return
    # /listコマンドの処理(登録ゲーム一覧の表示)
    if message.content.startswith('/list'):
        if not game_directory:
            await message.channel.send('登録されているゲームはないにゃ')
            return
        response = '登録されているゲームは\n' + '\n'.join(game_directory.keys()) + '\nにゃ'
        await message.channel.send(response)
        return
    
    if message.content.startswith('/staff'):
        await message.channel.send('"ゲマネコ"をご利用いただきありがとうございます！OhaGiです！\n皆さんのゲームライフがより楽しくなることを願っていおります！')
        return

    if message.content.startswith('/にゃ'):
        await message.channel.send('にゃ～🐾')
        return

    # メッセージがコマンドでない場合はスルーする
    if len(message.content.split()) != 2:
        await message.channel.send('メッセージの形式が正しくないにゃ')
        return
    
    # メッセージが正しい場合の処理
    else:
        # ユーザーのメッセージの前半部分(コマンド)を取得する
        user_command = message.content.split()[0].lower()
        # ユーザーのメッセージの後半部分(ゲーム名)を取得する
        game_name = message.content.split()[1].lower()

        match (user_command):

            #　/addコマンドの処理(ゲームをgame_directoryに追加)
            case ('/add'):            
                if game_name in game_directory:
                    await message.channel.send(f'{game_name}はすでに登録されているにゃ')
                    return
                game_directory[game_name] = set()
                await message.channel.send(f'{game_name}を登録したにゃ')

            # /removeコマンドの処理(ゲームをgame_directoryから削除)
            case ('/remove'):
                if game_name not in game_directory:
                    await message.channel.send(f'{game_name}は登録されていないにゃ')
                    return
                del game_directory[game_name]
                await message.channel.send(f'{game_name}を削除したにゃ')

            # /joinコマンドの処理(ゲームに参加)
            case ('/join'):
                if game_name not in game_directory:
                    await message.channel.send(f'{game_name}は登録されていないにゃ')
                    return
                if message.author.id in game_directory[game_name]:
                    await message.channel.send(f'{message.author.name}はすでに{game_name}に参加しているにゃ')
                    return
                game_directory[game_name].add(message.author.id)
                await message.channel.send(f'{message.author.name}が{game_name}に参加したにゃ')

            # /leaveコマンドの処理(ゲームから離脱)
            case ('/leave'):
                if game_name not in game_directory:
                    await message.channel.send(f'{game_name}は登録されていないにゃ')
                    return
                if message.author.id not in game_directory[game_name]:
                    await message.channel.send(f'{message.author.name}は{game_name}に参加していないにゃ')
                    return
                game_directory[game_name].remove(message.author.id)
                await message.channel.send(f'{message.author.name}が{game_name}から離脱したにゃ')

            # /clearコマンドの処理(ゲームの参加者を全員削除)
            case ('/clear'):
                if game_name not in game_directory:
                    await message.channel.send(f'{game_name}は登録されていないにゃ')
                    return
                game_directory[game_name].clear()
                await message.channel.send(f'{game_name}の参加者を全員削除したにゃ')

            # /statusコマンドの処理(ゲームの参加者一覧を表示)
            case ('/status'):
                if game_name not in game_directory:
                    await message.channel.send(f'{game_name}は登録されていないにゃ')
                    return
                if not game_directory[game_name]:
                    await message.channel.send(f'{game_name}には参加者がいないにゃ')
                    return
                member = []
                for user_id in game_directory[game_name]:
                    user = await client.fetch_user(user_id)
                    member.append(user.name)
                response = f'{game_name}の参加者は\n' + '\n'.join(member) + '\nにゃ'
                await message.channel.send(response)

            # /startコマンドの処理(ゲームを開始して参加者を全員削除)
            case ('/start'):
                if game_name not in game_directory:
                    await message.channel.send(f'{game_name}は登録されていないにゃ')
                    return
                if not game_directory[game_name]:
                    await message.channel.send(f'{game_name}には参加者がいないにゃ')
                    return
                member_mentions = []
                for user_id in game_directory[game_name]:
                    member_mentions.append(f"<@{user_id}>")
                response = f'{game_name}を開始するにゃ！\n' + ', '.join(member_mentions) + 'は集合にゃ！\n'
                await message.channel.send(response)
                game_directory[game_name].clear()
                
            
# Botの起動とDiscordサーバーへの接続
client.run(config.DISCORD_TOKEN)
