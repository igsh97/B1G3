from flask import Flask, render_template, request, jsonify, after_this_request,redirect,url_for
app = Flask(__name__)
from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://sparta:test@cluster0.eh7wfh6.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

# @app.after_request
# def add_no_cache_header(response):
#     print("No cache")
#     response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
#     response.headers['Pragma'] = 'no-cache'
#     response.headers['Expires'] = '0'
#     return response

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/hyelee')
def hyelee():
   return render_template('hyelee.html')

@app.route("/comment", methods=["POST"])
def guestbook_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    doc = {
        'name':name_receive,
        'comment':comment_receive
    }
    db.hyelee.insert_one(doc)
    
    return jsonify({'msg': '저장 완료!'})

@app.route("/comment", methods=["GET"])
def guestbook_get():
    all_fans = list(db.hyelee.find({},{'_id':False}))
    return jsonify({'result': all_fans})

@app.route("/delete", methods=["POST"])
def guestbook_delete():
    recieve_comment = request.form['give_comment']
    print(recieve_comment)

    db.hyelee.delete_one({'comment': recieve_comment})
    return jsonify({'msg': '삭제 완료'})

@app.route("/rewrite", methods=["POST"])
def guestbook_rewrite():
    recieve_comment = request.form.get('re_comment',False)
    print("recieve_comment :%s"%recieve_comment)

    if(recieve_comment==False):
       return jsonify({'msg':'값을 입력하십시오'})
    
    rewrite_comment = request.form.get('comment_rewrite',False)
    print("rewrite_comment :%s"%rewrite_comment)

    db.hyelee.update_one({'comment':recieve_comment},{'$set':{'comment':rewrite_comment}})
    return jsonify({'msg': '업데이트 완료'})

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


@app.route('/signIn', methods=["GET","POST"])
def sign_in():
   id_log = request.form.get('id_log', False)
   pwd_log = request.form.get('pwd_log', False)

   id = db.user.find_one({'id':id_log})
   pwd = db.user.find_one({'pwd':pwd_log})

   if(id and pwd):
      print("success")
      @after_this_request
      def add_no_cache_header(response):
          response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
          response.headers['Pragma'] = 'no-cache'
          response.headers['Expires'] = '0'
          return response
      #return redirect('/webstagram')
      return jsonify({'msg':'로그인 성공!'})
   #다른 페이지로 redirect
      
   else:
      print("fail")
      return jsonify({'msg':'사용자를 찾지 못했습니다. 회원가입을 진행해주세요.'})

@app.route('/profile', methods=["POST"])
def profile_post():
   name_receive=request.form['name_give']
   mbti_receive=request.form['mbti_give']
   hobby_receive=request.form['hobby_give']
   profile_receive=request.form['profile_give']
   feed_receive=request.form['feed_give']
   comment_receive=request.form['comment_give']

   doc = {
      'name':name_receive,
      'mbti':mbti_receive,
      'hobby':hobby_receive,
      'profile':profile_receive,
      'feed':feed_receive,
      'comment':comment_receive
   }
   db.profiles.insert_one(doc)

   return jsonify({'msg':'Profile 등록 완료!'})

@app.route('/profile', methods=["GET"])
def profile_get():
   all_profiles = list(db.profiles.find({},{'_id':False}))
   
   return jsonify({'result':all_profiles})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5001, debug=True)
