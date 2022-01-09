from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

leaf_apices = {'accuminate': ['n1', 'n2', 'n3', 'n4', 'n5', 'n7', 'n8', 'n9', 'n10', 'n31', 'leaf1', 'leaf2', 'leaf3', 'leaf6', 'leaf7', 'leaf9', 'leaf11', 'leaf12', 'leaf14'],
               'acute': ['leaf5', 'leaf8', 'leaf10', 'leaf13', 'leaf15'],
               'obtuse': ['leaf4'],
               'rounded': ['n6']
               }

leaf_bases = {'acute': ['leaf5'],
              'attenuate': ['n4', 'n5'],
              'auriculate': ['leaf4'],
              'cordate': ['n1', 'n6', 'n8', 'leaf6', 'leaf11', 'leaf12'],
              'cuneate': ['n3'],
              'cunneate': ['n7', 'n31', 'leaf7'],
              'hastate': ['leaf2'],
              'oblique': ['leaf1', 'leaf3', 'leaf9', 'leaf10', 'leaf13', 'leaf14', 'leaf15'],
              'rounded': ['n2', 'n9', 'n10', 'leaf8']}

leaf_margin = {'dantate': ['leaf9'],
               'doubly_serrate': ['n8', 'leaf1', 'leaf5', 'leaf14'],
               'entire': ['n2', 'n4', 'n6', 'n7', 'n9', 'n10'],
               'lobed': ['leaf4'],
               'serrate': ['n1', 'leaf6', 'leaf8', 'leaf10', 'leaf13'],
               'serrulate': ['leaf3', 'leaf7', 'leaf11', 'leaf12'],
               'sinuate': ['n5'],
               'spinose': ['leaf2'],
               'undulate': ['n3', 'n31', 'leaf15']}


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/second")
def secondpage():
    return render_template('second.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/refer")
def refer():
    return render_template('refer.html')


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


@app.route("/predict", methods=["GET", "POST"])
def calc():
    data = request.get_json()
    # // leaf_apices , leaf_margin, leaf_bases
    finalArray = []
    for arr in data:
        key = [k for k in arr.keys()]
        key = key[0]
        if key == 'leaf_margin':
            finalArray.append(leaf_margin[arr['leaf_margin']])
        if key == 'leaf_bases':
            finalArray.append(leaf_bases[arr['leaf_bases']])
        if(key == 'leaf_apices'):
            finalArray.append(leaf_apices[arr['leaf_apices']])
    finalImages = []
    if len(finalArray) == 0:
        pass
    elif len(finalArray) == 1:
        finalImages = getFileNames(finalArray[0])
        print(finalArray[0])
        # pass
    else:
        st = set.intersection(*[set(x) for x in finalArray])
        ans = []
        for folder in st:
            ans.append(folder)
        print(ans)
        finalImages = getFileNames(ans)

    return json.dumps(finalImages)


app.run(debug=True)
