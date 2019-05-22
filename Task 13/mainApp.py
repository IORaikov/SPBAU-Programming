#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import flask
import gauss
from flask import Flask, request
import numpy as np
app = Flask(__name__, static_folder="static", static_url_path="", template_folder="templates")

# @app.route('/hello/<string:text>')
# @app.route('/hello')
# def hello_world(text=None):
#     return 'Just a plain text: "Hello from Flask!"' + (' With param ' + text if text else '')


@app.route('/')
def root():
    return flask.render_template(
        'index.html'
    )


@app.route('/name', methods = ['GET', 'POST'])
def hello_name():
    if request.method == 'GET':
        name_param=request.args.get('name')
    elif request.method == 'POST':
        name_param=request.form.get('name')

    if name_param==None:
        name_param="Анонимус"

    return flask.render_template(
        'name.html',
        name=name_param,
        method=request.method
    )

@app.route('/gauss', methods = ['GET'])
def solveGauss():
    A = parseMatrixFromString(request.args.get('a'))
    B = parseMatrixFromString(request.args.get('b'))
    if(A.shape[0]!=0 and B.shape[0]!=0):
        eqs = max(A.shape[0],B.shape[0])
        A=shapeMatrix((eqs,eqs),A)
        B=shapeMatrix((eqs,1),B)
        #print(f"A={A},B={B}")
        print(A.shape,B.shape)
        print(A)
        print(B)
        res=gauss.gauss_nojit(A,B)
        print(res)
    else:
        res=""
    return flask.render_template(
        'gauss.html',
        a=A,b=B,
        result=str(res),
        method = 'GET'
    )
def shapeMatrix(shape,matrix):
    result = np.zeros(shape=shape)
    mShape = matrix.shape
    for i in range(mShape[0]):
        if i>=shape[0]:
                break
        for j in range(mShape[1]):
            if j>=shape[1]:
                break
            result[i][j]=matrix[i][j]
    return result
def parseMatrixFromString(string=""):
    if not isinstance(string, str):
        string = ""
    #Как ни странно, я не нашел простого готового решения даже для массивов вида [[1,5,...,7],...,[...]] 
    lines = string.splitlines()
    result = []
    for line in lines:
        linres=[]
        words = line.split(' ')
        for word in words:
            try:
                linres.append(np.float64(word))
            except:
                continue
        if len(linres)==0:
            linres.append(0)
        result.append(linres)
    return np.array(result)
if __name__ == '__main__':
   app.run(debug = True)
