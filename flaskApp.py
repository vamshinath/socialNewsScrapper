from flask import Flask, render_template,request,redirect,url_for,Markup
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
import datetime, os


db = client['socialnews']
app = Flask(__name__)
recs=[]
ctr=0
import functools

@app.route("/reboot")
def maston():
    os.system("sh reboot.sh flaskApp.py "+str(os.getpid())+" &")


    return render_template('index.html')


@app.route("/fload")
def fload():

    global recs
    global ctr
    rec = recs.pop(0)

    ctr+=1
    

    db["actresses"].update_one({"_id":rec["_id"]},{"$set":{"viewed":True}})


    return render_template("display.html",rec=rec,left=str(ctr)+"/"+str(len(recs)))

def collectionPage(unVie,searchQ):
    global recs
    
    
    recs = list(db["actresses"].find({"viewed":unVie}))

        #print("search",searchQ)
    if len(searchQ) :
        tmp=[]
        allcomments = ''
        for rc in recs:
            if searchQ.lower() in rc["title"].lower():
                tmp.append(rc)

        recs=tmp
        
    recs = sorted(recs, key=lambda x: x["date"], reverse=True)

    return redirect(url_for('fload'))


def insertURL(url):

    if "http" in url:
        #single(url=url)
        Thread(target=single,args=(url,)).start()
        return "url added"
    else:
        collnm,qry = url.split(",")
        #queryAdd(collnm,qry)
        Thread(target=queryAdd,args=(collnm,qry,)).start()
        return "query add"




@app.route("/consumer", methods=["POST"])
def consumer():
    if request.method == "POST":
        unViewed = request.form["viewed"] != "unViewed"
        searchQuery = request.form["query"]

    #print("to")

    return collectionPage(unViewed,searchQuery)





@app.route("/")
def main():
    return render_template("index.html")



if __name__ == '__main__':
    app.run('0.0.0.0', port=8002)