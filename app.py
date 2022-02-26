
from multiprocessing.sharedctypes import Value
from flask import Flask, render_template, request
import MySQLdb
db = MySQLdb.connect("localhost", "root", "", "project")
import json
import os
from flask_cors import CORS,cross_origin
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, support_credentials=True)

#generating sql commands
def create_sql_comand(keys,value):
    str1="select leaf_division from leaf where "
    for index in range(0,len(keys)-1):
        str1=str1+f"{keys[index]}='{value[index]}' and "
    str1=str1+f"{keys[len(keys)-1]}='{value[len(keys)-1]}'"
    return str1

#getting images path from contained folder
def getFileNames(folderNames):
    IMAGES_PATH = './static/dataset/'
    answer = {}
    fileName = []
    for folder in folderNames:
        allfiles = os.listdir(IMAGES_PATH+folder)
        for file in allfiles:
            fileName.append((IMAGES_PATH.split(".")[1]).split(
                "/")[2] + "/" + folder + "/" + file)
        answer[folder] = fileName
        fileName = []
    return answer

#recive client server call

@app.route("/predict", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def calc():
    data = request.get_json()
    print(data);
    print(type(data));
    keys=[]
    value=[]
    
    for arr in data:
         keys.append(arr)
        #  print(key,key[0])
         value.append(data[arr])
    

    command = create_sql_comand(keys,value)
    curs = db.cursor()  #create a curser to database for  data extraction
    print(command)
    try:
        curs.execute(command)
        folder=curs.fetchall() #insert extracted data to folder variable
        intersection_folder=[]
        for foll in folder:
            print(foll[0])
            intersection_folder.append(foll[0])
        filenames= getFileNames(intersection_folder)
        print(filenames)
        return json.dumps(filenames) #dump data from server to client
    except:
        print( "Error: unable to fetch items")
        return json.dumps({})   #dump data from server to client

app.run(debug=True)