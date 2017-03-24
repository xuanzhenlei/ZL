#!/usr/bin/python
#-*- coding:utf-8 -*-

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return '''<h1>Welcom to xxxx!</h1>'''

@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
              <p><text>用户：</text><input name="username"></p>
              <p><text>密码：</text><input name="password" type="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''
@app.route('/register',methods=['GET'])
def register_form():
    return'''<form action="/register" method="post">
             <p><text>用户：</text><input name="username"></p>
             <p><text>密码：</text><input name="fpassword" type="password"></p>
             <p><text>密码：</text><input name="spassword" type="password"></p>
             <p><button type="submit">Register</button></p>
             </form>'''
@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    if request.form['username']=='admin' and request.form['password']=='password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'
@app.route('/register',methods=['POST'])
def register():
    if request.form['fpassword']==request.form['spassword']:
        return '<h3>Regist Successful!</h3>'
    return'<h3>Register Failed!</h3>'

if __name__ == '__main__':
    app.run()