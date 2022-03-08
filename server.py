from flask import Flask, request
import threading
import os
import random
import time
import string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import requests
from multiprocessing import Process
import pandas as pd
import queue
import sys
import subprocess

q=queue.Queue()

lower_case = string.ascii_lowercase
app = Flask('server()', static_url_path='')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

chrome_options = Options()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux i686; rv:77.0) Gecko/20100101 Firefox/77.0")

qr_code = "To use WhatsApp on your computer:"
session_status = {}

# A global driver helps to avoid scanning qr code again and again
driver = webdriver.Chrome(executable_path="chromedriver.exe",
                          options=chrome_options)

try:
    os.mkdir("static")
except:
    pass


def openImage(path):
    imageViewerFromCommandLine = {'linux':'xdg-open',
                                  'win32':'explorer',
                                  'darwin':'open'}[sys.platform]
    subprocess.run([imageViewerFromCommandLine, path])

def macro(message, number):
    driver.get(f"https://web.whatsapp.com/send?phone={number}&text={message}")
    #time.wait(2)
    #.\_1E0Oz > span
    while (1>0):
       try:
            driver.find_element_by_css_selector(".\_1E0Oz > span").click()
            break
       except:
            try:
                driver.find_element_by_css_selector(".VtaVl").click()
                break
            except:
                pass
            pass

    #driver.find_element_by_css_selector(".\_2_1wd").clear()
    #driver.find_element_by_css_selector(".\_2_1wd").send_keys(number+Keys.ENTER)
    #time.sleep(2)
    #ActionChains(driver).send_keys(message+Keys.ENTER).perform()


@app.route("/queue")
def que():
    number = request.args.get("num")
    message = request.args.get("message")
    '''
    delay = request.args.get("delay")

    try:
        session_id = request.args.get("session")
    except:
        for i in range(6):
            session_id = session_id + random.choice(lower_case)
    '''

    q.put({'0':number, '1':message,})       # '2':delay, '3':session_id})

    return "ok"

@app.route("/send")
def sendmsg():
    #print("Hi")
    prevnum=""
    while q.empty()==False:
        item=q.get()
        #print(item)
        number = item['0']
        message = item['1']

        #delay = item['2']
        #session_id = item['3']
        if prevnum==number:
            ActionChains(driver).send_keys(message + Keys.ENTER).perform()
        else:
            macro(message, number)
        prevnum = number
        time.sleep(1)
    driver.quit()
    return "ok"


def server():
    # driver.get(f"https://web.whatsapp.com")

    app.run(host='127.0.0.1', port='5050')


def client(number, message, file, delay, session_id, a, b, c):

    if session_id == 0:
        for i in range(6):
            session_id = session_id + random.choice(lower_case)

    driver.get(f"https://web.whatsapp.com")

    try:
        rf = pd.read_csv(file).to_dict('list')
    except:
        pass
    key = list(rf.keys())
    while 1>0:
       if qr_code in driver.page_source:
           time.sleep(3)
           driver.save_screenshot('static/%s.png' % session_id)
           im = os.getcwd() + "\\static\\" + session_id + ".png"
           openImage(im)
           break

    print(rf)
    time.sleep(int(delay-4))

    a,b,c=key[a],key[b],key[c]

    if file != "false":

        for no,name,msg in zip(rf[a],rf[b],rf[c]):
            print(no, name ,msg)
            if pd.isna(msg) and pd.isna(name):
              mess = message.replace("<>","Sir/Ma'am")
            elif pd.isna(msg):
              mess = message.replace("<>",name)
            else:
              mess = msg.replace("<>",name)
            if mess == "":
                continue
            requests.get(f"http://127.0.0.1:5050/queue?num={no}&message={mess}&delay={delay}&session={session_id}")
            time.sleep(1)

    else:
        requests.get(f"http://127.0.0.1:5050/queue?num={number}&message={message}&delay={delay}&session={session_id}")
    requests.get(f"http://127.0.0.1:5050/send?arg=ok")




def main(message="", file="no.csv", delay=10, number=0, session_id=0, a=0, b=1, c=2):

    server1 = threading.Thread(target=server).start()
    time.sleep(8)
    client1 = threading.Thread(target=lambda: client(number, message, file, delay, session_id, a, b, c)).start()

