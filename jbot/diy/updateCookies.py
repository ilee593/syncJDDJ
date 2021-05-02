from telethon import events
from .. import jdbot,chat_id,_ConfigDir
_config = _ConfigDir + '/config.sh'
#自动替换/增加Cookies
#https://github.com/hysbeta/jddockerbot/jbot/diy/updateCookies.py
#用法：
#1.部署updateCookies.py到diy文件夹下
#2.从其他途径或SuMaiKaDe/jddockerbot的bot处获取Cookies
#3.发送Cookies给bot即可实现自动替换/增加Cookies

@jdbot.on(events.NewMessage(chats=chat_id,pattern=('pt_key=')))
async def updateCookies(event):
    #加载config.sh文件内容
    config = open(_config, 'r', encoding='utf-8').readlines()
    config_text = open(_config, 'r', encoding='utf-8').read()
    #获取当前Cookie数
    i = 1
    while "Cookie" + str(i) in config_text:
        i = i + 1
    #分离pt_pin用于匹配
    pt_pin = event.text.split(";")[1]
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
