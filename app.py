from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

client = MongoClient('mongodb+srv://sparta:test@cluster0.xi1pqvv.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta
application = app = Flask(__name__)
app.secret_key = 'any random string'

@app.route('/')
def home():
    id= session.get('id',None)
    return render_template('index.html',id=id)

@app.route('/write')
def write():
    if 'id' in session:
        id= session.get('id',None)
        return render_template('write.html',id=id)
    return render_template('login.html')

@app.route('/view')
def view():
    id= session.get('id',None)
    return render_template('index.html',id=id)

@app.route('/myview')
def myview():
    if 'id' in session:
        id= session.get('id',None)
        return render_template('myview.html',id=id)
    return render_template('login.html')

@app.route('/mypage')
def mypage():
    if 'id' in session:
        id= session.get('id',None)
        return render_template('mypage.html',id=id)
    return render_template('login.html')

@app.route('/join')
def join():
    return render_template('join.html')

@app.route('/join_done', methods=['POST'])
def join_done():
    email = request.form['email_give']  
    name = request.form['name_give']
    userID = request.form['id_give']
    pwd = request.form['pwd_give']

    # MongoDB의 값중에 회원가입에 기입한 ID이 존재하는지 확인하기
    user = db.users.find_one({'id': userID})

    if user:  # 이미 존재하는 경우 (True)
        return jsonify({'msg': '아이디 중복불가. 다시 입력하세요.'})
    else:
        # MongoDB에 데이터 저장
        doc = {
            'email': email,
            'name': name,
            'id': userID,
            'pwd': pwd
        }
        db.users.insert_one(doc)
        return jsonify({'msg': '회원 가입이 완료되었습니다.'})
    

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['id'] = request.form['id']
        id= session.get('id',None)
        return render_template('index.html',id=id)
    return render_template('login.html')


@app.route('/logout', methods=["GET"])
def logout():
    session.pop('id', None)
    return render_template('index.html')



@app.route("/writediary", methods=['GET','POST'])
def writediary_post():
    if request.method == 'POST':
        name_receive = request.form['name_give']
        comment_receive = request.form['comment_give']
        private_receive = request.form['private_give']
        emoji_receive = request.form['emoji_give']

        doc = {
            'name':name_receive,
            'comment':comment_receive,
            'private':private_receive,
            'emoji':emoji_receive,
        }
        db.diary.insert_one(doc)

        return jsonify({'msg': '전송완료!'})
    all_comments = list(db.diary.find({},{'_id':False}))
    return jsonify({'result': all_comments})

if __name__ == '__main__':
    app.run()