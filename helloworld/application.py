#!flask/bin/python
import json
import requests
import sys, os #class 4
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))

from flask import Flask, Response, request
from helloworld.flaskrun import flaskrun

application = Flask(__name__) #take the name of the class that run now

@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
    
@application.route('/get_ip', methods=['GET']) #Class 4
def get_ip():
    print(get_ip_meta())
    return Response(json.dumps(format(get_ip_meta())), mimetype='application/json', status=200)

@application.route('/', methods=['POST'])
def post():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)

def get_ip_meta(): #Class 4
    user_ip = str(request.environ['REMOTE_ADDR'])
    service_url = 'http://ipinfo.io/{}'.format(user_ip) 
    return requests.get(service_url).json()

if __name__ == '__main__':
    flaskrun(application)
    