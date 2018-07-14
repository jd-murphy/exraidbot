#   requirements.txt                  pyrebase
import pyrebase
import firebase_admin
from firebase_admin import credentials
import json

config = {
    "apiKey": "AIzaSyAPuV0fCfbbi-V8BJFXmeApIWNvKZUpzn4",
    "authDomain": "twilio-bot-1601d.firebaseapp.com",
    "databaseURL": "https://twilio-bot-1601d.firebaseio.com",
    "projectId": "twilio-bot-1601d",
    "storageBucket": "twilio-bot-1601d.appspot.com",
    "messagingSenderId": "933434061900",
    "serviceAccount": "twilio-bot-1601d-firebase-adminsdk-5bbb8-25331d6181.json"
  }


def push(name, phone, bcspogo, btj, aqua):    
    print("connecting")
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    data = {
        "name": name,
        "phone": phone,
        "BCS Pokemon Go": bcspogo,
        "bot-test-jordan": btj,
        "Team Aqua's Hideout": aqua
    }


    print("pushing...")
    results = db.child("users").push(data)
    print('finished!\nresults ->')
    print(results)



def getData():
    print("connecting")
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    print("retrieving")
    users = db.child("users").get()
    print('finished!\nall_users ->')
    for user in users.val().items():
        print(user)
    return users


def getByServer(server):
    users = getData()
    if server == "BCS Pokemon Go":
        for user in users.each():
            print(user.key())
            print(user.val())
            out = json.loads(user.val())
            print("out: " + out)
        
                
            

    if server == "bot-test-jordan":
        for user in users.each():
            print(user.key())
            print(user.val())
            out = json.loads(user.val())
            print("out: " + out)
        

        

    if server == "Team Aqua's Hideout":
        for user in users.each():
            print(user.key())
            print(user.val())
            out = json.loads(user.val())
            print("out: " + out)






def remove(name):
    print("connecting")
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    print("deleting")
    results = db.child("users").child(name).remove()
    print("result from delete:")
    print(results)
    