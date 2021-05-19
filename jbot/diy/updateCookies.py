import os
from telethon import events
from .. import jdbot,chat_id,_ConfigDir
_config = _ConfigDir + '/config.sh'
_CookiesDB = '/ql/db/cookie.db'
#为bot增加更新/添加Cookies功能
#https://github.com/hysbeta/jddockerbot/blob/master/jbot/diy/updateCookies.py
#用法：
#1.部署updateCookies.py到diy文件夹下
#2.从其他途径或SuMaiKaDe/jddockerbot的bot处获取Cookies
#3.发送Cookies给bot即可实现自动替换/增加Cookies

# Update on May 20, 2021
# 支持青龙Docker的Cookies更新
# 由于没搞明白怎么增加新的Cookies, 所以只能更新原有的Cookies
# 每次更新Cookies都会重启面板，请知悉

@jdbot.on(events.NewMessage(chats=chat_id,pattern=('pt_key=')))
async def updateCookies(event):
    i = 1
    #分离收到的pt_pin用于匹配
    pt_pin = event.text.split(";")[1]
    #区分Docker类型，若ql脚本存在则默认为QL docker，否则默认为v4
    if os.path.exists('/usr/local/bin/ql'):
        #加载config.sh文件内容
        config = open(_CookiesDB, 'r', encoding='utf-8').readlines()
        config_text = open(_CookiesDB, 'r', encoding='utf-8').read()
        for record in config:
            if record.strip() is not None:
                i = i + 1
        if pt_pin in config_text:
            for line in config:
                if pt_pin in line:
                    config[config.index(line)] = line.replace(line.split("\"")[3], event.text)
            try:
                open(_CookiesDB, 'w+', encoding='utf-8').writelines(config)
                await jdbot.send_message(chat_id,"更新"+str(pt_pin)+"的Cookies成功！当前共有："+str(i-1)+"个Cookies")
            except Exception as error:
                await jdbot.send_message(chat_id,"更新"+str(pt_pin)+"的Cookies失败，请重试！")
        else:
            # 由于没搞明白_CookiesDB里面的_id是怎么生成的， 所以不支持增加新Cookies
            await jdbot.send_message(chat_id,"Cookies:"+str(pt_pin)+"不存在，请先在面板添加！")
        os.system("/usr/local/bin/pm2 reload all")
    else:
        #加载config.sh文件内容
        config = open(_config, 'r', encoding='utf-8').readlines()
        config_text = open(_config, 'r', encoding='utf-8').read()
        while "Cookie" + str(i) in config_text:
            i = i + 1
        if pt_pin in config_text:
            for line in config:
                if pt_pin in line:
                    config[config.index(line)] = line.replace(line.split("\"")[1], event.text)
            try:
                open(_config, 'w+', encoding='utf-8').writelines(config)
                await jdbot.send_message(chat_id,"更新"+str(pt_pin)+"的Cookies成功！当前共有："+str(i-1)+"个Cookies")
            except Exception as error:
                await jdbot.send_message(chat_id,"更新"+str(pt_pin)+"的Cookies失败，请重试！")
        else:
            try:
                open(_config, 'a', encoding='utf-8').write('\n' + "Cookie" + str(i) + "=\"" + event.text + "\"")
                await jdbot.send_message(chat_id,"添加"+str(pt_pin)+"的Cookies成功！当前共有："+str(i)+"个Cookies")
            except Exception as error:
                await jdbot.send_message(chat_id,"添加"+str(pt_pin)+"的Cookies失败，请重试！")
