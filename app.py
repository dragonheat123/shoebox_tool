import pandas as pd
from flask import Flask, jsonify, request, render_template
import json
import os
import numpy as np
import pandas as pd

rootPath = os.path.dirname(__file__)
lcaDbPath = os.path.join(rootPath, 'LCA','testcase_db2.csv')
lcaD = pd.read_csv(lcaDbPath)
lcaD = lcaD.set_index("CPID")
lcaD = lcaD.to_json()

#floor_plan = 'json'

floor_plan = '{"int": [[[-15.257157712634401, 4.7831980959440106, 0.0], [-15.257157712634401, 8.9831980959440063, 0.0]], [[-17.957157712634618, 4.7831980959440106, 0.0], [-16.157157712634522, 4.7831980959440106, 0.0]], [[-16.157157712634522, 4.7831980959440106, 0.0], [-15.257157712634401, 4.7831980959440106, 0.0]], [[-15.257157712634401, 4.7831980959440106, 0.0], [-14.357157712634425, 4.7831980959440106, 0.0]], [[-14.357157712634425, 4.7831980959440106, 0.0], [-11.65715771263452, 4.7831980959440106, 0.0]], [[-4.4571577126343591, 4.7831980959440106, 0.0], [-4.4571577126343591, 8.9831980959440063, 0.0]], [[-8.0571577126343534, 4.7831980959440106, 0.0], [-5.3571577126344216, 4.7831980959440106, 0.0]], [[-5.3571577126344216, 4.7831980959440106, 0.0], [-4.4571577126343591, 4.7831980959440106, 0.0]], [[-0.8571577126343648, 4.7831980959440106, 0.0], [-0.8571577126343648, 8.9831980959440063, 0.0]], [[-4.4571577126343591, 4.7831980959440106, 0.0], [-3.5571577126343539, 4.7831980959440106, 0.0]], [[-3.5571577126343539, 4.7831980959440106, 0.0], [-1.7571577126343989, 4.7831980959440106, 0.0]], [[-1.7571577126343989, 4.7831980959440106, 0.0], [-0.8571577126343648, 4.7831980959440106, 0.0]], [[-0.8571577126343648, 4.7831980959440035, 0.0], [0.042842287365640774, 4.7831980959440035, 0.0]], [[0.042842287365640774, 4.7831980959440035, 0.0], [2.7428422873657143, 4.7831980959440035, 0.0]], [[9.9428422873656466, 4.7831980959440106, 0.0], [9.9428422873656466, 8.9831980959440063, 0.0]], [[6.342842287365567, 4.7831980959440106, 0.0], [9.0428422873656391, 4.7831980959440106, 0.0]], [[9.0428422873656391, 4.7831980959440106, 0.0], [9.9428422873656466, 4.7831980959440106, 0.0]], [[13.542842287365641, 4.7831980959440106, 0.0], [13.542842287365641, 8.9831980959440063, 0.0]], [[9.9428422873656466, 4.7831980959440106, 0.0], [10.842842287365682, 4.7831980959440106, 0.0]], [[10.842842287365682, 4.7831980959440106, 0.0], [12.642842287365637, 4.7831980959440106, 0.0]], [[12.642842287365637, 4.7831980959440106, 0.0], [13.542842287365641, 4.7831980959440106, 0.0]], [[13.542842287365641, 4.7831980959440106, 0.0], [14.442842287365703, 4.7831980959440106, 0.0]], [[14.442842287365703, 4.7831980959440106, 0.0], [17.142842287365635, 4.7831980959440106, 0.0]], [[24.342842287365681, 4.7831980959440106, 0.0], [24.342842287365681, 8.9831980959440063, 0.0]], [[20.7428422873658, 4.7831980959440106, 0.0], [23.442842287365707, 4.7831980959440106, 0.0]], [[23.4428422873657, 4.7831980959440106, 0.0], [24.342842287365681, 4.7831980959440106, 0.0]], [[24.342842287365681, 4.7831980959440106, 0.0], [25.2428422873658, 4.7831980959440106, 0.0]], [[25.2428422873658, 4.7831980959440106, 0.0], [27.042842287365897, 4.7831980959440106, 0.0]], [[-16.157157712634522, -0.016801904056011896, 0.0], [-16.157157712634522, 4.7831980959439893, 0.0]], [[-14.357157712634423, -0.016801904056004791, 0.0], [-14.357157712634423, 4.7831980959440106, 0.0]], [[-9.8571577126344234, -0.016801904056004791, 0.0], [-9.8571577126344234, 4.7831980959440106, 0.0]], [[-5.3571577126344216, -0.016801904056004791, 0.0], [-5.3571577126344216, 4.7831980959440106, 0.0]], [[-3.5571577126343534, -0.016801904056008343, 0.0], [-3.5571577126343534, 4.7831980959440106, 0.0]], [[-1.7571577126343989, -0.016801904056011896, 0.0], [-1.7571577126343989, 4.7831980959440106, 0.0]], [[0.042842287365640885, -0.016801904056011896, 0.0], [0.042842287365640885, 4.7831980959440106, 0.0]], [[4.5428422873656409, -0.016801904056011896, 0.0], [4.5428422873656409, 4.7831980959440035, 0.0]], [[9.0428422873656409, -0.016801904056011896, 0.0], [9.0428422873656409, 4.7831980959440035, 0.0]], [[10.842842287365681, -0.016801904056008343, 0.0], [10.842842287365681, 4.7831980959439964, 0.0]], [[12.642842287365635, -0.016801904056008343, 0.0], [12.642842287365635, 4.7831980959439964, 0.0]], [[14.442842287365703, -0.016801904056008343, 0.0], [14.442842287365703, 4.7831980959439964, 0.0]], [[18.942842287365703, -0.016801904056004791, 0.0], [18.942842287365703, 4.7831980959439964, 0.0]], [[23.442842287365703, -0.016801904056004791, 0.0], [23.442842287365703, 4.7831980959439964, 0.0]], [[25.2428422873658, -0.016801904056011896, 0.0], [25.2428422873658, 4.7831980959439893, 0.0]]], "nodes": [{"walls": [[-18.857157712634368, 4.7831980959440106, 0.0], [-15.257157712634401, 4.7831980959440106, 0.0], [-15.257157712634401, 8.9831980959440063, 0.0], [-18.857157712634368, 8.9831980959440063, 0.0], [-18.857157712634368, 4.7831980959440106, 0.0]], "roomtype": "", "floorArea": 15.11999999999985, "center": [-17.057157712634385, 6.8831980959440084, 0.0], "id": 2}, {"walls": [[-15.257157712634401, 4.7831980959440106, 0.0], [-11.65715771263452, 4.7831980959440106, 0.0], [-11.65715771263452, 8.9831980959440063, 0.0], [-15.257157712634401, 8.9831980959440063, 0.0], [-15.257157712634401, 4.7831980959440106, 0.0]], "roomtype": "", "floorArea": 15.119999999999484, "center": [-13.457157712634459, 6.8831980959440076, 0.0], "id": 3}, {"walls": [[-8.0571577126343534, 4.7831980959440106, 0.0], [-4.4571577126343591, 4.7831980959440106, 0.0], [-4.4571577126343591, 8.9831980959440063, 0.0], [-8.0571577126343534, 8.9831980959440063, 0.0], [-8.0571577126343534, 4.7831980959440106, 0.0]], "roomtype": "", "floorArea": 15.119999999999958, "center": [-6.2571577126343563, 6.8831980959440084, 0.0], "id": 4}, {"walls": [[-4.4571577126343591, 4.7831980959440106, 0.0], [-0.8571577126343648, 4.7831980959440106, 0.0], [-0.8571577126343648, 8.9831980959440063, 0.0], [-4.4571577126343591, 8.9831980959440063, 0.0], [-4.4571577126343591, 4.7831980959440106, 0.0]], "roomtype": "", "floorArea": 15.119999999999958, "center": [-2.657157712634362, 6.8831980959440084, 0.0], "id": 5}, {"walls": [[-0.8571577126343648, 4.7831980959440035, 0.0], [2.7428422873657143, 4.7831980959440035, 0.0], [2.7428422873657143, 8.9831980959440063, 0.0], [-0.8571577126343648, 8.9831980959440063, 0.0], [-0.8571577126343648, 4.7831980959440035, 0.0]], "roomtype": "", "floorArea": 15.120000000000339, "center": [0.94284228736567477, 6.8831980959440049, 0.0], "id": 6}, {"walls": [[6.342842287365567, 4.7831980959440106, 0.0], [9.9428422873656466, 4.7831980959440106, 0.0], [9.9428422873656466, 8.9831980959440063, 0.0], [6.342842287365567, 8.9831980959440063, 0.0], [6.342842287365567, 4.7831980959440106, 0.0]], "roomtype": "", "floorArea": 15.120000000000315, "center": [8.1428422873656068, 6.8831980959440084, 0.0], "id": 7}, {"walls": [[9.9428422873656466, 4.7831980959440106, 0.0], [13.542842287365641, 4.7831980959440106, 0.0], [13.542842287365641, 8.9831980959440063, 0.0], [9.9428422873656466, 8.9831980959440063, 0.0], [9.9428422873656466, 4.7831980959440106, 0.0]], "roomtype": "", "floorArea": 15.119999999999958, "center": [11.742842287365644, 6.8831980959440084, 0.0], "id": 8}, {"walls": [[13.542842287365641, 4.7831980959440106, 0.0], [17.142842287365635, 4.7831980959440106, 0.0], [17.142842287365635, 8.9831980959440063, 0.0], [13.542842287365641, 8.9831980959440063, 0.0], [13.542842287365641, 4.7831980959440106, 0.0]], "roomtype": "", "floorArea": 15.119999999999958, "center": [15.342842287365638, 6.8831980959440084, 0.0], "id": 9}, {"walls": [[20.7428422873658, 4.7831980959440106, 0.0], [24.342842287365681, 4.7831980959440106, 0.0], [24.342842287365681, 8.9831980959440063, 0.0], [20.7428422873658, 8.9831980959440063, 0.0], [20.7428422873658, 4.7831980959440106, 0.0]], "roomtype": "", "floorArea": 15.119999999999479, "center": [22.542842287365737, 6.8831980959440084, 0.0], "id": 10}, {"walls": [[24.342842287365681, 4.7831980959440106, 0.0], [27.942842287365647, 4.7831980959440106, 0.0], [27.942842287365647, 8.9831980959440063, 0.0], [24.342842287365681, 8.9831980959440063, 0.0], [24.342842287365681, 4.7831980959440106, 0.0]], "roomtype": "", "floorArea": 15.119999999999838, "center": [26.142842287365657, 6.8831980959440076, 0.0], "id": 11}, {"walls": [[-17.957157712634618, -0.016801904056011896, 0.0], [-16.157157712634522, -0.016801904056011896, 0.0], [-16.157157712634522, 4.7831980959439893, 0.0], [-17.957157712634618, 4.7831980959439893, 0.0], [-17.957157712634618, -0.016801904056011896, 0.0]], "roomtype": "", "floorArea": 8.640000000000466, "center": [-17.05715771263457, 2.3831980959439889, 0.0], "id": 12}, {"walls": [[-16.157157712634522, -0.016801904056004791, 0.0], [-14.357157712634423, -0.016801904056004791, 0.0], [-14.357157712634423, 4.7831980959440106, 0.0], [-16.157157712634522, 4.7831980959440106, 0.0], [-16.157157712634522, -0.016801904056004791, 0.0]], "roomtype": "", "floorArea": 8.6400000000004962, "center": [-15.257157712634474, 2.3831980959440027, 0.0], "id": 13}, {"walls": [[-14.357157712634423, -0.016801904056004791, 0.0], [-9.8571577126344234, -0.016801904056004791, 0.0], [-9.8571577126344234, 4.7831980959440106, 0.0], [-14.357157712634423, 4.7831980959440106, 0.0], [-14.357157712634423, -0.016801904056004791, 0.0]], "roomtype": "", "floorArea": 21.600000000000072, "center": [-12.107157712634425, 2.3831980959440027, 0.0], "id": 14}, {"walls": [[-9.8571577126344234, -0.016801904056004791, 0.0], [-5.3571577126344216, -0.016801904056004791, 0.0], [-5.3571577126344216, 4.7831980959440106, 0.0], [-9.8571577126344234, 4.7831980959440106, 0.0], [-9.8571577126344234, -0.016801904056004791, 0.0]], "roomtype": "", "floorArea": 21.60000000000008, "center": [-7.6071577126344243, 2.3831980959440036, 0.0], "id": 15}, {"walls": [[-5.3571577126344216, -0.016801904056008343, 0.0], [-3.5571577126343534, -0.016801904056008343, 0.0], [-3.5571577126343534, 4.7831980959440106, 0.0], [-5.3571577126344216, 4.7831980959440106, 0.0], [-5.3571577126344216, -0.016801904056008343, 0.0]], "roomtype": "", "floorArea": 8.6400000000003629, "center": [-4.4571577126343875, 2.3831980959440013, 0.0], "id": 16}, {"walls": [[-3.5571577126343534, -0.016801904056011896, 0.0], [-1.7571577126343989, -0.016801904056011896, 0.0], [-1.7571577126343989, 4.7831980959440106, 0.0], [-3.5571577126343534, 4.7831980959440106, 0.0], [-3.5571577126343534, -0.016801904056011896, 0.0]], "roomtype": "", "floorArea": 8.6399999999998194, "center": [-2.6571577126343762, 2.3831980959439987, 0.0], "id": 17}, {"walls": [[-1.7571577126343989, -0.016801904056011896, 0.0], [0.042842287365640885, -0.016801904056011896, 0.0], [0.042842287365640885, 4.7831980959440106, 0.0], [-1.7571577126343989, 4.7831980959440106, 0.0], [-1.7571577126343989, -0.016801904056011896, 0.0]], "roomtype": "", "floorArea": 8.6400000000002315, "center": [-0.85715771263437901, 2.3831980959439991, 0.0], "id": 18}, {"walls": [[0.042842287365640885, -0.016801904056011896, 0.0], [4.5428422873656409, -0.016801904056011896, 0.0], [4.5428422873656409, 4.7831980959440035, 0.0], [0.042842287365640885, 4.7831980959440035, 0.0], [0.042842287365640885, -0.016801904056011896, 0.0]], "roomtype": "", "floorArea": 21.600000000000069, "center": [2.2928422873656409, 2.3831980959439956, 0.0], "id": 19}, {"walls": [[4.5428422873656409, -0.016801904056011896, 0.0], [9.0428422873656409, -0.016801904056011896, 0.0], [9.0428422873656409, 4.7831980959440035, 0.0], [4.5428422873656409, 4.7831980959440035, 0.0], [4.5428422873656409, -0.016801904056011896, 0.0]], "roomtype": "", "floorArea": 21.600000000000069, "center": [6.7928422873656418, 2.3831980959439956, 0.0], "id": 20}, {"walls": [[9.0428422873656409, -0.016801904056008343, 0.0], [10.842842287365681, -0.016801904056008343, 0.0], [10.842842287365681, 4.7831980959439964, 0.0], [9.0428422873656409, 4.7831980959439964, 0.0], [9.0428422873656409, -0.016801904056008343, 0.0]], "roomtype": "", "floorArea": 8.6400000000001995, "center": [9.9428422873656608, 2.3831980959439942, 0.0], "id": 21}, {"walls": [[10.842842287365681, -0.016801904056008343, 0.0], [12.642842287365635, -0.016801904056008343, 0.0], [12.642842287365635, 4.7831980959439964, 0.0], [10.842842287365681, 4.7831980959439964, 0.0], [10.842842287365681, -0.016801904056008343, 0.0]], "roomtype": "", "floorArea": 8.6399999999997892, "center": [11.742842287365658, 2.3831980959439942, 0.0], "id": 22}, {"walls": [[12.642842287365635, -0.016801904056008343, 0.0], [14.442842287365703, -0.016801904056008343, 0.0], [14.442842287365703, 4.7831980959439964, 0.0], [12.642842287365635, 4.7831980959439964, 0.0], [12.642842287365635, -0.016801904056008343, 0.0]], "roomtype": "", "floorArea": 8.6400000000003345, "center": [13.542842287365669, 2.3831980959439942, 0.0], "id": 23}, {"walls": [[14.442842287365703, -0.016801904056004791, 0.0], [18.942842287365703, -0.016801904056004791, 0.0], [18.942842287365703, 4.7831980959439964, 0.0], [14.442842287365703, 4.7831980959439964, 0.0], [14.442842287365703, -0.016801904056004791, 0.0]], "roomtype": "", "floorArea": 21.600000000000001, "center": [16.692842287365703, 2.383198095943996, 0.0], "id": 24}, {"walls": [[18.942842287365703, -0.016801904056004791, 0.0], [23.442842287365703, -0.016801904056004791, 0.0], [23.442842287365703, 4.7831980959439964, 0.0], [18.942842287365703, 4.7831980959439964, 0.0], [18.942842287365703, -0.016801904056004791, 0.0]], "roomtype": "", "floorArea": 21.600000000000001, "center": [21.192842287365703, 2.383198095943996, 0.0], "id": 25}, {"walls": [[23.442842287365703, -0.016801904056011896, 0.0], [25.2428422873658, -0.016801904056011896, 0.0], [25.2428422873658, 4.7831980959439893, 0.0], [23.442842287365703, 4.7831980959439893, 0.0], [23.442842287365703, -0.016801904056011896, 0.0]], "roomtype": "", "floorArea": 8.6400000000004376, "center": [24.342842287365752, 2.383198095943988, 0.0], "id": 26}, {"walls": [[25.2428422873658, -0.016801904056011896, 0.0], [27.042842287365897, -0.016801904056011896, 0.0], [27.042842287365897, 4.7831980959439893, 0.0], [25.2428422873658, 4.7831980959439893, 0.0], [25.2428422873658, -0.016801904056011896, 0.0]], "roomtype": "", "floorArea": 8.6400000000004731, "center": [26.142842287365848, 2.3831980959439885, 0.0], "id": 27}]}'

out = "nothing"
#floor = None
parcel_req = "nothing"

# app
app = Flask(__name__)

# routes
@app.route("/")
def greet():
    return render_template('index.html',name=floor_plan,lcaData = lcaD)

@app.route('/req/', methods=['POST'])

def getfp():
	data = request.get_json(force=True)
	global floor_plan
	floor_plan = json.dumps(data)
	print("received")
	return render_template('index.html',name=floor_plan,lcaData = lcaD)

@app.route('/get/',methods=['POST'])
def get_output():
	global out
	out = request.get_json(force=True)
	print("submitted")
	return "ok"

@app.route('/get/',methods=['GET'])
def output():
	print("queried")
	return json.dumps(out)

@app.route('/parcel/',methods=['POST'])
def parcel():
	print("parcellation_output")
	global parcel_req
	parcel_req = request.get_json(force=True)
	return "ok"

@app.route('/parcel/',methods=['GET'])
def parcel_out():
	print("parc_queried")
	return json.dumps(parcel_req)




if __name__ == '__main__':
#    app.run(port = 5000, debug=True)
    app.run()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    