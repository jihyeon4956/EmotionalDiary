from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify

client = MongoClient('mongodb+srv://sparta:test@cluster0.xi1pqvv.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta
application = app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/join')
def join():
    return render_template('join.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/write')
def write():
    return render_template('write.html')

@app.route('/view')
def view():
    return render_template('view.html')

@app.route('/mypage')
def mypage():
    return render_template('mypage.html')


@app.route("/guestbook", methods=["POST"])
def guestbook_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    doc = {
        'name':name_receive,
        'comment':comment_receive
    }
    db.fan.insert_one(doc)

    return jsonify({'msg': '전송완료!'})

@app.route("/guestbook", methods=["GET"])
def guestbook_get():
    all_comments = list(db.fan.find({},{'_id':False}))
    return jsonify({'result': all_comments})

if __name__ == '__main__':
    app.run()