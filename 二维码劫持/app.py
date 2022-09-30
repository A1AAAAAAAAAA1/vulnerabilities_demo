# @Author:77
# -*- codeing = utf-8 -*-
# @TIME : 2022/9/28 19:14
# @File : app.py
# @Software: PyCharm
from flask import Flask,render_template
import sqlite3

app = Flask(__name__)
# @app.route('/')
# def index():
#     return render_template("")

@app.route('/')
def qrcode():
    f = open("qrcode.txt", 'r')
    ticket = f.readline()
    print(ticket)
    print(111)
    print(ticket)
    url='https://mp.weixin.qq.com/cgi-bin/showqrcode?{}'.format(ticket)
    print(url)
    f.close()
    return '<img src={}>'.format(url)

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000,debug=True)