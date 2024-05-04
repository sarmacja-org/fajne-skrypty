#!/usr/bin/env python3
import re
import os
from six.moves import urllib
from bs4 import BeautifulSoup
import requests
import json
import time
from pprint import pprint

channelID = os.environ["X11_DISCORD_CHANNEL_ID"]
botToken = os.environ["DISCORD_BOT_TOKEN"]

baseURL = "https://discordapp.com/api/channels/{}/messages".format(channelID)
headers = { "Authorization":"Bot {}".format(botToken),
            "User-Agent":"myBotThing (http://some.url, v0.1)",
            "Content-Type":"application/json", }

leagues = [
    ("SLP Ekstraklasa", 1),
    ("SLP Pierwsza Liga", 2),
    ("SLP Druga Liga", 3)
]

for league in leagues:
    message = ""
    resp = urllib.request.urlopen('http://xperteleven.com/standings.aspx?Lid=71065&Sel=T&Lnr={}&dh=2'.format(league[1]))
    rawhtml = resp.read()
    soup = BeautifulSoup(rawhtml , 'html.parser')

    div_last_round = soup.find('div', attrs={'class' : 'section'})
    #print(div_last_round)
    rx_date = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}")
    field = 0
    matches = []

    for x in div_last_round.find_all('td'):
        text_value = x.text.strip()
        if rx_date.match(text_value):
            field = 0
            match_data = []
        else:
            field = field + 1
        
        match_data.append(text_value)
        if field == 4:
            matches.append(match_data)

    message = ":soccer: [Wyniki {}]\n".format(league[0])

    for m in matches:
        message = "{}{} - {} {}\n".format(message, m[1], m[3], m[4])

    POSTedJSON =  json.dumps ( {"content": message} )
    pprint(message)
    r = requests.post(baseURL, headers = headers, data = POSTedJSON)
    time.sleep(2)
