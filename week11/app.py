import datetime

from flask import Flask, render_template, request, redirect
import pymongo

app = Flask(__name__)
myclient = pymongo.MongoClient("mongodb://db1.local:27017, db2.local:27017, db3.local:27017",
                               replicaset="rs0")

mydb = myclient["mydatabase"]
mycol = mydb["messages"]


@app.route('/', methods=['GET', 'POST'])
def sessions():
    if request.method == "POST":
        message = dict(request.form)
        if message["name"] != "" and message["message"] != "":
            message['timestamp'] = datetime.datetime.now()
            mycol.insert_one(message)
        return redirect("/")
    data = mycol.find().sort("timestamp")
    return render_template('session.html', data=list(data))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
