from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

client = MongoClient('mongodb+srv://sparta:test@cluster0.xi1pqvv.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta
application = app = Flask(__name__)
app.secret_key = 'any random string'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/write')
def write():
    if 'id' in session:
        return render_template('write.html')
    return render_template('login.html')

@app.route('/view')
def view():
    return render_template('index.html')

@app.route('/myview')
def myview():
    if 'id' in session:
        return render_template('myview.html')
    return render_template('login.html')

@app.route('/mypage')
def mypage():
    if 'id' in session:
        return render_template('mypage.html')
    return render_template('login.html')

@app.route('/join')
def join():
    return render_template('join.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['id'] = request.form['id']
        return render_template('index.html')
    return render_template('login.html')

@app.route('/logout', methods=["GET"])
def logout():
    session.pop('id', None)
    return render_template('index.html')

@app.route("/guestbook", methods=['GET','POST'])
def guestbook_post():
    if request.method == 'POST':
        name_receive = request.form['name_give']
        comment_receive = request.form['comment_give']
        doc = {
            'name':name_receive,
            'comment':comment_receive
        }
        db.fan.insert_one(doc)

        return jsonify({'msg': '전송완료!'})
    all_comments = list(db.fan.find({},{'_id':False}))
    return jsonify({'result': all_comments})

if __name__ == '__main__':
    app.run()