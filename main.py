import os
import discord
from discord.ext import commands
import datetime,time,json,requests,sys,os,pytz,jishaku
import random
import asyncio
from setting import *
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(os.path.realpath(sys.executable))
elif __file__:
    application_path = os.path.dirname(__file__)
path = application_path.replace("\\","/") + "/"
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=접두사, case_insensitive=True, help_command=None,intents=discord.Intents.all(),owner_ids=관리자아이디)

    async def on_ready(self):
        await self.wait_until_ready()
        i = datetime.datetime.now()
        print(f"{self.user.name}봇은 준비가 완료 되었습니다.")
        print(f"[!] 참가 중인 서버 : {len(self.guilds)}개의 서버에 참여 중")  
        print(f"[!] 이용자 수 : {len(self.users)}명과 함께하는 중")
        guild_list = self.guilds
        for i in guild_list:
            print("서버 ID: {} / 서버 이름: {} / 멤버 수: {}".format(i.id, i.name, i.member_count))

    async def setup_hook(self):
        await self.tree.sync()
        await bot.load_extension("jishaku")

bot = Bot()
pu = {}
pn = {}
inj = {}
dc = {}
ic = {}

def jload(fn):
    jstring = open(path + fn, "r", encoding='utf-8-sig').read()
    a = json.loads(jstring)
    return a

def jsave(fn,n):
    with open(path + fn, "w+", encoding='utf-8-sig') as f:
        json.dump(n, f, indent=2, ensure_ascii=False)

def lsave(fn,n,ctx):
    webhook = discord.SyncWebhook.from_url(웹훅로그)
    try:
        user = ctx.author
    except:
        user = ctx.author
    embed = dembed("로그",n)
    embed.set_author(name="BANK | Log", icon_url=user.avatar.url)
    webhook.send(embed=embed,username=user.name,avatar_url=user.display_avatar)
    with open(path + fn, "a+", encoding='utf-8') as f:
        f.writelines(f"{n}\n")
        f.close()

def get_kr_min():
    return datetime.datetime.now().strftime('%M')

