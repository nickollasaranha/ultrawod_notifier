#!/usr/bin/env python
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to send timed Telegram messages.
This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import os
import time
import datetime
import requests
import logging
import telegram
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BlockingScheduler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

ULTRAWOD_BOT_AUTH = "1677020610:AAFeBJjxqkbPD07QHWFqSMihoTSVd3Go5QQ"
ULTRAWOD_CHAT_ID = "806399286"

ultra_wod_10kg_url = "https://www.ultrawod.com.br/equipamentos-de-treino/lpo-levantamento-de-peso-olimpico/anilhas/anilha-10kg-competition-plate-ultrawod"
ultra_wod_15kg_url = "https://www.ultrawod.com.br/equipamentos-de-treino/lpo-levantamento-de-peso-olimpico/anilhas/anilha-15kg-competition-plate-ultrawod"
ultra_wod_20kg_url = "https://www.ultrawod.com.br/equipamentos-de-treino/lpo-levantamento-de-peso-olimpico/anilhas/anilha-20kg-competition-plate-ultrawod"
ultrawod_eventos = "https://www.ultrawod.com.br/seminovos"

telegram_bot = telegram.Bot(token=ULTRAWOD_BOT_AUTH)
ultra_wod_10kg_msg_sent = False
ultra_wod_15kg_msg_sent = False

# This function will get availability of ultra_wod plates
def check_availability(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    results_1 = soup.find(id="produto_preco")
    results_2 = soup.find(id="produto_nao_disp")

    if results_2.img is not None:
        return False
    else:
        return True

def send_message(msg):
    telegram_bot.sendMessage(chat_id=ULTRAWOD_CHAT_ID, text=msg)
    telegram_bot.sendMessage(chat_id=ULTRAWOD_CHAT_ID, text=r'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCqpeojMBc0E9PMbnkyfQckrULtgodUr5r2Wn26xWZ5j6NcTygx3rG0ROozfBr42RAHLQaZb1nbpv8O5P0jiy/5EeUj7hVFtS5rDhTXlj9TVDXSYtF3zLMMBosi+7GuAOlHxzA+HbCmw2cVDUwrfw379ENJ0jn1sek2+KNnJsng6u0tF3Do0ukM0wBF+u7mej3ZTujB7sS5XhEN4NVFG4ycLIy4/t326hO/WSrbwcUqgNhVlnYJdzsJVTixPTm/ANHaDlg72RQk0UMRZGPFnHfOaSqcllIaQVI9bYBXUp1ASuFkALrtmN4h53RCO2nN/aKk/f6rcJ66C6S34os3c01OLazDuKkA+B+aDIl7wu8GKxfmHQnwt/SYZHWiIsxJIcUIOqCTDcS9jjLwfwYWB7D5VjMxm9aMzenC+sorr7wPE5HoMVVBaavB+953j3CqLXJOJ4508kinzkSVg/1Tq5Ly8uFMMX2m6g9s+N6GZZimaMWXLR8RLso/Mf6f2+9VlcM= ubuntu@ip-172-31-16-207')

def check_eventos():
    page = requests.get(ultrawod_eventos)
    soup = BeautifulSoup(page.content, 'html.parser')

    results_1 = soup.find_all("div", class_="catalog-empty")
    if len(results_1) > 0:
        if "nenhum produto" in results_1[0].text.lower():
            logger.info("Nenhum produto nos eventos")
        else:
            msg = "Algum produto está disponível nos eventos!"
            telegram_bot.sendMessage(chat_id=ULTRAWOD_CHAT_ID, text=msg)

def check_working():
    msg = ""
    logger.info("Checking if still alive")
    if check_availability(ultra_wod_20kg_url):
        msg = "I'm still working @ " + str(time.strftime("%d/%m"))
    else:
        msg = "Guess I'm not working anymore or 20 KG plate is over :("
    send_message(msg)

def check_10kg_url():
    logger.info("Checking 10 kg ultrawod plate")
    if (check_availability(ultra_wod_10kg_url)):
        if (ultra_wod_10kg_msg_sent == False):
            ultra_wod_10kg_msg_sent = True
            logger.info("10 Kg Plate is in stock!")
            sendMessage("10 Kg Plate is in stock!")
    else:
        logger.info("10 Kg Plate is out of stock!") 

def check_15kg_url():
    logger.info("Checking 15 kg ultrawod plate")
    if (check_availability(ultra_wod_15kg_url)):
        if (ultra_wod_15kg_msg_sent == False):
            ultra_wod_15kg_msg_sent = True
            logger.info("15 Kg Plate is in stock!")
            sendMessage("15 Kg Plate is in stock!")
    else:
        logger.info("15 Kg Plate is out of stock!")  

def main():

    update_frequency = 60 # seconds

    scheduler = BlockingScheduler()
    scheduler.add_job(check_10kg_url, 'interval', seconds=update_frequency)
    scheduler.add_job(check_15kg_url, 'interval', seconds=update_frequency)
    scheduler.add_job(check_eventos, 'interval', seconds=update_frequency)
    scheduler.add_job(check_working, 'cron', day="*", hour=5)

    send_message("oie")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == '__main__':
    main()
