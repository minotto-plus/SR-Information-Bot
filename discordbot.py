import discord
import random
import re
import google.generativeai as genai


from dotenv import load_dotenv
load_dotenv()

import os
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

genai.configure(api_key=GOOGLE_API_KEY)



# Bot起動時に呼び出される関数
@client.event
async def on_ready():
    print("Ready!")

# メッセージの検知
@client.event
async def on_message(message):
    # 自身が送信したメッセージには反応しない
    if message.author == client.user:
        return

    if "!sri" in message.content:
        if "!sri help" in message.content:
            # await message.channel.send(answer.text)
            embed = discord.Embed(
                title="help",)
            embed.add_field(name="!sri help",value="ヘルプを表示。",inline=False)
            embed.add_field(name="!sri housou,!sri h",value="駅放送、車内放送を表示。最後-1~6を付けると表示する放送の種類を指定できる。",inline=False)
            embed.add_field(name="!sri info",value="運行情報を表示。",inline=False)
            
            await message.channel.send(embed=embed)

        elif "!sri housou" in message.content or "!sri h" in message.content:

            onegai_syurui=[
                "接近放送",
                "次発予告放送",
                "停車中放送",
                "終着放送",
                "到着車内放送",
                "次駅車内放送"
            ]
            onegai_list=[
                "下北沢鉄道という架空の鉄道の接近放送を、次の形式に基づいて一つだけ出力してください。形式：「まもなく（番線番号）番線に、（直通先路線）直通、（列車種別）、（行先）行きがまいります。危ないですから、黄色い点字ブロックまでお下がりください。この電車は（列車両数）両です。」",
                "下北沢鉄道という架空の鉄道の次発予告放送を、次の形式に基づいて一つだけ出力してください。形式：「本日も、（列車運営会社）をご利用くださいましてありがとうございます。今度の（番線番号）番線の列車は、（発車時）時（発車分）分発、（直通先路線）直通、（列車種別）、（駅名）行きです。この電車は（列車両数）両です。次は、（次の駅名）に停まります。」",
                "下北沢鉄道という架空の鉄道の停車中放送を、次の形式に基づいて一つだけ出力してください。形式：「本日も、（列車運営会社）をご利用くださいましてありがとうございます。（番線番号）番線に停車中の電車は、（発車時）時（発車分）分発、（直通先路線）直通、（列車種別）、（駅名）行きです。発車までしばらくお待ちください。」",
                "下北沢鉄道という架空の鉄道の終着放送を、次の形式に基づいて一つだけ出力してください。形式：「（列車が到着した駅名）、（列車が到着した駅名）。本日も、（列車運営会社）をご利用くださいましてありがとうございました。お忘れ物のないようご注意ください。」",
                "下北沢鉄道という架空の鉄道の到着車内放送を、次の形式に基づいて一つだけ出力してください。形式：「（列車運営会社）をご利用くださいまして、ありがとうございます。この電車は、（直通先路線）直通、（列車種別）、（駅名）行きです。」",
                "下北沢鉄道という架空の鉄道の次駅車内放送を、次の形式に基づいて一つだけ出力してください。形式：「まもなく（列車が到着した駅名）、（列車が到着した駅名）。お出口は右側です。電車とホームの間が空いているところがありますので、足元にご注意ください。お降りの際はドア横のボタンを押してください。」",
            ]
            
            joken=["-1","-2","-3","-4","-5","-6"]
            if any((a in message.content) for a in joken):
                
                m = message.content.partition('-')
                bangou=int(m[2])
                syurui_bangou=bangou-1
                random_chokutsu=random_chokutsu=random.randint(0,3)
                ISrandom="("+str(bangou)+")"
            else:
                syurui_bangou=random.randint(0,5)
                random_chokutsu=random.randint(0,3)
                ISrandom="(random)"



            if random_chokutsu==0:
                chokutsu=""
            else:
                chokutsu="この電車は直通しないため、案内放送の「（直通先路線）直通、」の部分を飛ばして出力してください"

            onegai=onegai_list[syurui_bangou]
            embed_title=onegai_syurui[syurui_bangou] + ISrandom


            gemini_pro = genai.GenerativeModel("gemini-pro")
            prompt = onegai + chokutsu + "回答には一切のかぎかっこ記号を含めないでください。" + "以下が下北沢鉄道の情報です。所有する路線：下北沢本線。発着番線：114番線、514番線、810番線。発車時刻：１９時１９分。停車する駅：備中田所神代、野獣邸、下北沢、東北沢、軍畑、田所、遠野、三浦、木村、谷岡。両数：114両、514両、810両。直通先：「中オオン!・総武線」、「ゲイ備線」、「迫真線」。列車種別：普通、急行、特急。特急の名称：田所あずさ、快速ホームライナー屋上。特急の号数：114,514,810号のいずれか。"
            answer = gemini_pro.generate_content(prompt)
            print(answer.text)
            # await message.channel.send(answer.text)
            embed = discord.Embed(title=embed_title,description=answer.text)
            await message.channel.send(embed=embed)


        elif "!sri info" in message.content:
            onegai="架空の鉄道である下北沢鉄道の遅延情報を作成して。次の形式に基づいて一つだけ出力してください。「（駅名）駅で発生した（遅延理由）のため、（路線名）線の一部列車に約（最低分数）分~（最高分数）分以上の遅れがでています。」"
            embed_title="遅延情報"

            gemini_pro = genai.GenerativeModel("gemini-pro")
            prompt = onegai + "回答には一切のかぎかっこ記号を含めないでください。" + "以下が下北沢鉄道の情報です。所有する路線：下北沢本線。停車する駅：備中田所神代、野獣邸、下北沢、東北沢、軍畑、田所、遠野、三浦、木村、谷岡。直通先：「中オオン!・総武線」、「ゲイ備線」、「迫真線」。列車種別：普通、急行、特急。特急の名称：田所あずさ、快速ホームライナー屋上。特急の号数：114,514,810号のいずれか。"
            answer = gemini_pro.generate_content(prompt)
            print(answer.text)
            # await message.channel.send(answer.text)
            embed = discord.Embed(title=embed_title,description=answer.text)
            await message.channel.send(embed=embed)




# Bot起動
client.run(DISCORD_TOKEN)