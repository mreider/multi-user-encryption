# -*- coding: utf-8 -*-
from flask import Flask,request, jsonify
from dbmanager import Database

db = Database()
db.start_engine()
app = Flask(__name__)

@app.route('/api/v1.0/data',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        #Fetch data
        username = request.args.get('user','')
        password = request.args.get('password','')
        print 'Username = %s, password = %s'%(username,password)
        content = db.get_data(username,password)
        return jsonify(data=content)
    elif request.method == 'POST':
        #Update data
        username = request.form.get('user','')
        password = request.form.get('password','')
        data = request.form.get('content','')
        print 'Username = %s, password = %s'%(username,password)
        print 'Data %s'%data
        db.save_data(data,username,password)
    else :
        print 'Not handling it'
    return jsonify(data=data)


@app.route('/api/v1.0/rotate',methods=['GET'])
def rotate():
    if request.method == 'GET':
        #Fetch data
        username = request.args.get('user','')
        password = request.args.get('password','')
        print 'Username = %s, password = %s'%(username,password)
        if username != 'Root':
            return jsonify(data='Error : Only root user can perform this.')
        print 'Username = %s, password = %s'%(username,password)
        data = db.rotate_data(username,password)
        return jsonify(data=data)

@app.teardown_appcontext
def teardown_db(exception):
    if db:
        db.connection_close()

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)