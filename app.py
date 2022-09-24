from flask import Flask,render_template,url_for,request,redirect, make_response
import random
import json
import numpy as np
import urllib.request
import requests
import threading
import subprocess
import calendar
import pickle
from time import time
from random import random
from datetime import datetime
from flask import Flask, render_template, make_response
app = Flask(__name__)

def decrypt(message, key):
    return subprocess.check_output(['./a.out', message, key, "1"]).decode('utf8').strip()


def encrypt(message, key):
    return subprocess.check_output(['./a.out', message, key, "0"]).decode('utf8').strip()

def get_data(uri, data_format="json"):
    """
        Method description:
        Deletes/Unregisters an application entity(AE) from the OneM2M framework/tree
        under the specified CSE

        Parameters:
        uri_cse : [str] URI of parent CSE
        ae_name : [str] name of the AE
        fmt_ex : [str] payload format
    """
    headers = {
        'X-M2M-Origin': '0msPeJ:NGB!1i',
        'Content-type': 'application/{}'.format(data_format)}

    response = requests.get(uri, headers=headers)
    # print('Return code : {}'.format(response.status_code))
    # print('Return Content : {}'.format(response.text))
    _resp = json.loads(response.text)
    # return _resp['m2m:cin']['con']
    # print("hiiii")
    # print(_resp)
    return response.status_code, _resp ## To get latest or oldest content instance
    #return response.status_code, _resp["m2m:cnt"]#["con"] ## to get whole data of container (all content instances)
model = pickle.load(open('model.pkl','rb'))
@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')

@app.route('/get_plot_data', methods=["GET", "POST"])
def get_plot_data():
    code , result = get_data("https://esw-onem2m.iiit.ac.in/~/in-cse/in-name/Team-37/Node-1/Data/la")
    key = 'VidhiMafia'
    encrypted_string = result['m2m:cin']['con']
    decrypted_string = decrypt(encrypted_string , key)
    # print(decrypted_string)

    # remove the '[' from the decrypted_string
    decrypted_string = decrypted_string[1:]
    # remove the ' ' from the decrypted_string
    decrypted_string = decrypted_string.replace(" ", "")
    # store the , seperated number from decrypted_string in a list and convert them to integer
    decrypted_string = [int(i) for i in decrypted_string.split(',')]
    response = make_response(json.dumps(decrypted_string))
    response.content_type = 'application/json'
    return response    

@app.route('/data', methods=["GET", "POST"])
def data():

    # get_data=requests.get("https://api.thingspeak.com/channels/1843911/feeds.json?api_key=9ACLC4CTSM4RVW90&results=1").json()
    # feild_1=get_data['feeds'][0]['field1']
    # date = get_data['feeds'][0]['created_at']
    # # print(feild_1)
    # print(date)
    # datetime_object = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    # print(datetime_object)
    # epoch_time  =  datetime_object.timestamp()
    # print(epoch_time)
    # # timestamp = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    # # # unix_time_local = datetime.mktime(timestamp)
    # # unix_time_utc = calendar.timegm(timestamp)
    # # print(unix_time_local)
    # # print(unix_time_utc)
    
    # data = [float(epoch_time *1000)-3600000, float(feild_1) ]
    # response = make_response(json.dumps(data))
    # response.content_type = 'application/json'
    # return response

    code , result = get_data("https://esw-onem2m.iiit.ac.in/~/in-cse/in-name/Team-37/Node-1/Data/la")
    # print("callingggg")
    # print(result)
    key = 'VidhiMafia'
    encrypted_string = result['m2m:cin']['con']
    decrypted_string = decrypt(encrypted_string , key)
    # print(decrypted_string)

    # remove the '[' from the decrypted_string
    decrypted_string = decrypted_string[1:]
    # remove the ' ' from the decrypted_string
    decrypted_string = decrypted_string.replace(" ", "")
    # store the , seperated number from decrypted_string in a list and convert them to integer
    decrypted_string = [int(i) for i in decrypted_string.split(',')]


    decrypted_string = np.array(decrypted_string)
    decrypted_string = decrypted_string.reshape(-1, 100)


    decrypted_string = decrypted_string.reshape((decrypted_string.shape[0],decrypted_string.shape[1],1))
    decrypted_string = np.asarray(decrypted_string).astype('float32')
    print(decrypted_string.shape)
    # print("Size of test data is " , decrypted_string.shape)

    # # Convert decrypted_string to a list having 3 rows and having np.array 
    # decrypted_string = np.array(decrypted_string).reshape(-1,100 , 1)
    
    # # print shape of decrypted_string
    # print(decrypted_string)

    # ans = model.predict(decrypted_string)
    ans = model.predict(decrypted_string , verbose=1)

    print(ans)
    t = []
    # x = -1

    for arr in ans:
        t.append(np.argmax(arr , axis=0))
    
    print(t)

    count_1 = 0
    count_2 = 0
    count_3 = 0
    count_4 = 0

    for i in t:
        if i == 1:
            count_1+=1
        elif i == 2:
            count_2 += 1
        elif i == 3:
            count_3+=1
        elif i == 4:
            count_4+=1
    
    resp = 0

    if count_1 >= 2:
        resp = 1
    elif count_2 >= 2:
        resp = 2
    elif count_3 >= 2:
        resp = 3
    elif count_4 >= 2:
        resp = 4

    # print(ans)
    # ans = np.argmax(x , axis = 1)
    # print(ans)

    print("response is " , resp)
    response = make_response(json.dumps(resp))
    return response
    # print(encrypted_string)
    # print(result)


def begin():
    get_data=requests.get("https://api.thingspeak.com/channels/1579481/feeds.json?api_key=W3YO4Q3IGTZT9XWC").json()


if __name__ == "__main__":
    app.run(debug=True)