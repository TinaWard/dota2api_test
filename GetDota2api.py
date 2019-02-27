import dota2api
from dota2api.src.exceptions import APIError, APITimeoutError
api = dota2api.Initialise("HERE_YOUR_CODE", raw_mode=True)
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import re
import pandas as pd
import numpy as np
import requests
import time
def readystate_complete(d):
    return d.execute_script("return document.readyState") == "complete"

url = "https://dotabuff.com/matches?game_mode=all_pick&skill_bracket=very_high_skill"
driver = webdriver.Firefox()
driver.get(url)
WebDriverWait(driver, 30).until(readystate_complete)
time.sleep(1)
htmltext = driver.page_source
matches = re.compile('<a href="/matches/(.*?)">' , re.DOTALL | re.IGNORECASE).findall(str(htmltext))

infolist = []
for index in range(len(matches)):
    info = api.get_match_details(match_id=int(matches[index]))
    infolist.append(info)
    print(index)

df = pd.DataFrame(index = range(len(infolist)))
df['radiant'] = pd.NaT
df['dire']    = pd.NaT
df['win']    = pd.NaT
index = 0
for info in infolist:
    df['radiant'][index] = info['radiant_score']
    df['dire'][index] = info['dire_score']
    df['win'][index] = info['radiant_win']
    index = index + 1