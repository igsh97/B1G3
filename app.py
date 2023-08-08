from flask import Flask, render_template, request, jsonify, redirect, url_for
app = Flask(__name__)
from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://sparta:test@cluster0.eh7wfh6.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/webstagram')
def webstagram():
   return render_template('instagram.html')

@app.route('/signUp', methods=["POST"])
def sign_up():
   id_receive = request.form['id_give']
   pwd_receive = request.form['pwd_give']

   doc = {
        'id':id_receive,
        'pwd':pwd_receive
    }
   db.user.insert_one(doc)
    
   return jsonify({'msg': '저장 완료!'})


@app.route('/signIn', methods=["POST"])
def sign_in():
   id_log = request.form['id_log']
   pwd_log = request.form['pwd_log']

   id = db.user.find_one({'id':id_log})
   pwd = db.user.find_one({'pwd':pwd_log})


   if(id and pwd):
      print("success")
      redirect(url_for('webstagram'))
      return jsonify({'msg':'로그인 성공!'})
   #다른 페이지로 redirect
      
   else:
      print("fail")
      return jsonify({'msg':'사용자를 찾지 못했습니다. 회원가입을 진행해주세요.'})



if __name__ == '__main__':
   app.run('0.0.0.0', port=5001, debug=True)