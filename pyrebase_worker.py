#   requirements.txt                  pyrebase
import pyrebase
import firebase_admin
from firebase_admin import credentials

config = {
    "apiKey": "AIzaSyAPuV0fCfbbi-V8BJFXmeApIWNvKZUpzn4",
    "authDomain": "twilio-bot-1601d.firebaseapp.com",
    "databaseURL": "https://twilio-bot-1601d.firebaseio.com",
    "projectId": "twilio-bot-1601d",
    "storageBucket": "twilio-bot-1601d.appspot.com",
    "messagingSenderId": "933434061900",
    "serviceAccount": "twilio-bot-1601d-firebase-adminsdk-5bbb8-25331d6181.json"
  }


def push(name, phone, servers):    
    print("connecting")
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    if servers.lower() == "all":
        servers = ["bot-test-jordan", "BCS Pokemon Go", "Team Aqua's Hideout"]
    data = {
            "phone": phone,
            "servers": servers
    }
    print("pushing...")
    results = db.child("users").child(name).push(data)
    print('finished!\nresults ->')
    print(results)



def getData():
    print("connecting")
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    print("retrieving")
    all_users = db.child("users").get()
    print('finished!\nall_users ->')
    for item in all_users.val().items():
        print(item)


def getByServer(server):
    # users_by_score = db.child("users").order_by_child("score").equal_to(10).get()
    print("connecting")
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    print("retrieving")
    users_by_server = db.child("users").child("$name").child("$uid").order_by_child("phone").equal_to(server).get()
    print('finished!\nusers_by_server: [' + server + ']  ->')
    for item in users_by_server.val().items():
        print(item)
 

def remove(name):
    print("connecting")
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    print("deleting")
    results = db.child("users").child(name).remove()
    print("result from delete:")
    print(results)
    