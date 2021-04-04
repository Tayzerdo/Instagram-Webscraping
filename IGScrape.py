# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 09:08:34 2021

@author: Asus
"""

from selenium.webdriver import Chrome
from instascrape import *
import pandas as pd
from datetime import datetime
import logging

def scrapePosts(username,numberposts):
    # Creating our webdriver
    webdriver = Chrome("chromedriver.exe")
    
    # Scraping the profile
    SESSIONID = 'xxx'
    headers = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
               "cookie": f"sessionid={SESSIONID};"}
    Insta = Profile(username)
    Insta.scrape(headers=headers)

    # Scraping the posts
    try:
        posts = Insta.get_posts(webdriver=webdriver, amount=numberposts, login_first=True, scrape=True, scrape_pause=3)
        # scraped_posts, unscraped_posts = scrape_posts(posts, headers=headers, pause=10)
    except:
        logging.warn("Error with instagram login")
    return posts

def savePostInfo(posts):
    instaIDs = []
    post=[]
    #save the posts info into csv files and the IDlists
    for post in posts:
        post.to_csv(f"./data/{post['shortcode']}.csv")
        instaIDs.append(post['shortcode'])
    #Create Dataframe with the ID's list
    IDlist = pd.DataFrame(instaIDs, columns=["IDs"])
    #Save the Insta IDs into a csv file
    IDlist.to_csv("./data/IDs.csv")
    logging.warn("Error to save the posts")
    return instaIDs, IDlist

def createDataFrame(instaIDs):
    infoDF=pd.DataFrame()
    #Create a DataFrame with the posts info
    for i in instaIDs:
        a = pd.read_csv("./data/"+i+".csv")
        b = list(a[a.columns[0]])
        infoDF=infoDF.append([a[a.columns[1]]])
    postinfo = pd.DataFrame(infoDF)
    postinfo.set_axis(b, axis=1, inplace=True)
    postinfo.reset_index(drop=True, inplace=True)
    postinfo["hashtags"] = postinfo["hashtags"].str.lower()
    return postinfo


def hashtagList(postinfo):
    hashtag = []
    #Create the unique hashtag list
    for i in postinfo["hashtags"]:
        c = i.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
        c = list(c.split(","))
        c = list(filter(None, c))
        for j in c:
            if j not in hashtag:
                hashtag.append(j)
    
    hashtag=sorted(hashtag)
    hashtag = [each_string.lower() for each_string in hashtag]
    return hashtag

def createDict(hashtag,postinfo):
    dictLikes = {}
    #Create a dict to save the sum of likes, number of posts and the hashtag ratio for each hashtag
    for i in hashtag:
        sumLikes=0
        numPosts=0
        for j in range(0,len(postinfo)):
            if str(i) in postinfo.loc[j]["hashtags"]:
                numPosts=numPosts+1
                sumLikes = sumLikes+int(postinfo.loc[j]["likes"])
        dictLikes[i] = [sumLikes,numPosts,sumLikes/numPosts]

    df1 = pd.DataFrame.from_dict(dictLikes,orient="index")
    df1.index = df1.index.set_names(['HashtagNames'])
    df1.reset_index(inplace=True)
    df1 = df1.rename(columns={0:"HashtagLikes",1:"HashtagPosts",2:"HashtagRatio"})
    df1 = df1.sort_values(by='HashtagLikes', ascending=False)
    df1.reset_index(drop=True, inplace=True)
    return df1

def top10Hashtags(df1):
    #Create a DF with the top10 liked hashtag
    mostLikedHashtag = list(df1['HashtagNames'])
    mostLikedHashtag = mostLikedHashtag[:9]
    
    quantity = {}
    for i in mostLikedHashtag:
        try:
            google_hashtag = Hashtag(i)
            google_hashtag.scrape()
            quantity[i] = google_hashtag.amount_of_posts
        except:
            logging.warn("Instagram error login")
            break
    
    Liked = pd.DataFrame.from_dict(quantity,orient="index")
    Liked = Liked.rename(columns={0:"Quantity"})
    Liked.reset_index(inplace=True)   
    df2 = pd.concat([df1, Liked["Quantity"]], join = 'outer', axis = 1, sort = False)
    return df2

def saveAllInfo(username,IDlist,postinfo,df1,df2):
    with pd.ExcelWriter("./data/info_"+username+".xlsx") as writer:  
        IDlist.to_excel(writer, sheet_name='ID_info')
        postinfo.to_excel(writer, sheet_name='All_Info')
        df1.to_excel(writer, sheet_name='Hashtag_info')
        df2.to_excel(writer, sheet_name='AllHashtag_info')


def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logging.info(f'Started at {datetime.now().strftime("%y/%m/%d %H:%M:%S")}')
    username = "clicktays"
    numberposts=2
    
    logging.info("STEP 1")
    posts = scrapePosts(username,numberposts)
    logging.info("STEP 2")
    instaIDs, IDlist = savePostInfo(posts)
    logging.info("STEP 3")  
    postinfo = createDataFrame(instaIDs)
    logging.info("STEP 4")    
    hashtag = hashtagList(postinfo)
    logging.info("STEP 5") 
    df1 = createDict(hashtag,postinfo)
    logging.info("STEP 6")
    df2 = top10Hashtags(df1)
    logging.info("STEP 7")
    saveAllInfo(username,IDlist,postinfo,df1,df2)
    logging.info("Process finished without issues")
    
if __name__ == "__main__":
    main()