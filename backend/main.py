import os
from flask import Flask, request, Response, send_file, make_response
from flask_cors import CORS
import pandas as pd
import json
from service.getWarehouseLocationService import getWarehouseLocationService
from utils.check import *
from service.getTimeLimitService import getTimeLimitService
from service.getRoutePlanService import getRoutePlanService
from paths import *
app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/')
def index():
    return 'Portfolio source excerpt; see README for omitted resources.'

@app.route('/upload/warehouseData', methods=['post'])
def uploadWarehouseData():
    file = request.files.get('file')
    file.save(input_file_path)
    message = {'status': 'success'}
    return Response(json.dumps(message), mimetype='application/json')

@app.route('/upload/routePlanData', methods=['post'])
def uploadRoutePlanData():
    file = request.files.get('file')
    file.save(routeplan_input_file_path)
    message = {'status': 'success'}
    return Response(json.dumps(message), mimetype='application/json')

@app.route('/download/routeplan_result', methods=['post'])
def downloadRoutePlanResult():
    message_dict = {'status': 'success', 'message': '', 'filename': ''}
    message_dict['filename'] = os.path.basename(routeplan_result_path)
    response = make_response(send_file(routeplan_result_path, as_attachment=True))
    response.headers['message_dict'] = json.dumps(message_dict)
    response.headers['Access-Control-Expose-Headers'] = 'message_dict'
    return response

@app.route('/getWarehouseLocation', methods=['post'])
def getWarehouseLocationController():
    message = {'status': 'success'}
    form_dict = request.get_json()
    check_file = checkFile()
    data_demand_points = pd.read_excel(input_file_path, sheet_name='需求点')
    check_result = check_file.check(data_demand_points, file_type='需求点')
    if check_result['status'] != 'success':
        message = check_result
        return Response(json.dumps(message), mimetype='application/json')
    if form_dict['specWarehouse'] == '指定仓':
        data_spec_warehouse = pd.read_excel(input_file_path, sheet_name='指定仓')
        check_result = check_file.check(data_spec_warehouse, file_type='指定仓')
        if check_result['status'] != 'success':
            message = check_result
            return Response(json.dumps(message), mimetype='application/json')
    if form_dict['specWarehouse'] == '指定仓':
        message_dict = getWarehouseLocationService(data=pd.read_excel(input_file_path, sheet_name='需求点'), time_cost_path=time_cost_path, spec_warehouses_data=pd.read_excel(input_file_path, sheet_name='指定仓'), n_clusters=int(form_dict['warehouseLocationNumber']), bool_spec_warehouse=True, algorithm_type=form_dict['algori'], result_dir=base_dir)
    else:
        message_dict = getWarehouseLocationService(data=pd.read_excel(input_file_path, sheet_name='需求点'), time_cost_path=time_cost_path, n_clusters=int(form_dict['warehouseLocationNumber']), bool_spec_warehouse=False, algorithm_type=form_dict['algori'], result_dir=base_dir)
    return Response(json.dumps(message_dict), mimetype='application/json')

@app.route('/getTimeLimit', methods=['get', 'post'])
def getTimeLimitController():
    message = {'status': 'success', 'message': '', 'filename': ''}
    (message_dict, add_time_limit_path) = getTimeLimitService(add_time_points_path)
    if message_dict['status'] == 'success':
        message_dict['filename'] = os.path.basename(add_time_points_path)
        response = make_response(send_file(add_time_points_path, as_attachment=True))
    else:
        response = make_response()
    response.headers['message_dict'] = json.dumps(message_dict)
    response.headers['Access-Control-Expose-Headers'] = 'message_dict'
    return response

@app.route('/routeplan_result2', methods=['post'])
def getRoutePlanResultController2():
    message = {'status': 'success', 'message': '', 'filename': ''}
    form_dict = request.get_json()
    inputfile = routeplan_input_file_path
    use_cache_flag = False
    time_limit = 10
    obj = 'cost'
    strategy = '长期规划'
    pickup_delivery = '取货'
    form_dict = request.get_json()
    strategy = form_dict['strategy']
    pickup_delivery = form_dict['pickup_delivery']
    time_limit = int(form_dict['time_limit'])
    max_residence_time = float(form_dict['waiting_time'])
    use_cache_flag = False if form_dict['use_cache_flag'] == '否' else True
    message_dict = getRoutePlanService(inputfile=inputfile, use_cache_flag=use_cache_flag, obj=obj, time_limit=time_limit, strategy=strategy, max_residence_time=max_residence_time, pickup_delivery=pickup_delivery)
    response = make_response()
    response.headers['message_dict'] = json.dumps(message_dict)
    response.headers['Access-Control-Expose-Headers'] = 'message_dict'
    return response
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
