from flask import Flask, jsonify
from flask import make_response
from flask import abort
from flask import request
import uuid
import jiexi
from dbs.smdb import smdb
import urllib.parse
import re
import json
import lxml
import random
from datetime import datetime
import time
import json

app = Flask(__name__)


@app.route("/")
def index():
    return '123'

@app.route('/suanming/user', methods=['GET','POST'])
def create_user():
    #argsvalue =  request.args
    word = request.args.get('word', '')
    name = request.args.get('name', '')
    sex = request.args.get('sex', '')
    year = request.args.get('year', '')
    month = request.args.get('month', '')
    day = request.args.get('day', '')
    hour = request.args.get('hour', '0')
    minute = request.args.get('minute', '0')
    if (word and name and sex and year and month and day) == '':
        return 'successCallback({0})'.format(json.dumps({'error':'bad param'}))
    datas = jiexi.lifemobile(word,year,month,day,hour,minute,sex,name)
    rqxm = jiexi.zhouyihaoma2(word)
    datas['rqxm'] = rqxm
    userid = str(uuid.uuid1())
    sdb = smdb()
    sdb.create_user(userid,json.dumps(datas,ensure_ascii=False))
    dicthead = {'userid':userid,'pnum':word,'uname':name}
    data = dict(**dicthead,result=datas['suli'])
    return 'successCallback({0})'.format(json.dumps(data,ensure_ascii=False))

@app.route('/suanming/userdata', methods=['GET','POST'])
def get_user_data():
    #argsvalue =  request.args
    userid = request.args.get('userid', '')
    step = request.args.get('step', '')
    if (userid and step) == '':
        return jsonify({'error':'bad param'})
    sdb = smdb()
    userdata = sdb.get_user_data(userid)
    if userdata:
        userdictdata = json.loads(userdata[0])
        dbsteps = userdata[1]
        pnum = userdictdata['pnum']
        name = userdictdata['uname']
        data = None
        dicthead = {'userid':userid,'pnum':pnum,'uname':name}
        if step == '1':
            data = dict(**dicthead,result=userdictdata['suli'])
        elif step == '2':
            data = dict(dicthead,result=userdictdata['yunshi'])
        elif step == '3':
            data = dict(dicthead,result=userdictdata['mima'])
        elif step == '4':
            data = dict(dicthead,result=userdictdata['rqxm'])
        else:
            return  'successCallback({0})'.format(json.dumps({'error':'bad param'}))
        if data:
            if dbsteps < int(step):
                sdb.update_step(userid,step)
        return 'successCallback({0})'.format(json.dumps(data,ensure_ascii=False))
    else:
        return 'successCallback({0})'.format(json.dumps({'error':'no data'}))


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run()