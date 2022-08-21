#!/usr/bin/env python3
import requests
import json
import os
import subprocess
from bs4 import BeautifulSoup

def loadSubs(subs):
    subList = []
    with open(subs, "r") as f:
        for sub in f:
            subList.append(sub[:-1])
    return subList

def getVideoLinks(subReddit):
    links = []
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'}
    response = requests.get('https://reddit.com' +
            subReddit + '.json', headers=headers)
    data = response.json()
    posts = data["data"]["children"] #list of dictionaries
    for post in posts:
        if post["data"]["is_video"]:
            #print(post["data"]["title"])
            links.append(post["data"]["permalink"])
    return links
    

def getHLSFileLinks(links):
    videoLinks = []
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'}
    for link in links:
        response = requests.get('https://reddit.com' + link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        videoLinks.append(soup.source['src'])
    return videoLinks

def playVideos(links):
    for link in links:
        subprocess.call(['ffplay', link])


subs = loadSubs("subs.txt")
links = []
for sub in subs:
    links += getVideoLinks(sub)
videoLinks = getHLSFileLinks(links)

playVideos(videoLinks)
