from __future__ import unicode_literals

import os
import sys
import redis
import requests
import bs4


from datetime import datetime

from PIL import Image
from io import BytesIO

from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, VideoMessage, FileMessage, StickerMessage, StickerSendMessage
)
from linebot.utils import PY3

from bs4 import BeautifulSoup


app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

# obtain the port that heroku assigned to this app.
heroku_port = os.getenv('PORT', None)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=['POST'])

def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if isinstance(event.message, TextMessage):
            handle_TextMessage_forSearch(event)
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

    return 'OK'

def quit():
    print("Thanks for using")
    sys.exit(0)

def handle_TextMessage_forPDF(event):
    HOST = "redis-12230.c15.us-east-1-4.ec2.cloud.redislabs.com"
    PWD = "ejnxK44QJ6MVyhbS2ou93rXLGccl3b7s"
    PORT = "12230" 
    url = "https://www.who.int/docs/default-source/coronaviruse/situation-reports/20200414-sitrep-85-covid-19.pdf?sfvrsn=7b8629bb_4"
    r = redis.Redis(host = HOST, password = PWD, port = PORT)

    if bool(r.get("pdfURL")) == 0:
        res = r.set("newsURL", url)
        r.setex('newsURL', url, 5)
        print(url)
        return url

    else:
        r.get("pdfURL")
        res = r.get("pdfURL")
        print(res)
        return res
        # html = getHTMLText(new_res)
        # msg = forNews(html) 
        # line_bot_api.reply_message(
        # event.reply_token,
        # TextSendMessage(msg)
        # )

def handle_TextMessage_forNew(event):
    HOST = "redis-12230.c15.us-east-1-4.ec2.cloud.redislabs.com"
    PWD = "ejnxK44QJ6MVyhbS2ou93rXLGccl3b7s"
    PORT = "12230" 
    url = "http://www.xinhuanet.com/politics/2020-04/06/c_1125819214.htm"

    r = redis.Redis(host = HOST, password = PWD, port = PORT)
    if bool(r.get("newsURL")) == 0:
        res = r.set("newsURL", url)
        r.setex('newsURL', url, 5)
        print(url)
        html = getHTMLText(url)
        return forNews(html)
        # msg = forNews(html) 
        # line_bot_api.reply_message(
        # event.reply_token,
        # TextSendMessage(msg)
        # )

    else:
        r.get("newsURL")
        res = r.get("newsURL")
        print(res)
        html = getHTMLText(res)
        return forNews(html)



def handle_TextMessage_forPicture(event):
    img_src ="https://www.rivm.nl/sites/default/files/2020-04/niet_gemeld_als_zorgmedewerker.png"
    return img_src
    # msg = img_src
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(msg)
    # )



# Handler function for Text Message
def handle_TextMessage_forSearch(event):
    msg = print(meau = """
 Main meau
 --------------------
 you may want to do some search,please input:'I want to know XXX'
 2:Finding the definition of COVID-19 in Chinese
 3:Return a news about COVID-19 in Chinese
 4:Return a picture
 5:Return a PDF report about COID-19
 6:Quit
 -------------------
""")
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(msg)
        )
    print(event.message.text)
    #msg = 'You said: "' + event.message.text + '" '
    
    sentence = event.message.text
    sentence_cut = sentence.split()
    for i in range(len(sentence_cut)):
        print(sentence_cut[i])
    
    error_Text = "you need to input:'I want to know XXX'"
    if sentence_cut[0] != "I":
        if sentence_cut[0] == '2':
            msg = handle_TextMessage_forDefinition(event)
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(msg)
            )
        elif sentence_cut[0] == '3':
            msg = handle_TextMessage_forNew(event)
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(msg)
            )
        elif sentence_cut[0] == '4':
            msg = handle_TextMessage_forPicture(event)
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(msg)
            )
        elif sentence_cut[0] == '5':
            msg = handle_TextMessage_forPDF(event)
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(msg)
            )
        elif sentence_cut[0] == '6':
            sys.exit(1)
        else:
            print(error_Text)
            msg = error_Text
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(msg)
            )
    elif sentence_cut[1] != "want":
        print(error_Text)
        msg = error_Text
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(msg)
        )
    elif sentence_cut[2] != "to":
        print(error_Text)
        msg = error_Text
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(msg)
        )
    elif sentence_cut[3] != "know":
        print(error_Text)
        msg = error_Text
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(msg)
        )
    else:
        keyword5 = sentence_cut[4]
        print(keyword5)
        try:
            kv = {'user-agent':'Mozilla/5.0', 'q':keyword5}
            r = requests.get("http://www.google.com.hk/search?hl=en&q",params = kv)
            print(r.request.url)
            r.raise_for_status()
            msg = 'The search website is:"' + r.request.url +'" '
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(msg)
            )
        except:
            error_message = "the website is not exit"
            print(error_message)
            msg = error_message
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(msg)
            )
    
def getHTMLText(url):
    try:
        kv = {'user-agent':'Mozilla/5.0'}
        r = requests.get(url,headers = kv, timeout = 30)
        #r = requests.get(url, timeout = 30)
        #r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "fail"
def fillList(ulist, html):
    soup = BeautifulSoup(html, "html.parser")
    #soup.find_all('meta', attrs={"name":"description"})
    description = soup.find(attrs={"name":"description"})['content']
    return description   
    # print(description)

def forNews(html):
    soup = BeautifulSoup(html, "html.parser")
    for p in soup.body.find_all('p'):
        #print(p.text)
        return(p.text)
        

def handle_TextMessage_forDefinition(event):
    uinfo=[]
    url = "https://baike.baidu.com/item/%E6%96%B0%E5%9E%8B%E5%86%A0%E7%8A%B6%E7%97%85%E6%AF%92%E8%82%BA%E7%82%8E/24282529?fromtitle=COVID-19&fromid=24357637&fr=aladdin"
    html = getHTMLText(url)
    return fillList(uinfo,html)
    # msg = fillList(uinfo, html)
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(msg)
    #     )



if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(host='0.0.0.0', debug=options.debug, port=heroku_port)
    

