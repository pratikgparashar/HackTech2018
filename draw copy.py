# import cv2

# cv2.namedWindow("preview")
# vc = cv2.VideoCapture(0)

# if vc.isOpened(): # try to get the first frame
#     rval, frame = vc.read()
# else:
#     rval = False

# while rval:
#     cv2.imshow("preview", frame)
#     rval, frame = vc.read()
# #     key = cv2.waitKey(20)
#   if key == 27: # exit on ESC
#       break

# cv2.destroyWindow("preview")
# vc.release()

from azure.storage.blob import ContentSettings
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess

from azure.cognitiveservices.vision.customvision.training import training_api
from azure.cognitiveservices.vision.customvision.prediction import prediction_endpoint
from azure.cognitiveservices.vision.customvision.prediction.prediction_endpoint import models

import cv2
import math
import json
import os
import random
import _thread
import requests


#prediction
training_key ="50c2ce1537da463bb1bb96d3833e5607"
prediction_key = "a37bf842c80a4380b7cd7ff45abec38d"
predictor = prediction_endpoint.PredictionEndpoint(prediction_key)

#Image Upload
acct_name="framestore"
acct_key="zBqpNlcVjCuhzfGWIt02pV8i4EgCwY6XYZkrKqNf0nvb9teFSOC2xpyAjh8D5fykSqpN9jLzjhrUxHRzJ+6KNA=="
block_blob_service = BlockBlobService(account_name=acct_name, account_key=acct_key)






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

def get_pred(imagesFolder, temp_name):

    global res
    img_link=upload_img(imagesFolder,temp_name)
    # res = predictor.predict_image_url(key1, key2, url=test_img_url)
    # image_data = open(imagesFolder+"/"+temp_name, "rb").read()
    emotion_recognition_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceAttributes=emotion"
    headers  = {'Ocp-Apim-Subscription-Key': "f771b37a021647189f81eb7ca157e447"}
    response = requests.post(emotion_recognition_url, headers=headers, json={'Url': img_link})
    response.raise_for_status()
    analysis = response.json()
    print(analysis)
    # if len(analysis)!=0:
        
    #   #print(analysis[0]['faceAttributes'])
    # else:
    #   print(analysis)
    res = predictor.predict_image_url("05bed582-9f11-4906-83a0-e9cae717ec84", "2ceb6d39-03ee-4fc8-8603-fd7ab2501af1", url=img_link)
    for prediction in res.predictions:
            print ("\t" + prediction.tag + ": {0:.2f}%".format(prediction.probability * 100))

    """  Call to calculatye score """

iter_id=get_iter_id()
videoFile = "capture.avi"
imagesFolder = os.path.join("./frames")
cap = cv2.VideoCapture(0)
frameRate = 5 #frame rate
cv2.namedWindow("preview")
n = 100
async_list = []
res = None;
while(cap.isOpened()):
    frameId = n #current frame number
    ret, frame = cap.read()
    cv2.imshow("preview", frame)
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
    if (ret != True):
        break
    #print(frameId)
    if (frameId % math.floor(frameRate) == 0):
        temp_name="image_" +  str(int(frameId))+ str(random.randrange(0, 101, 2)) + ".jpg"
        filename = imagesFolder + "/"+temp_name
        cv2.imwrite(filename, frame)
        print("Aaaaaa")
        
        print(filename)
        # test_img_url=img_link
        # results = predictor.predict_image_url("05bed582-9f11-4906-83a0-e9cae717ec84", "9bfe13f5-8db7-4831-a47b-6e7f5d2e1ad1", url=test_img_url)
        _thread.start_new_thread( get_pred, (imagesFolder, temp_name, ))
        while(res == None):
            ret, frame = cap.read()
            cv2.imshow("preview", frame)
            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                get_out()
            if (ret != True):
                get_out()

                
        
        res = None
        # import grequests
        # params = {'url': img_link}
        # headers = {'Content-type' : 'application/json',
        #   'Prediction-Key' : 'a37bf842c80a4380b7cd7ff45abec38d'}

        # print("@@@@@@@@@")
        # url= ""
        # grequests.post('https://southcentralus.api.cognitive.microsoft.com/customvision/v1.1/Prediction/05bed582-9f11-4906-83a0-e9cae717ec84/image?iterationId=9bfe13f5-8db7-4831-a47b-6e7f5d2e1ad1', params=params, headers=headers, callback=printStatus)   
        # d = get_async_web_response('https://southcentralus.api.cognitive.microsoft.com/customvision/v1.1/Prediction/05bed582-9f11-4906-83a0-e9cae717ec84/image?iterationId=9bfe13f5-8db7-4831-a47b-6e7f5d2e1ad1', 'POST', params=params, headers=headers, callback=printStatus)
        # async_list.add(d);
    n -= 1
    if(n == 0):
        n = 100     

        
def get_out():      
    cv2.destroyWindow("preview")
    # vc.release()      
    cap.release()
    print("Done!")  