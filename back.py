from flask import Flask, render_template, request, make_response, jsonify, send_from_directory
from random import randint
import os
import Number as Number
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html', the_title="laba")


@app.route("/gen", methods=['POST'])
def gen():
    req = request.get_json()
    isError = 0
    print(req["gen_type"])
    if req["gen_type"] == "P":
        try:
            pol = Number.Polynomial("gen-{}-3".format(req["len"]))
        except:
            isError = 1
            res = {"error": -1}
        if isError == 0:
            res = {"generated": pol.show("get")}
    else:
        try:
            num = Number.Number("gen-{}".format(req["len"]))
        except:
            isError = 1
            res = {"error": -1}
        if isError == 0:
            if (req["sign"] == "2"):
                num.updateSign(randint(0, 1))
            else:
                num.updateSign(int(req["sign"]))
            num = num.show("get")
            res = {"generated": str(num)}

    return make_response(jsonify(res))

@app.route("/getInfo", methods=['POST'])
def getInfo():
    req = request.get_json()
    if req["type"] in Number.content:
        print(req["type"])
        print(Number.content[req["type"]])
        print(Number.content[req["type"]]["info"])
        res = jsonify(Number.content[req["type"]]["info"])
    else:
        res = jsonify({"error": -1})
    return make_response(res)

@app.route("/process", methods=['POST'])
def process():
    req = request.get_json()
    print("req['input']", req["input"])
    for i in range(len(req["input"])):
        numberValues= ["N", "Z"]
        intValue = ["i+", "i-"]
        if Number.content[req["type"]]["info"]["argsTypes"][i] in numberValues:
            req["input"][i] = Number.Number(req["input"][i])
        elif Number.content[req["type"]]["info"]["argsTypes"][i] == "Q":
            req["input"][i][0] = Number.Number(req["input"][i][0])
            req["input"][i][1] = Number.Number(req["input"][i][1])
        elif Number.content[req["type"]]["info"]["argsTypes"][i] in intValue:
            req["input"][i] = int(req["input"][i])
        elif Number.content[req["type"]]["info"]["argsTypes"][i] == "P":
            for k in range(len(req["input"][i])):
                req["input"][i][k] = [[Number.Number(req["input"][i][k][0][0]), Number.Number(req["input"][i][k][0][1])], int(req["input"][i][k][1])] #обрабатываем каждый элемент полинома
            req["input"][i] = Number.Polynomial(req["input"][i]) #создаём полином
    try:
        res = Number.content[req["type"]]["link"](*req["input"])
    except:
        res = -1
    #print(res)

    if type(res) == Number.Number:
        res = {"result": str(res.show("get"))}
    elif type(res) == Number.Polynomial:
        res = {"result": res.show("get")}

    elif type(res) == list:
        for i in range(len(res)):
            if type(res[i]) == Number.Number:
                res[i] = str(res[i].show("get"))
            elif type(res[i]) == Number.Polynomial:
                res[i] = res[i].show("get")
            elif type(res[i]) == list:
                for j in range(len(res[i])):
                    if type(res[i][j]) == Number.Number:
                        res[i][j] = str(res[i][j].show("get"))
                    elif type(res[i][j]) == Number.Polynomial:
                        res[i][j] = res[i][j].show("get")
        print(res)
        res = {"result": res}
    else:
        if res == -1:
            res = {"error": -1}
        else:
            res = {"result": str(res)}
    print(res)
    return make_response(jsonify(res))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='img/Vinni.png')

app.run()
