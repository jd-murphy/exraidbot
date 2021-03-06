import pyrebase
import firebase_admin
from firebase_admin import credentials
import json
from os import environ
from datetime import datetime


config = {
    "apiKey": environ["firebaseApiKey"],
    "authDomain": environ["authDomain"],
    "databaseURL": environ["databaseURL"],
    "projectId": environ["projectId"],
    "storageBucket": environ["storageBucket"],
    "messagingSenderId": environ["messagingSenderId"],
    "serviceAccount": environ["sapath"]
  }

def setUpServiceAccountFile():
    try:
        with open(environ["sapath"], 'r') as f:
            f.write(environ['serviceAccount'])
    except IOError:
        with open(environ["sapath"], 'w') as f:
            f.write(environ['serviceAccount'])

    


# def push(name, phone, bcspogo, aqua):
#     setUpServiceAccountFile()    
#     print("connecting")
#     firebase = pyrebase.initialize_app(config)
#     db = firebase.database()
#     data = {
#         "name": name,
#         "phone": phone,
#         "BCS Pokemon Go": bcspogo,
#         "Team Aqua's Hideout": aqua
#     }
#     print("pushing...")
#     results = db.child("users").push(data)
#     print('finished!\nresults ->')
#     print(results)



# def getData():
#     setUpServiceAccountFile()
#     print("connecting")
#     firebase = pyrebase.initialize_app(config)
#     db = firebase.database()
#     print("retrieving")
#     users = db.child("users").get()
#     print('finished!\nall_users ->')
#     for user in users.val().items():
#         print(user)
#     return users


# def getByServer(server):
#     users = getData()
#     nums = []
#     if server == "BCS Pokemon Go":
#         for user in users.each():
#             # print(user.key())
#             # print(user.val())
#             userDict = user.val()
#             if userDict["BCS Pokemon Go"].lower() == 'true':  #  stored as strings in firebase
#                 print("userDict[\"name\"] -> " + userDict["name"])
#                 print("userDict[\"phone\"] -> " + userDict["phone"])
#                 print("userDict[\"BCS Pokemon Go\"] -> " + userDict["BCS Pokemon Go"])
#                 nums.append(userDict["phone"])
#         return nums

#     if server == "Team Aqua's Hideout":
#         for user in users.each():
#            # print(user.key())
#             # print(user.val())
#             userDict = user.val()
#             if userDict["Team Aqua's Hideout"].lower() == 'true':  #  stored as strings in firebase
#                 print("userDict[\"name\"] -> " + userDict["name"])
#                 print("userDict[\"phone\"] -> " + userDict["phone"])
#                 print("userDict[\"Team Aqua's Hideout\"] -> " + userDict["Team Aqua's Hideout"])
#                 nums.append(userDict["phone"])
#         return nums
#     return nums
            



# def remove(name):
#     setUpServiceAccountFile()
#     print("connecting")
#     firebase = pyrebase.initialize_app(config)
#     db = firebase.database()
#     users = getData()
#     removeKey = "not set"
#     for user in users.each():
#         # print(user.key())
#         # print(user.val())
#         userDict = user.val()
#         if userDict["name"].lower() == name.lower():  #  stored as strings in firebase
#             print("Deleting user -> " + userDict["name"])
#             print("user key -> " + user.key())
#             removeKey = user.key()
#     print("deleting")
#     results = db.child("users").child(removeKey).remove()
#     print("result from delete:")
#     print(results)
    



def upload(data):
    setUpServiceAccountFile()    
    print("connecting")
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    uploadPacket = {
        "dateUploaded": str(datetime.now()),
        "discord_name": data["discord_name"],
        "team": data["team"],
        "gym_name": data["gym_name"],
        "date_extracted": data["date_extracted"],
        "unprocessed_image_to_string": data["unprocessed_image_to_string"],
        "image_url": data["image_url"]
    }
    print("pushing...")
    results = db.child("ex_ocr_testing").push(uploadPacket)
    print('finished!\nresults ->')
    print(results)




def getData():
    setUpServiceAccountFile()
    print("connecting")
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    print("retrieving")
    ocr_data = db.child("ex_ocr_testing").get()
    print('finished!\nocr_data ->')
    for item in ocr_data.val().items():
        print(item)
    return ocr_data



# def logPin(gym, user):
#     setUpServiceAccountFile()    
#     print("connecting")
#     firebase = pyrebase.initialize_app(config)
#     db = firebase.database()
#     data = {
#         "date": str(datetime.now()),
#         "gym": gym,
#         "user": user
#     }
#     print("pushing...")
#     results = db.child("pin_data").push(data)
#     print('finished!\nresults ->')
#     print(results)




# def getLogs():
#     setUpServiceAccountFile()
#     print("connecting")
#     firebase = pyrebase.initialize_app(config)
#     db = firebase.database()
#     print("retrieving logs")
#     data = db.child("logs").get()
#     return data