def dembed(title=None,description=None,color=None):
    if color == None:
        color = random.randint(0x000000,0xFFFFFF)
    if title == None:
        return discord.Embed(description=description,color=color,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
    return discord.Embed(title=title,description=description,color=color,timestamp=datetime.datetime.now(pytz.timezone('UTC')))

@bot.hybrid_command(name="가입",description="서비스에 가입 할 수 있습니다.",with_app_command=True)
async def 가입(ctx):
    userdb = jload("db.json")
    if not str(ctx.author.id) in userdb.keys():
        nowtime = datetime.datetime.now()
        lsave(f"log/{ctx.author.id}.txt",f"[ 가입 ]\n\n{ctx.author}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 가입을 완료했습니다\n",ctx)
        le = len(userdb.keys())+1
        f = ""
        for i in range(4-len(str(le))):
            f += "0"
        f += str(le)
        user = str(ctx.author.id)
        timee = datetime.datetime.now().timestamp()
        timee = str(timee).split(".")[0]
        userdb[user] = {"money":int(축하금),"time":timee}
        embed = discord.Embed(description=f"가입 성공! 가입 축하금으로 {축하금}원을 보내드렸어요!",color=0xd8b0cc,timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        try:
            embed.set_author(name="BANK | Join", icon_url=ctx.author.avatar.url)
        except:
            embed.set_author(name="BANK | Join")
        embed.add_field(name=f"돈", value=f"**{축하금}원**", inline=True)
        embed.add_field(name=f"가입 시간", value=f"<t:{timee}:F>", inline=True)
        await ctx.reply(embed=embed)
        jsave("db.json",userdb)
    else:
        await ctx.reply("이미 가입이 되있어요!")

@bot.hybrid_command(name="송금",description="다른 유저에게 송금을 할 수 있습니다.",with_app_command=True)
async def 송금(ctx,user:discord.Member,amount:int):
    userdb = jload("db.json")
    try:
        uinf = userdb[str(ctx.author.id)]
    except:
        return await ctx.reply(embed=dembed("조회실패",f"{ctx.author}님은 아직 서비스를 가입하지 않으셨어요!"))
    if not str(user.id) in userdb.keys():
        return await ctx.reply(embed=dembed("송금 실패","돈을 받을 유저가 서비스를 가입하지 않으셨습니다.",discord.Color.red()))
    elif userdb[str(ctx.author.id)]["money"] < amount or str(userdb[str(ctx.author.id)]["money"]) == "0":
        return await ctx.reply(embed=dembed("송금 실패","자신이 가신 돈보다 큰 금액은 송금이 불가능합니다.",discord.Color.red()))
    elif amount < 500:
        return await ctx.reply(embed=dembed("송금 실패","최소 송금 금액은 500원입니다.",discord.Color.red()))
    elif user == ctx.author:
        return await ctx.reply(embed=dembed("송금 실패","자신에게는 송금할 수 없습니다.",discord.Color.red()))
    su = user
    olm = userdb[str(ctx.author.id)]["money"]
    userdb[str(ctx.author.id)]["money"] = userdb[str(ctx.author.id)]["money"] - amount
    time = uinf["time"]
    money = userdb[str(ctx.author.id)]["money"]
    embed = discord.Embed(title="송금 성공",description=f"{su}님에게 송금을 완료했습니다!",color=random.randint(0x000000,0xFFFFFF),timestamp=datetime.datetime.now(pytz.timezone('UTC')))
    try:
        embed.set_author(name="BANK | Remit", icon_url=ctx.author.avatar.url)
    except:
        embed.set_author(name="BANK | Remit")
    embed.add_field(name=f"돈", value=f"{olm} - {amount} = **{olm - amount}**", inline=True)
    embed.add_field(name=f"가입 시간", value=f"<t:{time}:F>", inline=True)
    await ctx.reply(embed=embed)
    uinf = userdb[str(su.id)]
    money = userdb[str(su.id)]["money"]
    time = uinf["time"]
    embed = discord.Embed(title="입금 안내",description=f"{ctx.author}님이 당신에게 {amount}원을 송금하셨습니다!",color=random.randint(0x000000,0xFFFFFF),timestamp=datetime.datetime.now(pytz.timezone('UTC')))
    try:
        embed.set_author(name="BANK | Remit", icon_url=su.avatar.url)
    except:
        embed.set_author(name="BANK | Remit")
    embed.add_field(name=f"돈", value=f"{money} + {amount} = **{money + amount}**", inline=True)
    embed.add_field(name=f"가입 시간", value=f"<t:{time}:F>", inline=True)
    nowtime = datetime.datetime.now()
    if not str(ctx.author.id) in userdb.keys():
        lsave(f"log/{ctx.author.id}.txt",f"[ 송금 ]\n\n{ctx.author}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {amount}원을 {su}({su.id})님에게 송금하셨습니다\n",ctx)
    else:
        l = f"[ 송금 ]\n\n{ctx.author}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {amount}원을 {su}({su.id})님에게 송금하셨습니다\n"
        lsave(f"log/{ctx.author.id}.txt",l,ctx)
    if not str(su.id) in userdb.keys():
        lsave(f"log/{su.id}.txt",f"[ 송금 ]\n\n{su}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {amount}원을 {ctx.author}({ctx.author.id})님에게 받았습니다\n",ctx)
    else:
        l = f"[ 송금 ]\n\n{su}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {amount}원을 {ctx.author}({ctx.author.id})님에게 받았습니다\n"
        lsave(f"log/{su.id}.txt",l,ctx)
    await su.send(embed=embed)
    userdb[str(su.id)]["money"] = userdb[str(su.id)]["money"] + amount
    jsave("db.json",userdb)

@bot.hybrid_command(name="조회",description="가상 뱅킹을 조회할 수 있습니다.",with_app_command=True)
async def 조회(ctx,user:discord.Member=None):
    if user == None:
        user = ctx.author
    userdb = jload("db.json")
    try:
        uinf = userdb[str(user.id)]
    except:
        return await ctx.reply(embed=dembed("조회실패",f"{user}님은 아직 서비스를 가입하지 않으셨어요!"))
    money = uinf["money"]
    time = uinf["time"]
    embed = discord.Embed(title="조회 성공",description=f"{user}님의 정보를 조회했습니다!",color=random.randint(0x000000,0xFFFFFF),timestamp=datetime.datetime.now(pytz.timezone('UTC')))
    try:
        embed.set_author(name="BANK | Lookup", icon_url=user.avatar.url)
    except:
        embed.set_author(name="BANK | Lookup")
    embed.add_field(name=f"돈", value=f"**{money}**", inline=True)
    embed.add_field(name=f"가입 시간", value=f"<t:{time}:F>", inline=True)
    await ctx.reply(embed=embed)


@bot.hybrid_command(name="돈설정",description="관리자 전용 커맨드입니다.",with_app_command=True)
@commands.is_owner()
async def 돈설정(ctx, user:discord.Member, amount:int):
    userdb = jload("db.json")
    if not str(user.id) in userdb.keys():
        return await ctx.send(embed=dembed("설정실패",f"유저가 아직 서비스를 가입하지 않았습니다",color=discord.Color.red()))   
    else:
        pass
    uinf = userdb[str(user.id)]
    money = uinf["money"]
    time = uinf["time"]
    embed = discord.Embed(title="설정 성공",description=f"{user}님의 돈을 설정했습니다!",color=random.randint(0x000000,0xFFFFFF),timestamp=datetime.datetime.now(pytz.timezone('UTC')))
    try:
        embed.set_author(name="BANK | Setting", icon_url=user.avatar.url)
    except:
        embed.set_author(name="BANK | Setting")
    embed.add_field(name=f"돈", value=f"**기존 : {money}, 현재 : {amount}**", inline=True)
    embed.add_field(name=f"가입 시간", value=f"<t:{time}:F>", inline=True)
    userdb[str(user.id)]["money"] = amount
    jsave("db.json",userdb)
    await ctx.reply(embed=embed)
    nowtime = datetime.datetime.now()
    lsave(f"log/{user.id}.txt",f"[ 조회 ]\n\n{user}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {ctx.author}관리자님이 {user}님의 돈을 {money}원에서 {amount}원으로 돈을 설정하셨습니다\n",ctx)

@bot.hybrid_command(name="강제충전",description="관리자 전용 커맨드입니다.",with_app_command=True)
@commands.is_owner()
async def 강제충전(ctx, user:discord.Member, amount:int):
    userdb = jload("db.json")
    if not str(user.id) in userdb.keys():
        return await ctx.send(embed=dembed("설정실패",f"유저가 아직 서비스를 가입하지 않았습니다",color=discord.Color.red()))   
    else:
        pass
    uinf = userdb[str(user.id)]
    money = uinf["money"]
    time = uinf["time"]
    embed = discord.Embed(title="충전 성공",description=f"{user}님의 돈을 충전했습니다!",color=random.randint(0x000000,0xFFFFFF),timestamp=datetime.datetime.now(pytz.timezone('UTC')))
    try:
        embed.set_author(name="BANK | Charge", icon_url=user.avatar.url)
    except:
        embed.set_author(name="BANK | Charge")
    embed.add_field(name=f"돈", value=f"{money} + {amount} = **{int(money) + int(amount)}**", inline=True)
    embed.add_field(name=f"가입 시간", value=f"<t:{time}:F>", inline=True)
    userdb[str(user.id)]["money"] = int(money) + int(amount)
    jsave("db.json",userdb)
    await ctx.reply(embed=embed)
    nowtime = datetime.datetime.now()
    lsave(f"log/{user.id}.txt",f"[ 강제충전 ]\n\n{user}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {ctx.author}관리자님이 {amount}원을 강제로 충전해주셨습니다\n",ctx)

class updown(discord.ui.Modal,title="업다운 게임"):
    answer = discord.ui.TextInput(label="베팅할 금액을 입력해주세요",style=discord.TextStyle.short,placeholder="1000",required=True,max_length=10)
    async def on_submit(self,ctx:discord.Interaction):
        user = ctx.author
        userdb = jload("banking.json")
        try:
            if pu[str(ctx.author.id)] == True:
                return await ctx.response.send_message(embed=dembed("경고","이미 게임이 진행중입니다.",discord.Color.red()))
        except:
            pass
        if int(str(self.answer)) < 1000:
            return await ctx.response.send_message(embed=dembed("경고","최소 배팅 금액은 1000원 입니다.",discord.Color.red()))
        if userdb[str(ctx.author.id)]["money"] < int(str(self.answer)):
            return await ctx.response.send_message(embed=dembed("경고","자기 돈보다 높은 금액을 배팅하셨습니다.",discord.Color.red()))
        pu[str(ctx.author.id)] = True
        asd = 100
        rn = random.randint(1,asd)
        count = 0
        self.answer = int(str(self.answer))
        await ctx.response.send_message(embed=dembed("업다운게임",f"봇이 1부터 {asd}까지의 숫자를 정했습니다! 정해진 기회는 5번이고 그중 봇이 정한 숫자를 맞춰주세요!\n[제한시간 15초]"))
        for i in range(5):
            hc = True
            while hc:
                try:
                    msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author,timeout=15)
                except asyncio.TimeoutError:
                    pu[str(ctx.author.id)] = False
                    uinf = userdb[str(user.id)]
                    money = uinf["money"]
                    bid = uinf["account"]
                    time = uinf["time"]
                    embed = discord.Embed(title="게임 패배",description=f"<@{ctx.author.id}>님, 제안시간안에 게임을 성공하지 못했습니다.\n[봇이 정한 수는 {rn}이였습니다]",color=discord.Color.red(),timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                    try:
                        embed.set_author(name="BANK | UpdownGame", icon_url=ctx.author.avatar.url)
                    except:
                        embed.set_author(name="BANK | UpdownGame")
                    b = int(str(self.answer))
                    embed.add_field(name=f"돈", value=f"{money} - {b} = **{int(money) - int(b)}**", inline=True)
                    embed.add_field(name=f"코인", value=f"{userdb[str(ctx.author.id)]['coin']}", inline=True)
                    embed.add_field(name=f"유저 계좌", value=f"{bid}", inline=True)
                    embed.add_field(name=f"가입 시간", value=f"<t:{time}:F>", inline=True)
                    userdb[str(user.id)]["money"] = int(money) - int(b)
                    jsave("banking.json",userdb)
                    nowtime = datetime.datetime.now()
                    if not str(user.id) in userdb.keys():
                        lsave(f"log/{ctx.author.id}.txt",f"업다운게임 : {ctx.author}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {self.answer}원을 업다운게임에서 잃으셨습니다",ctx)
                    else:
                        l = f"업다운게임 : {ctx.author}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {self.answer}원을 업다운게임에서 잃으셨습니다"
                        lsave(f"log/{ctx.author.id}.txt",l,ctx)
                    return await ctx.channel.send(embed=embed)
                await msg.delete()
                try:
                    test = int(msg.content)
                    hc = False
                except:
                    await ctx.channel.send(embed=dembed("경고","숫자로 입력하세요.",discord.Color.gold()),delete_after=15)
            try:
                count += 1
                if int(msg.content) == rn:
                    pu[str(ctx.author.id)] = False
                    uinf = userdb[str(user.id)]
                    money = uinf["money"]
                    bid = uinf["account"]
                    time = uinf["time"]
                    embed = discord.Embed(title="게임 승리",description=f"<@{ctx.author.id}>님, 적중했어요! 봇이 선택한 숫자는 {rn}였습니다!\n[{count}번만에 맞추셨어요]",color=discord.Color.green(),timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                    try:
                        embed.set_author(name="BANK | UpdownGame", icon_url=ctx.author.avatar.url)
                    except:
                        embed.set_author(name="BANK | UpdownGame")
                    b = round(int(str(self.answer)) * 0.99)
                    embed.add_field(name=f"돈", value=f"{money} + {b} = **{int(money) + int(b)}**", inline=True)
                    embed.add_field(name=f"코인", value=f"{userdb[str(ctx.author.id)]['coin']}", inline=True)
                    embed.add_field(name=f"유저 계좌", value=f"{bid}", inline=True)
                    embed.add_field(name=f"가입 시간", value=f"<t:{time}:F>", inline=True)
                    userdb[str(user.id)]["money"] = int(money) + int(b)
                    jsave("banking.json",userdb)
                    nowtime = datetime.datetime.now()
                    if not str(user.id) in userdb.keys():
                        lsave(f"log/{ctx.author.id}.txt",f"업다운게임 : {ctx.author}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {self.answer}원을 1.99배인 {round(float(str(self.answer)) * 1.99)}원을 늘렸습니다.",ctx)
                    else:
                        l = f"업다운게임 : {ctx.author}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {self.answer}원을 1.99배인 {round(float(str(self.answer)) * 1.99)}원으로 뿔리셨습니다"
                        lsave(f"log/{ctx.author.id}.txt",l,ctx)
                    return await ctx.channel.send(embed=embed)
                elif int(msg.content) > rn:
                    i = 5 - count
                    if i == 0:
                        pu[str(ctx.author.id)] = False
                        uinf = userdb[str(user.id)]
                        money = uinf["money"]
                        bid = uinf["account"]
                        time = uinf["time"]
                        embed = discord.Embed(title="게임 패배",description=f"<@{ctx.author.id}>님, 5번 안에 숫자를 맞추지 못했어요.\n[봇이 정한 수는 {rn}이였습니다]",color=discord.Color.red(),timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                        try:
                            embed.set_author(name="BANK | UpdownGame", icon_url=ctx.author.avatar.url)
                        except:
                            embed.set_author(name="BANK | UpdownGame")
                        b = int(str(self.answer))
                        embed.add_field(name=f"돈", value=f"{money} - {b} = **{int(money) - int(b)}**", inline=True)
                        embed.add_field(name=f"코인", value=f"{userdb[str(ctx.author.id)]['coin']}", inline=True)
                        embed.add_field(name=f"유저 계좌", value=f"{bid}", inline=True)
                        embed.add_field(name=f"가입 시간", value=f"<t:{time}:F>", inline=True)
                        userdb[str(user.id)]["money"] = int(money) - int(b)
                        jsave("banking.json",userdb)
                        nowtime = datetime.datetime.now()
                        if not str(user.id) in userdb.keys():
                            lsave(f"log/{ctx.author.id}.txt",f"업다운게임 : {ctx.author}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {self.answer}원을 업다운게임에서 잃으셨습니다",ctx)
                        else:
                            l = f"업다운게임 : {ctx.author}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {self.answer}원을 업다운게임에서 잃으셨습니다"
                            lsave(f"log/{ctx.author.id}.txt",l,ctx)
                        return await ctx.channel.send(embed=embed)
                    await ctx.channel.send(embed = dembed("다운!",f"기회가 {i}번 남음.\n[입력한 수 : {msg.content}]"),delete_after=15)
                elif int(msg.content) < rn:
                    i = 5 - count
                    if str(i) == "0":
                        pu[str(ctx.author.id)] = False
                        uinf = userdb[str(user.id)]
                        money = uinf["money"]
                        bid = uinf["account"]
                        time = uinf["time"]
                        embed = discord.Embed(title="게임 패배",description=f"<@{ctx.author.id}>님, 5번 안에 숫자를 맞추지 못했어요.\n[봇이 정한 수는 {rn}이였습니다]",color=discord.Color.red(),timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                        try:
                            embed.set_author(name="BANK | UpdownGame", icon_url=ctx.author.avatar.url)
                        except:
                            embed.set_author(name="BANK | UpdownGame")
                        b = int(str(self.answer))
                        embed.add_field(name=f"돈", value=f"{money} - {b} = **{int(money) - int(b)}**", inline=True)
                        embed.add_field(name=f"코인", value=f"{userdb[str(ctx.author.id)]['coin']}", inline=True)
                        embed.add_field(name=f"유저 계좌", value=f"{bid}", inline=True)
                        embed.add_field(name=f"가입 시간", value=f"<t:{time}:F>", inline=True)
                        userdb[str(user.id)]["money"] = int(money) - int(b)
                        jsave("banking.json",userdb)
                        nowtime = datetime.datetime.now()
                        if not str(user.id) in userdb.keys():
                            lsave(f"log/{ctx.author.id}.txt",f"업다운게임 : {ctx.author}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {self.answer}원을 업다운게임에서 잃으셨습니다",ctx)
                        else:
                            l = f"업다운게임 : {ctx.author}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {self.answer}원을 업다운게임에서 잃으셨습니다"
                            lsave(f"log/{ctx.author.id}.txt",l,ctx)
                        return await ctx.channel.send(embed=embed)
                    await ctx.channel.send(embed = dembed("업!",f"기회가 {i}번 남음.\n[입력한 수 : {msg.content}]"),delete_after=15)
            except Exception as e:
                print(str(e))

@bot.hybrid_command(name="업다운",description="업다운 게임을 할 수 있습니다. (1.99배)",with_app_command=True)
async def 업다운(ctx):
    if ctx.channel.name != f"개인채널-{str(ctx.author.id)}":
        await ctx.defer(ephemeral=True)
        return await ctx.send(embed=dembed("게임 시작 실패","``/개인채널``명령어로 개인채널을 생성한 후 개인채널에서 게임을 진행해주세요.",discord.Color.red()))
    await ctx.interaction.response.send_modal(updown())

class baccarat(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Tie",style=discord.ButtonStyle.gray)
    async def TieButton(self,inter,button):
        class baccarat_(discord.ui.Modal,title="바카라"):
            answer = discord.ui.TextInput(label="베팅할 금액을 입력해주세요",style=discord.TextStyle.short,placeholder="1000",required=True,max_length=10)
            async def on_submit(self,ctx):
                banker = random.randint(0,9)
                player = random.randint(0,9)
                userdb = jload("banking.json")
                if int(str(self.answer)) < 1000:
                    return await ctx.response.send_message(embed=dembed("경고","최소 배팅 금액은 1000원 입니다.",discord.Color.red()))
                if userdb[str(ctx.author.id)]["money"] < int(str(self.answer)):
                    return await ctx.response.send_message(embed=dembed("경고","자기 돈보다 높은 금액을 배팅하셨습니다.",discord.Color.red()))
                if banker == player:
                    user = inter.user
                    uinf = userdb[str(user.id)]
                    money = uinf["money"]
                    bid = uinf["account"]
                    time = uinf["time"]
                    embed = discord.Embed(title="게임 승리",description=f"<@{user.id}>님, 배팅에 성공했어요.\n[Player : {player}, Banker : {banker}]",color=discord.Color.green(),timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                    try:
                        embed.set_author(name="BANK | Baccarat", icon_url=user.avatar.url)
                    except:
                        embed.set_author(name="BANK | Baccarat")
                    b = round(int(str(self.answer)) * 5.98)
                    answer = self.answer
                    embed.add_field(name=f"돈", value=f"{money} + {b} = **{int(money) + int(b)}**", inline=True)
                    embed.add_field(name=f"코인", value=f"{userdb[str(user.id)]['coin']}", inline=True)
                    embed.add_field(name=f"유저 계좌", value=f"{bid}", inline=True)
                    embed.add_field(name=f"가입 시간", value=f"<t:{time}:F>", inline=True)
                    userdb[str(user.id)]["money"] = int(money) + int(b)
                    jsave("banking.json",userdb)
                    nowtime = datetime.datetime.now()
                    if not str(user.id) in userdb.keys():
                        lsave(f"log/{user.id}.txt",f"바카라 : {user}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {self.answer}원을 6.98배인 {round(float(str(self.answer)) * 6.98)}원으로 뿔리셨습니다",ctx)
                    else:
                        l = f"바카라 : {user}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {self.answer}원을 6.98배인 {round(float(str(self.answer)) * 6.98)}원으로 뿔리셨습니다"
                        lsave(f"log/{user.id}.txt",l,ctx)
                    return await ctx.response.send_message(embed=embed)
                else:
                    user = inter.user
                    uinf = userdb[str(user.id)]
                    money = uinf["money"]
                    bid = uinf["account"]
                    time = uinf["time"]
                    embed = discord.Embed(title="게임 패배",description=f"<@{user.id}>님, 배팅에 실패했어요.\n[Player : {player}, Banker : {banker}]",color=discord.Color.red(),timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                    try:
                        embed.set_author(name="BANK | Baccarat", icon_url=user.avatar.url)
                    except:
                        embed.set_author(name="BANK | Baccarat")
                    b = int(str(self.answer))
                    answer = self.answer
                    embed.add_field(name=f"돈", value=f"{money} - {b} = **{int(money) - int(b)}**", inline=True)
                    embed.add_field(name=f"코인", value=f"{userdb[str(user.id)]['coin']}", inline=True)
                    embed.add_field(name=f"유저 계좌", value=f"{bid}", inline=True)
                    embed.add_field(name=f"가입 시간", value=f"<t:{time}:F>", inline=True)
                    userdb[str(user.id)]["money"] = int(money) - int(b)
                    jsave("banking.json",userdb)
                    nowtime = datetime.datetime.now()
                    if not str(user.id) in userdb.keys():
                        lsave(f"log/{user.id}.txt",f"바카라 : {user}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {answer}원을 바카라에서 잃으셨습니다",ctx)
                    else:
                        l = f"바카라 : {user}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {answer}원을 바카라에서 잃으셨습니다"
                        lsave(f"log/{user.id}.txt",l,ctx)
                    return await ctx.response.send_message(embed=embed)
        await inter.response.send_modal(baccarat_())
    @discord.ui.button(label="Player",style=discord.ButtonStyle.success)
    async def PlayerButton(self,inter,button):
        class baccarat_(discord.ui.Modal,title="바카라"):
            answer = discord.ui.TextInput(label="베팅할 금액을 입력해주세요",style=discord.TextStyle.short,placeholder="1000",required=True,max_length=10)
            async def on_submit(self,ctx):
                banker = random.randint(0,9)
                player = random.randint(0,9)
                userdb = jload("banking.json")
                if int(str(self.answer)) < 1000:
                    return await ctx.response.send_message(embed=dembed("경고","최소 배팅 금액은 1000원 입니다.",discord.Color.red()))
                if userdb[str(ctx.author.id)]["money"] < int(str(self.answer)):
                    return await ctx.response.send_message(embed=dembed("경고","자기 돈보다 높은 금액을 배팅하셨습니다.",discord.Color.red()))
                if banker < player:
                    user = inter.user
                    uinf = userdb[str(user.id)]
                    money = uinf["money"]
                    bid = uinf["account"]
                    time = uinf["time"]
                    embed = discord.Embed(title="게임 승리",description=f"<@{user.id}>님, 배팅에 성공했어요.\n[Player : {player}, Banker : {banker}]",color=discord.Color.green(),timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                    try:
                        embed.set_author(name="BANK | Baccarat", icon_url=user.avatar.url)
                    except:
                        embed.set_author(name="BANK | Baccarat")
                    b = round(int(str(self.answer)) * 0.98)
                    answer = self.answer
                    embed.add_field(name=f"돈", value=f"{money} + {b} = **{int(money) + int(b)}**", inline=True)
                    embed.add_field(name=f"코인", value=f"{userdb[str(ctx.author.id)]['coin']}", inline=True)
                    embed.add_field(name=f"유저 계좌", value=f"{bid}", inline=True)
                    embed.add_field(name=f"가입 시간", value=f"<t:{time}:F>", inline=True)
                    userdb[str(user.id)]["money"] = int(money) + int(b)
                    jsave("banking.json",userdb)
                    nowtime = datetime.datetime.now()
                    if not str(user.id) in userdb.keys():
                        lsave(f"log/{user.id}.txt",f"바카라 : {user}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {self.answer}원을 1.98배인 {round(float(str(self.answer)) * 1.98)}원으로 뿔리셨습니다",ctx)
                    else:
                        l = f"바카라 : {user}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {self.answer}원을 1.98배인 {round(float(str(self.answer)) * 1.98)}원으로 뿔리셨습니다"
                        lsave(f"log/{user.id}.txt",l,ctx)
                    return await ctx.response.send_message(embed=embed)
                else:
                    if banker == player:
                        user = inter.user
                        uinf = userdb[str(user.id)]
                        money = uinf["money"]
                        bid = uinf["account"]
                        time = uinf["time"]
                        embed = discord.Embed(title="게임 무승부",description=f"<@{user.id}>님, 무승부에요.\n[Player : {player}, Banker : {banker}]",color=discord.Color.gold(),timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                        try:
                            embed.set_author(name="BANK | Baccarat", icon_url=user.avatar.url)
                        except:
                            embed.set_author(name="BANK | Baccarat")
                        answer = self.answer
                        embed.add_field(name=f"돈", value=f"**{money}**", inline=True)
                        embed.add_field(name=f"코인", value=f"{userdb[str(ctx.author.id)]['coin']}", inline=True)
                        embed.add_field(name=f"유저 계좌", value=f"{bid}", inline=True)
                        embed.add_field(name=f"가입 시간", value=f"<t:{time}:F>", inline=True)
                        nowtime = datetime.datetime.now()
                        if not str(user.id) in userdb.keys():
                            lsave(f"log/{user.id}.txt",f"바카라 : {user}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {self.answer}원을 배팅했지만 무승부로 돌려받으셨습니다",ctx)
                        else:
                            l = f"바카라 : {user}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {self.answer}원을 배팅했지만 무승부로 돌려받으셨습니다"
                            lsave(f"log/{user.id}.txt",l,ctx)
                        return await ctx.response.send_message(embed=embed)
                    user = inter.user
                    uinf = userdb[str(user.id)]
                    money = uinf["money"]
                    bid = uinf["account"]
                    time = uinf["time"]
                    embed = discord.Embed(title="게임 패배",description=f"<@{user.id}>님, 배팅에 실패했어요.\n[Player : {player}, Banker : {banker}]",color=discord.Color.red(),timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                    try:
                        embed.set_author(name="BANK | Baccarat", icon_url=user.avatar.url)
                    except:
                        embed.set_author(name="BANK | Baccarat")
                    b = int(str(self.answer))
                    answer = self.answer
                    embed.add_field(name=f"돈", value=f"{money} - {b} = **{int(money) - int(b)}**", inline=True)
                    embed.add_field(name=f"코인", value=f"{userdb[str(ctx.author.id)]['coin']}", inline=True)
                    embed.add_field(name=f"유저 계좌", value=f"{bid}", inline=True)
                    embed.add_field(name=f"가입 시간", value=f"<t:{time}:F>", inline=True)
                    userdb[str(user.id)]["money"] = int(money) - int(b)
                    jsave("banking.json",userdb)
                    nowtime = datetime.datetime.now()
                    if not str(user.id) in userdb.keys():
                        lsave(f"log/{user.id}.txt",f"바카라 : {user}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {answer}원을 바카라에서 잃으셨습니다",ctx)
                    else:
                        l = f"바카라 : {user}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {answer}원을 바카라에서 잃으셨습니다"
                        lsave(f"log/{user.id}.txt",l,ctx)
                    return await ctx.response.send_message(embed=embed)
        await inter.response.send_modal(baccarat_())
    @discord.ui.button(label="Banker",style=discord.ButtonStyle.danger)
    async def BankerButton(self,inter,button):
        class baccarat_(discord.ui.Modal,title="바카라"):
            answer = discord.ui.TextInput(label="베팅할 금액을 입력해주세요",style=discord.TextStyle.short,placeholder="1000",required=True,max_length=10)
            async def on_submit(self,ctx):
                banker = random.randint(0,9)
                player = random.randint(0,9)
                userdb = jload("banking.json")
                if int(str(self.answer)) < 1000:
                    return await ctx.response.send_message(embed=dembed("경고","최소 배팅 금액은 1000원 입니다.",discord.Color.red()))
                if userdb[str(ctx.author.id)]["money"] < int(str(self.answer)):
                    return await ctx.response.send_message(embed=dembed("경고","자기 돈보다 높은 금액을 배팅하셨습니다.",discord.Color.red()))
                if banker > player:
                    user = inter.user
                    uinf = userdb[str(user.id)]
                    money = uinf["money"]
                    bid = uinf["account"]
                    time = uinf["time"]
                    embed = discord.Embed(title="게임 승리",description=f"<@{user.id}>님, 배팅에 성공했어요.\n[Player : {player}, Banker : {banker}]",color=discord.Color.green(),timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                    try:
                        embed.set_author(name="BANK | Baccarat", icon_url=user.avatar.url)
                    except:
                        embed.set_author(name="BANK | Baccarat")
                    b = round(int(str(self.answer)) * 0.8)
                    answer = self.answer
                    embed.add_field(name=f"돈", value=f"{money} + {b} = **{int(money) + int(b)}**", inline=True)
                    embed.add_field(name=f"코인", value=f"{userdb[str(ctx.author.id)]['coin']}", inline=True)
                    embed.add_field(name=f"유저 계좌", value=f"{bid}", inline=True)
                    embed.add_field(name=f"가입 시간", value=f"<t:{time}:F>", inline=True)
                    userdb[str(user.id)]["money"] = int(money) + int(b)
                    jsave("banking.json",userdb)
                    nowtime = datetime.datetime.now()
                    if not str(user.id) in userdb.keys():
                        lsave(f"log/{user.id}.txt",f"바카라 : {user}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {self.answer}원을 1.8배인 {round(float(str(self.answer)) * 1.8)}원으로 뿔리셨습니다",ctx)
                    else:
                        l = f"바카라 : {user}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {self.answer}원을 1.8배인 {round(float(str(self.answer)) * 1.8)}원으로 뿔리셨습니다"
                        lsave(f"log/{user.id}.txt",l,ctx)
                    return await ctx.response.send_message(embed=embed)
                else:
                    if banker == player:
                        user = inter.user
                        uinf = userdb[str(user.id)]
                        money = uinf["money"]
                        bid = uinf["account"]
                        time = uinf["time"]
                        embed = discord.Embed(title="게임 무승부",description=f"<@{user.id}>님, 무승부에요.\n[Player : {player}, Banker : {banker}]",color=discord.Color.gold(),timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                        try:
                            embed.set_author(name="BANK | Baccarat", icon_url=user.avatar.url)
                        except:
                            embed.set_author(name="BANK | Baccarat")
                        answer = self.answer
                        embed.add_field(name=f"돈", value=f"**{money}**", inline=True)
                        embed.add_field(name=f"코인", value=f"{userdb[str(ctx.author.id)]['coin']}", inline=True)
                        embed.add_field(name=f"유저 계좌", value=f"{bid}", inline=True)
                        embed.add_field(name=f"가입 시간", value=f"<t:{time}:F>", inline=True)
                        nowtime = datetime.datetime.now()
                        if not str(user.id) in userdb.keys():
                            lsave(f"log/{user.id}.txt",f"바카라 : {user}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {self.answer}원을 배팅했지만 무승부로 돌려받으셨습니다",ctx)
                        else:
                            l = f"바카라 : {user}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {self.answer}원을 배팅했지만 무승부로 돌려받으셨습니다"
                            lsave(f"log/{user.id}.txt",l,ctx)
                        return await ctx.response.send_message(embed=embed)
                    user = inter.user
                    uinf = userdb[str(user.id)]
                    money = uinf["money"]
                    bid = uinf["account"]
                    time = uinf["time"]
                    embed = discord.Embed(title="게임 패배",description=f"<@{user.id}>님, 배팅에 실패했어요.\n[Player : {player}, Banker : {banker}]",color=discord.Color.red(),timestamp=datetime.datetime.now(pytz.timezone('UTC')))
                    try:
                        embed.set_author(name="BANK | Baccarat", icon_url=user.avatar.url)
                    except:
                        embed.set_author(name="BANK | Baccarat")
                    b = int(str(self.answer))
                    answer = self.answer
                    embed.add_field(name=f"돈", value=f"{money} - {b} = **{int(money) - int(b)}**", inline=True)
                    embed.add_field(name=f"코인", value=f"{userdb[str(ctx.author.id)]['coin']}", inline=True)
                    embed.add_field(name=f"유저 계좌", value=f"{bid}", inline=True)
                    embed.add_field(name=f"가입 시간", value=f"<t:{time}:F>", inline=True)
                    userdb[str(user.id)]["money"] = int(money) - int(b)
                    jsave("banking.json",userdb)
                    nowtime = datetime.datetime.now()
                    if not str(user.id) in userdb.keys():
                        lsave(f"log/{user.id}.txt",f"바카라 : {user}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {answer}원을 바카라에서 잃으셨습니다",ctx)
                    else:
                        l = f"바카라 : {user}님이 {nowtime.year}년 {nowtime.month}월 {nowtime.day}일 {nowtime.hour}시 {nowtime.minute}분 {nowtime.second}초에 {answer}원을 바카라에서 잃으셨습니다"
                        lsave(f"log/{user.id}.txt",l,ctx)
                    return await ctx.response.send_message(embed=embed)
        await inter.response.send_modal(baccarat_())
@bot.hybrid_command(name="바카라",description="바카라를 할 수 있습니다. (Banker : 1.8배, Player : 1.98배, Tie : 6.98배)",with_app_command=True)
async def 바카라(ctx):
    if ctx.channel.name != f"개인채널-{str(ctx.author.id)}":
        await ctx.defer(ephemeral=True)
        return await ctx.send(embed=dembed("게임 시작 실패","``/개인채널``명령어로 개인채널을 생성한 후 개인채널에서 게임을 진행해주세요.",discord.Color.red()))
    await ctx.send(embed=dembed("배팅","배팅할 곳을 선택해주세요!\n```Tie : 6.98배, Player : 1.98배, Banker : 1.8배```"),view=baccarat())


@bot.hybrid_command(name="로그",description="관리자 전용 커맨드입니다.",with_app_command=True)
@commands.is_owner()
async def 로그(ctx,user:discord.Member):
    try:
        await ctx.reply(file=discord.File(f"{path}log/{user.id}.txt"))
    except:
        await ctx.reply("유저가 아직 가입하지 않았습니다")

class dsm(discord.ui.Select):
    def __init__(self):
        options = []
        a = 0
        for i in dc:
            a += 1
            options.append(discord.SelectOption(label=f'다이스 #{a}', description=f"{i}\n배팅금 : 1000원", emoji='📥'))
        super().__init__(placeholder='입장하실 채널을 선택해주세요', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'{self.values[0]}채널에 입장하셨습니다',ephemeral=True)

class diceselect(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(dsm())

class ism(discord.ui.Select):
    def __init__(self):
        options = []
        a = 0
        for i in list(ic.values()):
            a += 1
            owner = bot.get_user(i["owner"])
            options.append(discord.SelectOption(label=i["name"], description=f"방장 : {owner}\n배팅금 : {i['bet']}원", emoji='📥'))
        super().__init__(placeholder='입장하실 채널을 선택해주세요', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'{self.values[0]}채널에 입장하셨습니다',ephemeral=True)

class ipokerselect(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ism())

class bcmenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="다이스 채널 참가",style=discord.ButtonStyle.green,custom_id="dice:cj")
    async def dchannel_join(self,inter,button):
        if len(list(dc.keys())) == 0:
            return await inter.response.send_message(embed=dembed("채널 참가 실패","입장 가능한 방이 없습니다"),ephemeral=True)
        await inter.response.send_message("채널 참가",view=diceselect(),ephemeral=True)

    @discord.ui.button(label="다이스 채널 생성",style=discord.ButtonStyle.red,custom_id="dice:cc")
    async def dchannel_create(self,inter,button):
        cg = discord.utils.get(inter.guild.categories, id=다이스카테고리)
        channel = await inter.guild.create_text_channel(name=f'다이스 #{len(ic.keys())+1}', category=cg)
        dc[str(channel.id)] = {"name":f'다이스 #{len(dc.keys())+1}',"owner":inter.user.id,"bet":1000,"disabled":False,"users":[inter.user.id]}
        await inter.response.send_message(f"<#{channel.id}>로 이동하세요",ephemeral=True)

    @discord.ui.button(label="인디언 포커 채널 참가",style=discord.ButtonStyle.green,custom_id="bcmenu:cj")
    async def ichannel_join(self,inter,button):
        if len(list(ic.keys())) == 0:
            return await inter.response.send_message(embed=dembed("채널 참가 실패","입장 가능한 방이 없습니다"),ephemeral=True)
        await inter.response.send_message("채널 참가",view=ipokerselect(),ephemeral=True)

    @discord.ui.button(label="인디언 포커 채널 생성",style=discord.ButtonStyle.red,custom_id="bcmenu_cc")
    async def ichannel_create(self,inter,button):
        cg = discord.utils.get(inter.guild.categories, id=인디언포커카테고리)
        channel = await inter.guild.create_text_channel(name=f'인디언 포커 #{len(ic.keys())+1}', category=cg)
        ic[str(channel.id)] = {"name":f'인디언 포커 #{len(ic.keys())+1}',"owner":inter.user.id,"bet":1000,"disabled":False,"users":[inter.user.id]}
        print(ic)
        await inter.response.send_message(f"<#{channel.id}>로 이동하세요",ephemeral=True)



@bot.hybrid_command(name="배팅채널메뉴",description="관리자 전용 커맨드입니다.",with_app_command=True)
@commands.is_owner()
async def 뱃채널메뉴(ctx):
    await ctx.send(embed=dembed("게임","다이스, 인디언 포커 방에 들어가시거나 방을 만드시려면 아래 버튼을 눌러주세요"),view=bcmenu())

@bot.hybrid_command(name="문의",description="티켓을 만들어줍니다.",with_app_command=True)
async def 문의(ctx):
    if ctx.channel.name == f"문의-{str(ctx.author.id)}":
        if ctx.author.guild_permissions.administrator:
            await ctx.defer()
            m = await ctx.send(f"채널이 10초 후에 삭제됩니다.")
            a = 10
            for i in range(10):
                await asyncio.sleep(1)
                a -= 1
                await m.edit(content=f"채널이 {a}초 후에 삭제됩니다.")
            await asyncio.sleep(1)
            return await ctx.channel.delete()
        else:
            await ctx.defer(ephemeral=True)
            await ctx.send("티켓 관리자만 가능합니다.")
    await ctx.defer(ephemeral=True)
    for i in ctx.guild.channels:
        if i.name == str(ctx.author.id):
            return await ctx.send(embed=dembed("티켓 생성 오류","이미 당신의 티켓이 존재합니다.",discord.Color.red()))
    pcc = discord.utils.get(ctx.guild.categories,name="티켓")
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
        ctx.author: discord.PermissionOverwrite(view_channel=True,send_messages=True),
    }
    pc = await pcc.create_text_channel(
        f"문의-{ctx.author.id}",overwrites=overwrites
    )
    await ctx.send(f"<#{pc.id}>로 이동해주세요.")
    await pc.send(embed=dembed("티켓 생성 완료","티켓을 생성했습니다!\n문의 내용을 말씀해주세요.\n티켓을 닫으시려면 /문의 를 입력해주세요"))
    a = await pc.send("@everyone")
    await a.delete()

bot.run(토큰)