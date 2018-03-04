from azure.storage.blob import ContentSettings
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess

from azure.cognitiveservices.vision.customvision.training import training_api
from azure.cognitiveservices.vision.customvision.prediction import prediction_endpoint
from azure.cognitiveservices.vision.customvision.prediction.prediction_endpoint import models

import http.client, urllib.request, urllib.parse, urllib.error, base64

import cv2
import math
import json
import os
import random
import _thread
import requests
import sys
from twilio.rest import Client


#prediction
training_key ="#{Your Training Key}"
prediction_key = "#{Your Prediction Key}"
predictor = prediction_endpoint.PredictionEndpoint(prediction_key)

#Image Upload
acct_name="framestore"
acct_key="#{Your Azzure Cloud Account Key}"
block_blob_service = BlockBlobService(account_name=acct_name, account_key=acct_key)
event_cap = False

def get_iter_id():
    headers = {
    # Request headers
    'Training-key': '#{Your Key}',
    }

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('southcentralus.api.cognitive.microsoft.com')
        conn.request("GET", "/customvision/v1.0/Training/projects/05bed582-9f11-4906-83a0-e9cae717ec84/iterations?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        dic=json.loads(data.decode('utf-8'))
        #print(dic)
        iter_id=dic[len(dic)-2]['Id']
        print(iter_id)

        conn.close()
        return iter_id
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    



def upload_img(imagesFolder,filename):
    block_blob_service.create_blob_from_path(
        'criminal-frame',
        filename,
        imagesFolder+"/"+filename,
        content_settings=ContentSettings(content_type='image/jpg')
                )
    return ("https://framestore.blob.core.windows.net/criminal-frame/"+filename)


def get_async_web_response(url, method='GET', params=None, headers=None, encode=False, verify=None, use_verify=False, callback=None):
    # make a string with the request type in it:
    response = None
    request = None
    try:
        if 'POST' == method:
            if use_verify:
                request = grequests.post(url, data=params, headers=headers, verify=verify, callback=callback)
                print("HERERERERE")
            else:
                request = grequests.post(url, data=params, headers=headers, callback=callback)
        else:
            request = requests.get(url, data=params, headers=headers, callback=callback)

        if request:
            response = grequests.send(request, grequests.Pool(1))
            return response
        else:
            return response
    except:
        return response

def printStatus(response, **kwargs):
    print(response)
    print("response code {}".format(response.status_code))
    print("response text {}".format(response.content))  




account = "#{twilio_account}"
token = "#{twilio_token}"
client = Client(account, token)

top=0
left=0
width=0
height=0
anger=0
frames_c=0
min_top = sys.maxsize
min_left = sys.maxsize
new_anger = 0
# response from api

def find_min_distance(json_entry):
    global min_top
    global min_left
    if(min_top>abs(top-json_entry['faceRectangle']['top']) and min_left>abs(left-json_entry['faceRectangle']['left'])):
        min_top = abs(top-json_entry['faceRectangle']['top'])
        min_left = abs(left-json_entry['faceRectangle']['left'])
        return True
    return False

def get_alert(json_object, tag_data):
    # print(json_object)
    # print(tag_data)
    global top
    global left
    global width
    global height
    global anger
    global frames_c
    global new_anger
    global event_cap
    for json_entry in json_object:
        # print(json_entry)
        if frames_c == 0:
            if( anger <= json_entry['faceAttributes']['emotion']['anger']): 
                anger = json_entry['faceAttributes']['emotion']['anger']
                top = json_entry['faceRectangle']['top']
                left = json_entry['faceRectangle']['left']
                width = json_entry['faceRectangle']['width']
                height = json_entry['faceRectangle']['height']
        else:
            if (find_min_distance(json_entry)):
                new_anger = json_entry['faceAttributes']['emotion']['anger']
    frames_c += 1
    anger += new_anger
    if(anger >= 0.2 and ((tag_data["Gun"] * tag_data["Person"]) >= 0.05 or (tag_data["Knife"] * tag_data["Person"] ) >= 0.05)):
        message = client.messages.create(to="+13232877405", from_="+19093456569",
                                     body="High Alert..There might. be person with potential weapon and intent to hurt people.")
        event_cap = True
    elif((tag_data["Gun"] * tag_data["Person"] ) >= 0.05 or (tag_data["Knife"] * tag_data["Person"] ) >= 0.05):
        message = client.messages.create(to="+13232877405", from_="+19093456569",
                                     body="Alert..There might be person with potential deadly weapon.") 
        event_cap = True


def get_pred(imagesFolder, temp_name,iter_id):

    global res
    img_link=upload_img(imagesFolder,temp_name)
    emotion_recognition_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceAttributes=emotion"
    headers  = {'Ocp-Apim-Subscription-Key': "#{prediction key}"}
    response = requests.post(emotion_recognition_url, headers=headers, json={'Url': img_link})
    response.raise_for_status()
    analysis = response.json()

    res = predictor.predict_image_url("#{customvision_api_key}",iter_id, url=img_link)
    preds = {}
    for prediction in res.predictions:

        preds[prediction.tag] = prediction.probability
        print ("\t" + prediction.tag + ": {0:.2f}%".format(prediction.probability * 100))
    get_alert(analysis, preds)      

    """  Call to calculatye score """
def get_out():      
    cv2.destroyWindow("preview")
    # vc.release()      
    cap.release()
    print("Alert Generated .. Notification Sent to Police.. !") 


iter_id=get_iter_id()
iter_id ="0f761fd-61c8-469d-998e-13a74655b8ec"
videoFile = "capture.avi"
imagesFolder = os.path.join("./frames")
cap = cv2.VideoCapture(0)
frameRate = 5 #frame rate
cv2.namedWindow("preview",cv2.WINDOW_NORMAL)
cv2.resizeWindow('preview', 500,350)
n = 100
async_list = []
res = None;
while(cap.isOpened()):
    frameId = n #current frame number
    ret, frame = cap.read()
    cv2.imshow("preview", frame)
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        get_out()
    if (ret != True):
        get_out()
    if event_cap:
        get_out()   
    if (frameId % math.floor(frameRate) == 0):
        temp_name="image_" +  str(int(frameId))+ str(random.randrange(0, 101, 2)) + ".jpg"
        filename = imagesFolder + "/"+temp_name
        cv2.imwrite(filename, frame)
        _thread.start_new_thread( get_pred, (imagesFolder, temp_name,iter_id,))
        while(res == None):
            ret, frame = cap.read()
            cv2.imshow("preview", frame)
            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                get_out()
            if (ret != True):
                get_out()

                
        
        res = None
    n -= 1
    if(n == 0):
        n = 100     
