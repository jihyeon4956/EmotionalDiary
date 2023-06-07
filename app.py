from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import re

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

# join의 경우 GET과(/join) POST를(/join_done) 나눠서 작성함.
@app.route('/join')
def join():
    return render_template('join.html')


# 이메일 유효성 검사 함수(re) - 
# 참고) import re 등록해야 사용가능함
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

@app.route('/join_done', methods=['POST'])
def join_done():
    email = request.form['email_give']  
    name = request.form['name_give']
    userID = request.form['id_give']
    pwd = request.form['pwd_give']

    # 모든 필드가 비어있지 않은 조건을 걸어준다(is not null)
    if email and name and userID and pwd:
        # 중복체크: 이미 존재하는 id 또는 email값 확인, 둘중 하나라도('$or') 해당될 경우 재입력
        user = db.users.find_one({'$or': [{'id': userID}, {'email': email}]})

        # user가 비어있지 않다 = MongoDB에 이미 해당값이 있다(= 입력 ID중복)
        if user:
            return jsonify({'msg': '아이디 또는 이메일이 이미 사용 중입니다. 다시 입력하세요.'})
        else:
            # 이메일 유효성 검사
            if not is_valid_email(email):
                return jsonify({'msg': '유효한 이메일 형식이 아닙니다. 다시 입력하세요.'})

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
            
    else:
        return jsonify({'msg': '모든 정보를 입력하세요.'})




# login의 경우 if를 이용하여 GET과 POST를 한번에 작성했다.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userID = request.form['loginID']
        password = request.form['loginPW']

        user = db.users.find_one({'id': userID, 'pwd': password})
        
        if user is not None:
            session['id'] = user['id']
            return jsonify({'msg':"로그인 성공!!"})
        else:
            return jsonify({'msg': "로그인 정보가 유효하지 않습니다."})
            
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