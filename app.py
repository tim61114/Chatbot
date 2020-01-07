import requests 
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

    

def apple_news2():
    target_url = 'https://tw.appledaily.com/new/realtime'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = ""
    for index, data in enumerate(soup.select('div.item a')):
        if index ==6:           
            return content
        print(data)  
        title = data.find('img')['alt']
        link =  data['href']
        link2 = 'https:'+ data.find('img')['data-src']
        content+='{}\n{}\n{}\n'.format(title,link,link2)
    return content  





from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('/pheE+LAP0oYmg3Le0uu+KhlnJ41bbMqeHawIL8OiN0PQGSswT3+foNk05WGaFoA7f8gtPKA7WF5McAdK4MeBZQD0VeqVsgSNPzzxgKrGTzWo5666PnilWpVU+shiN5S9fqbD8e/HZ8fxois5yFhJAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('9e0c2041f6ff1d49250b94fc5a0a8590')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


    

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    text=event.message.text
    def send(reply_text):
        message = TextSendMessage(reply_text)
        line_bot_api.reply_message(event.reply_token, message)

    if (text=="Hi"):
        reply_text = "Hello"
        send(reply_text)
        #Your user ID

    elif(text=="你好"):
        reply_text = "哈囉"
        send(reply_text)
        
    elif(text=="機器人"):
        reply_text = "叫我嗎"
        send(reply_text)
        
    elif(text=="嵐嵐"):
        reply_text = "可愛"
        send(reply_text)
        
    elif(text=="范范"):
        reply_text = "好臭"
        send(reply_text)
        
    elif(text=="test"):
        reply_text = "testtest123"
        send(reply_text)
        
    elif(("我要去")in text):
        text.strip("我要去")
    
    elif(("天氣") in text):
        text.raisestrip("天氣")
        text.replace(" ","")
        reply_text = text
        send(reply_text)
        
    elif('dic' in text and 'mdic' not in text):
        a = text.split(' ')
        res = requests.get('http://tw.dictionary.search.yahoo.com/search?p='+a[1])
        print(res.status_code)
        soup = BeautifulSoup(res.content,'html.parser')
        meaning = soup.find_all('div',attrs={'class':'grp grp-tab-content-explanation tabsContent tab-content-explanation tabActived'})
        outputstring = a[1]+"\n"
        for i in meaning:
            turn_into_string = str(i.text)
            
            outputstring += (i.text + '\n')
            count=1
        #outputstring += '\nSynonyms and Antonyms \n'
        #for i in synant:
            #outputstring += (i.text +'\n')
        
        reply_text = outputstring
        send(reply_text)
        
    elif('mdic' in text):
        a = text.split(' ')
        res = requests.get('https://www.merriam-webster.com/dictionary/'+a[1])
        print(res.status_code)
        soup = BeautifulSoup(res.content,'html.parser')
        meaning = soup.find_all('div',attrs={'class':'vg'})
        outputstring = a[1]+"\n"
        for i in meaning:
            print(i.text)
            outputstring += (i.text + '\n')
            count=1
            
        reply_text = outputstring
        send(reply_text)
    
    elif (("新聞") in text):
        a=apple_news2()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))    
        
    else:
        reply_text = text
        send(reply_text)
     
    #message = TextSendMessage(reply_text)
    #line_bot_api.reply_message(event.reply_token, message)
    

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
