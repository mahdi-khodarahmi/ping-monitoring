#!/usr/bin/python
# -*- coding: utf-8 -*-

#Written By Mahdi Khodarahmi
#Release Date:1400/05/20

import subprocess as sp
import time
import requests
import json
import datetime
import sys

ip = "8.8.8.8"
serverLocation="سرور غرب تهران"

now = datetime.datetime.now()
hour = now.hour
if hour < 12:
    greeting = "صبح بخير"
elif hour < 19:
    greeting = "عصر بخير"
else:
    greeting = "شب بخير"

timeNow=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#print("{}!".format(greeting))


def prettyJSON(response):
    b=json.loads(response.text)
    print(json.dumps(b, indent = 1, ensure_ascii=False))
    
def getSMS():
    
    tokenUrl = "https://RestfulSms.com/api/Token"
    tokenPayload ={
            "UserApiKey":"5db8.........94c",
            "SecretKey":"key........"
    }
    tokenHeaders = {
      'Content-Type': 'application/json'
    }
    
    try:
        tokenResponse = requests.request("POST", tokenUrl, headers=tokenHeaders, data = json.dumps(tokenPayload))
        token=tokenResponse.json()['TokenKey']
    except:
        print("Maybe the internet is disconnect!. can't get Token")        
    try :   
        if tokenResponse.json()['IsSuccessful'] == True:
            url = "https://restful.........com/api/ReceiveMessage?Shamsi_FromDate=1400/04/31&Shamsi_ToDate=1410/04/31&RowsPerPage=5&RequestedPageNumber=1"
            headers = {
              'x-sms-ir-secure-token': token,
              'Content-Type': 'application/json'
            }
            response = requests.request("GET", url, headers=headers)
            if response.json()['IsSuccessful'] == True:
                return response
            else:
                print("get sms problem!")            
    except:
        print("Maybe the internet is disconnect!. can't get send SMS")           



def sendSMS(myMessages):
    
    tokenUrl = "https://Restful..................com/api/Token"
    tokenPayload ={
            "UserApiKey":"5db.............94c",
            "SecretKey":"key........."
    }
    tokenHeaders = {
      'Content-Type': 'application/json'
    }
    try :
        tokenResponse = requests.request("POST", tokenUrl, headers=tokenHeaders, data = json.dumps(tokenPayload))
        token=tokenResponse.json()['TokenKey']
    except:
        print("Maybe the internet is disconnect!. can't get Token(sendSMS)")
    try :
        if tokenResponse.json()['IsSuccessful'] == True:
            url = "https://Restful............com/api/MessageSend"
            payload = {
                    "Messages":[myMessages],
                    "MobileNumbers": ["09........."],
                    "LineNumber": "3000.........",
                    "SendDateTime": "",
                    "CanContinueInCaseOfError": "false",     
            }
            headers = {
              'x-sms-ir-secure-token': token,
              'Content-Type': 'application/json'
            }
            
            response = requests.request("POST", url, headers=headers, data = json.dumps(payload))                        
            if response.json()['IsSuccessful'] == True:
                return response           
            else:
                print("send sms problem!")
    except:
        print("Maybe the internet is disconnect!. can't send SMS")



print ("++++ App Started ++++")
getSMSresponse=getSMS()        
msgID=getSMSresponse.json()['Messages'][0]["ID"]

def getNumberFromSMS():
    
    sendSMS("لطفا با ارسال عدد وضعيت را مشخص نماييد")
    while True:
        getSMSresponse=getSMS()
        msgBody=getSMSresponse.json()['Messages'][0]["SMSMessageBody"]
        print("Last SMS That Sent By Admin: "+msgBody)
        
        #check ping when wait for get sms from admin:
        status,result = sp.getstatusoutput("ping " + ip)
        if status == 0: 
          print("Server: " + ip + " is UP Now !")
          time.sleep(3)
          #send sms that ping come back:
          sendSMS("پينگ سرور:"+ip+"برقرار گرديد.")
          break
        else:
          print("■■■ Server: " + ip + " still is DOWN ! ■■■")
                  
        time.sleep(2)
        msgIDNew=getSMSresponse.json()['Messages'][0]["ID"]
        #print(msgIDNew)
        global msgID
        if msgID != msgIDNew:
            print("++++++++++ Internet Down - wait for get New Code status from SMS... +++++++++++")
            statusNumber=getSMSresponse.json()['Messages'][0]["SMSMessageBody"]
            msgID=msgIDNew
            #print("new id set")
            #print(msgID)
            if statusNumber == 'off':
                sendSMS("کد خاموش کردن برنامه دريافت شد.")
                time.sleep(3)
                sys.exit()
                break
            elif statusNumber == '1':
                sendSMS("کد شروع بررسي دريافت شد.")
                return statusNumber
                break
            else:
                print ("mistake sms code")
                sendSMS("کد وارد شده اشتباه است")
        else:
            time.sleep(5)
            


def listenComingNewCode():

        getSMSresponse=getSMS()
        time.sleep(2)
        msgBody=getSMSresponse.json()['Messages'][0]["SMSMessageBody"]
        time.sleep(2)
        msgIDNew=getSMSresponse.json()['Messages'][0]["ID"]
        global msgID
        if msgID != msgIDNew:
            print("++++++++++New Code Detected from SMS... +++++++++++")
            statusNumber=getSMSresponse.json()['Messages'][0]["SMSMessageBody"]
            msgID=msgIDNew
            if statusNumber == 'off':
                print ("SMS received --> off code.")
                sendSMS("کد خاموش کردن برنامه دريافت شد.")
                time.sleep(3)
                sys.exit()
            elif statusNumber == '1':
                print ("SMS received --> check again.")
                sendSMS("کد شروع بررسي دريافت شد.")
                return statusNumber
            
    



isUp = 1
downMyInternet=0

while True:
        if isUp == 1:
                status,result = sp.getstatusoutput("ping " + ip)
                if status == 0: 
                 print("Server: " + ip + " is UP !")
                 #os.system("timeout /t 5")
                 #response = os.system("ping -c 1 " + hostname)
                 listenComingNewCode()
                 time.sleep(3)
                else:
                  print("■ Server: " + ip + " is DOWN !")
                  #sendSMS("System " + ip + " is DOWN !")
                  isUp = 0
                  print("##### Let check: #####")
                  
                  status,result = sp.getstatusoutput("ping 8.8.8.8")
                  time.sleep(5)
                  if status == 0 and isUp != 1:         
                      print("i can see 8.8.8.8, so your other server is down!!!")
                      myMessages=(greeting+"\nسرور پايين است - "+serverLocation+"\nip:"+ip+"\ntime:"+timeNow+"\nارسال عدد 1 به معنای بررسی دوباره پینگ"+"\nارسال عبارت off برای خاموش کردن برنامه")
                      sendSMS(myMessages)
                      statusNumber=getNumberFromSMS()
                      isUp = 1
                      
                  else:
                      print("i couldn't see google.com and your server, so my internet is down. \n ■■■ please connect me to internet ...■■■ \n !!!!!!!!!!!!!!!!!!!")
                      downMyInternet+= 1
                      time.sleep(5)
                      isUp = 1
