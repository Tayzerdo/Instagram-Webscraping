# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 14:03:47 2021

@author: Asus
"""

#STEP 0 / Import libraries
import pandas as pd
import time
from selenium.webdriver import Chrome
from instascrape import *
from datetime import datetime

#Create the tuple days of the week to return the day of the week based on the date
dayOfWeek = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")

#STEP 1 - Get the most recent posts
number = int(input("Provide the number of post you want to extract it: "))
username = input("Provide the Instagram username: ", )
# number = 100
# username = 'tayzerdo'

#Go to Instagram username page, to retrieve the pictures id to be able to store each post link
lastlink = url = "https://www.instagram.com/" + username + "/"
browser = Chrome()
browser.get(url)
post = "https://www.instagram.com/p/"
post_links = []
while len(post_links) < number:
    print(len(post_links))
    scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
    browser.execute_script(scroll_down)
    try:
        links = [a.get_attribute('href') for a in browser.find_elements_by_tag_name('a')]
        firstposition = links.index(lastlink)
        lastposition = links.index("https://www.instagram.com/")
        print("The position for the last link is: ",firstposition, "and the last position is: ",lastposition)
        links = links[firstposition:lastposition+1]
        try:
            print(links)
            print("")
            print("")
            for link in links:
                print("for loop", link)
                if post in link and link not in post_links:
                    post_links.append(link)
                    lastlink = link
                    print("internal number",len(post_links))
                    # if len(post_links) == number:
                        # break
                time.sleep(10)
            else:
                post_links = post_links[:number]
        except:
            print("Some problem occurred")
    except:
        print("Error with the login part")
        break
        
# browser.close()
print("-----------------------------------------")
print("The number of links are ",len(post_links))
print("-----------------------------------------")
#STEP 2 - Create the pandas table to save the informatin of the posts
aux = pd.DataFrame(columns=["date","time","comments","likes","is_video","Post link","Caption"])
instaUrls = post_links
print(instaUrls) 
print("") 

#Take the information of the posts to scrape and extract the information to save in a DataFrame
for i in instaUrls:
    try:
        print(i)
        google_post = Post(i)
        google_post.scrape()
        dateinfo = datetime.fromtimestamp(google_post.timestamp).isoformat()
        dateinfo = dateinfo.split("T")
        print(dateinfo[0],"  ",dateinfo[1][:5],"  ",google_post.comments, "  ",google_post.likes, "  ",google_post.is_video)
        print("")
        aux = aux.append({"date":dateinfo[0],
                          "time":dateinfo[1][:5],
                          "comments":google_post.comments,
                          "likes":google_post.likes,
                          "is_video":google_post.is_video,
                          "Post link":i,
                          "Caption":google_post.caption},ignore_index=True)
        time.sleep(10)
    except:
        print("Some problem occurred")
    
print(aux)

##Save the information into Excel file
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(username+" Instagram Info.xlsx", engine='xlsxwriter')

# Write each dataframe to a different worksheet.
aux.to_excel(writer, sheet_name='Posts info')

# Close the Pandas Excel writer and output the Excel file.
writer.save()