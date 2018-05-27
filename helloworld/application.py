#!flask/bin/python
import json
import requests
import boto3 #class 7
import datetime #class 7
import sys, os #class 4
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))

from flask import Flask, Response, request, render_template
from helloworld.flaskrun import flaskrun

application = Flask(__name__) #take the name of the class that run now

@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
    
@application.route('/get_ip', methods=['GET']) #Class 4
def get_ip():
    print(get_ip_meta())
    return Response(json.dumps(format(get_ip_meta())), mimetype='application/json', status=200)
    
@application.route('/temp/<temp>', methods=['POST']) #Class 7 send data to dynamodb
def get_temp(temp):
    response = get_ip_meta()
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('eb_try_logger')
    # res_data = {k: v for k, v in response.items() if v!=''}
    # print(res_data)
    item={
    'ipAddress': str(response),
    'path': temp,
    'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    'time': datetime.datetime.now().strftime("%H:%M:%S"),
    'ip_meta' : response, # res_data
    'name': 'Hemi'
    }
    print(item)
    table.put_item(Item=item)

    return Response(json.dumps(item), mimetype='application/json', status=200)
    
#@application.route('/bi', methods=['GET']) #class 7 scan dynamo table
#def get_bi():
 #   dynamodb = boto3.resource('dynamodb')
  #  table = dynamodb.Table('eb_try_logger')
    # replace table scan
   # resp = table.scan()

    #return Response(json.dumps(str(resp)), mimetype='application/json', status=200)
    #return render_template('index.html', response=str(resp), title='bi') #return html page
    
    
@application.route('/bi', methods=['GET'])
def get_bi():
    my_ses = boto3.Session(region_name = 'us-east-2')
    dynamodb = my_ses.resource('dynamodb')
    table = dynamodb.Table('eb_try_logger')
    resp = table.scan()

    #return Response(json.dumps(str(resp)), mimetype='application/json', status=200)
    return render_template('index.html', response=str(resp), title='bi')


#@application.route('/', methods=['POST'])
#def post():
 #   return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)


def get_ip_meta(): #Class 4
    user_ip = str(request.environ['REMOTE_ADDR'])
    service_url = 'http://ipinfo.io/{}'.format(user_ip) 
    return requests.get(service_url).json()

if __name__ == '__main__':
    flaskrun(application)
    