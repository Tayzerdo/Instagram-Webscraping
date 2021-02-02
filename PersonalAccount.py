# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 14:03:47 2021

@author: Asus
"""

import pandas as pd
import time
from selenium.webdriver import Chrome
from instascrape import *
from datetime import datetime
timenow = datetime.now()
dayOfWeek = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")

#Get the most recent posts
# number = input("Provide the number of post you want to extract it: ")
number = 50
username = 'tayzerdo'

#Instagram information
profile = Profile(username)
profile.scrape()
print(f"The number of people that {username} is following are {profile.following}")
print(f"\nThe number of people that {username} as followers are {profile.followers}")
print(f"\nThe profile biography is:\n {profile.biography}")

# def recent_posts(username):
url = "https://www.instagram.com/" + username + "/"
browser = Chrome()
browser.get(url)
post = "https://www.instagram.com/p/"
post_links = []
while len(post_links) < number:
    scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
    browser.execute_script(scroll_down)
    links = [a.get_attribute('href') for a in browser.find_elements_by_tag_name('a')]
    print("")
    print("")
    print(links)
    for link in links:
        if post in link and link not in post_links:
            post_links.append(link)
            print(len(post_links))
            if len(post_links) == number:
                break
        time.sleep(10)
    else:
        post_links = post_links[:number]
# browser.close()
print("-----------------------------------------")
print(post_links)

aux = pd.DataFrame(columns=["date","time","comments","likes","is_video","Weekday"])
instaUrls = post_links
print(instaUrls) 
print("") 

for i in instaUrls:
    print(i)
    google_post = Post(i)
    google_post.scrape()
    dateinfo = datetime.datetime.fromtimestamp(google_post.timestamp).isoformat()
    dateinfo = dateinfo.split("T")
    print(dateinfo[0],"  ",dateinfo[1],"  ",google_post.comments, "  ",google_post.likes, "  ",google_post.is_video)
    print("")
    aux = aux.append({"date":dateinfo[0],
                      "time":dateinfo[1][:5],
                      "comments":google_post.comments,
                      "likes":google_post.likes,
                      "is_video":google_post.is_video,
                      "Weekday":dayOfWeek[dateinfo[1].weekday()]},ignore_index=True)


print(aux)
aux.to_excel(username+" Instagram Info.xlsx")