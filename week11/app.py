from flask import Flask, render_template, request, redirect
import pymongo

app = Flask(__name__)
myclient = pymongo.MongoClient("mongodb://db3.local:27017/", replicaset="rs0")

mydb = myclient["mydatabase"]
mycol = mydb["messages"]


@app.route('/', methods=['GET', 'POST'])
def sessions():
    if request.method == "POST":
        x = mycol.insert_one(dict(request.form))
        return redirect("/")
    data = mycol.find().limit(10)
    return render_template('session.html', data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
