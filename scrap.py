#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests,sys
from bs4 import BeautifulSoup as soup
from pymongo import MongoClient

gctr=0



client = MongoClient("localhost")

db = client["socialnews"]

collection = db["actresses"]


# In[ ]:


def urlToHtml(url):
    html = soup(requests.get(url).text,"html.parser")
    return html


# In[ ]:


def dateConversion(dt):
    
    splitdt = dt.split()
    
    
    monthVals = {"jan":"01","feb":"02","march":"03","april":"04","may":"05","june":"06","july":"07","august":"08","sept":"09","oct":"10",
                "nov":"11","dec":"12"}
    for month,val in monthVals.items():
        if month in dt.lower():
            year = splitdt[-1].strip()
            date = "%02d" % int(splitdt[1].strip().replace(",",""))
            timestamp = str(year)+str(val)+str(date)
    return int(timestamp)-gctr


# In[ ]:


def articleToRecord(article):
    global gctr

    postId = article.get("class")[2]
    print(postId)
    
    thumbnail = article.find("img").get("data-large-file").split("?fit=")[0]
    print(thumbnail)
    
    title = article.find("img").get("data-image-title").split(".")[0]
    print(title)
    
    link = article.find("a").get("href")
    
    date = article.find("span",{"class":"entry-meta-date updated"}).text
    
    rec = {
        "_id":postId,
        "img":thumbnail,
        "title":title,
        "link":link,
        "date":dateConversion(date),
        "textDate":date,
        "viewed":False
    }
    gctr+=1
    try:
        collection.insert_one(rec)
        print(title," inserted")
    except Exception as e:
        print(e)
        sys.exit(0)
    return True
    


# In[ ]:


def scrap(html):
    mainContent = html.find("div",{"id":"main-content"})
    articles = mainContent.findAll("article")
    print(len(articles))
    for article in articles:
        if not articleToRecord(article):
            break


# In[ ]:


for pgno in range(1,395):
    print(pgno)
    html = urlToHtml("https://www.socialnews.xyz/category/gallery/actresses/page/{}/".format(str(pgno)))
    scrap(html)


# In[ ]:





# In[ ]:




