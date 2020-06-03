import pandas as pd
from flask import Flask, jsonify, request, render_template
import json
import os
import numpy as np

floor_plan = 'json'

# app
app = Flask(__name__)

# routes
@app.route("/")
def greet():
    return render_template('index.html',name=floor_plan)

@app.route('/req/', methods=['POST'])

def getfp():
	data = request.get_json(force=True)
	global floor_plan
	floor_plan = data
	print(data)
	return render_template('index.html',name=floor_plan)


if __name__ == '__main__':
#    app.run(port = 5000, debug=True)
    app.run()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    