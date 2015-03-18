import requests
from lxml import html
import time
import os
from postmark import PMMail

TRACKING_CODE = os.environ.get('TRACKING_CODE')
SLEEP_TIME = int(os.environ.get('SLEEP_TIME')) * 60
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
RECV_EMAIL = os.environ.get('RECV_EMAIL')
POSTMARK_API_TOKEN = os.environ.get('POSTMARK_API_TOKEN')

loop = True

def get_status():
    address = 'http://www.poste.it/online/dovequando/ricerca.do'
    payload = {'mpcode': TRACKING_CODE, 'mpdate': '0', 'findCap': 'Esegui la ricerca'}
    r = requests.post(address, payload)
    pageReady = r.text
    data = html.document_fromstring(pageReady)
    status = data.xpath('//div[@class="statoDoveQuandoLavorazione"]/ul/li/text()')
    try:
        return status[0]
    except:
        status = data.xpath('//div[@class="statoDoveQuandoConsegnato"]/ul/li/text()')
        return status[0]

old_status = get_status()
print("Init: " + str(old_status))
time.sleep(SLEEP_TIME)

while loop:
    status = get_status()
    print("Check..")
    if status != old_status:
        message = PMMail(api_key = POSTMARK_API_TOKEN,
           subject = "Update tracking poste.it",
           sender = SENDER_EMAIL,
           to = RECV_EMAIL,
           text_body = status
           )
        print("Update! Sending email..")
        message.send()
        old_status = status
        if "Consegnato" in status:
            print("Delivered! Exiting..")
            loop = False
    else:
        print("Nothing new.. Sleep.")
        time.sleep(SLEEP_TIME)