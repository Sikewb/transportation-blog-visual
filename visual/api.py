from flask import Flask, jsonify,request
from flask_restplus import Resource, Api
import json
import pymysql
from pymysql.cursors import DictCursor
from flask_cors import cross_origin

app = Flask(__name__)
api = Api(app)

@api.route('/event')
@cross_origin()
def get(self):
    return_dict = {'code': 1, 'result': False, 'msg': '请求成功'}
    return_dict['result'] = sql_result()

    return(json.dumps(return_dict, ensure_ascii=False))

def sql_result(self):
    conn = pymysql.connect(host='127.0.0.1', database='event', user='root', password='3a140db621dd4c72')
    cursor = conn.cursor(DictCursor)
    cursor.execute("SELECT * FROM event_table")
    result = cursor.fetchall()
    conn.close()
    return result

@app.route('/event/search')
@cross_origin()
def search():
    return_dict = {'code': 1, 'result': False, 'msg': '请求成功'}

    get_data = request.args.to_dict()
    event_name = get_data.get("event_name")

    return_dict['result'] = sql_search(event_name)

    return(json.dumps(return_dict, ensure_ascii=False))

@app.route('/event/add')
@cross_origin()
def insert():
    get_data = request.args.to_dict()
    event_name = get_data.get("event_name")
    location = get_data.get("location")
    time = get_data.get("time")
    detail= get_data.get("detail")
    result = sql_insert(event_name,location,time,detail)
    return(result)

@app.errorhandler(404)
@cross_origin()
def page_not_found(e):
    res = jsonify({'error': 'not found'})
    res.status_code = 404
    return res



def sql_result():
    conn = pymysql.connect(host='127.0.0.1', database='event', user='root', password='3a140db621dd4c72')
    cursor = conn.cursor(DictCursor)
    cursor.execute("SELECT * FROM event_table")
    result = cursor.fetchall()
    conn.close()
    return result

def sql_insert(event_name,location,time,detail):
    conn = pymysql.connect(host='127.0.0.1', database='event', user='root', password='3a140db621dd4c72')
    cursor = conn.cursor()
    sql = 'INSERT INTO event_table VALUES ("%s","%s","%s","%s")' %(event_name,location,time,detail)
    cursor.execute(sql)
    conn.commit()
    conn.close()
    return("插入成功")

def sql_search(event_name):
    conn = pymysql.connect(host='127.0.0.1', database='event', user='root', password='3a140db621dd4c72')
    cursor = conn.cursor(DictCursor)
    cursor.execute('SELECT * FROM event_table WHERE event_name LIKE "%%%s%%"' %(event_name))
    result = cursor.fetchall()
    conn.close()
    return result

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)