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
    


    # cred = credentials.Certificate("/twilio-bot-1601d-firebase-adminsdk-5bbb8-25331d6181.json")
    # firebase = firebase_admin.initialize_app(cred)

    # firebase = pyrebase.initialize_app(config)
    # auth = firebase.auth()
    # email = "murphyjd541@gmail.com"
    # password = "twilioBotPyrebase666"
    # user = auth.sign_in_with_email_and_password(email, password)   #    murphyjd541@gmail.com      twilioBotPyrebase666
    # db = firebase.database()
    # name = "Vinnie"
    # phone = "333-1231-2222"
    if servers.lower() == "all":
        servers = ["bot-test-jordan", "BCS Pokemon Go", "Team Aqua's Hideout"]

    data = {
            name : {
                "phone": phone,
                "servers": servers
            }
    }
    print("pushing...")
    # Pass the user's idToken to the push method
    # results = db.child("users").child("Bobert").set(data, user['idToken'])
    results = db.child("users").push(data)
    print('finished!\nresults ->')
    print(results)



def getData():
    print("connecting")

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    # db.child("users").get()

    # cred = credentials.Certificate("/twilio-bot-1601d-firebase-adminsdk-5bbb8-25331d6181.json")
    # firebase = firebase_admin.initialize_app(cred)

    # firebase = pyrebase.initialize_app(config)
    # auth = firebase.auth()
    # email = "murphyjd541@gmail.com"
    # password = "twilioBotPyrebase666"
    # user = auth.sign_in_with_email_and_password(email, password)   #    murphyjd541@gmail.com      twilioBotPyrebase666
    # db = firebase.database()
    print("retrieving")
    all_users = db.child("users").get()
    print('finished!\nall_users ->')
    print(all_users.val())
 