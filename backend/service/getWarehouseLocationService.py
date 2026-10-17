from algorithm_boundary import create_warehouse_model
from paths import *

def getWarehouseLocationService(data, time_cost_path, spec_warehouses_data='df', algorithm_type='auto', bool_spec_warehouse=False, n_clusters=4, result_dir='./data'):
    message_dict = dict()
    message_dict['status'] = 'success'
    message_dict['message'] = ''
    algorithm_type = 'auto'
    try:
        if bool_spec_warehouse:
            mcgds = create_warehouse_model(fixed_warehouses=True, n_clusters=n_clusters, seed=42, init=algorithm_type)
            mcgds.setDefineStores(spec_warehouses_data, '详细地址', '经度', '纬度')
            mcgds.fit(data, '详细地址', '经度', '纬度', '销售量（吨）', '运输费率（元/吨公里）')
            (df_add_time_points, dict_result) = mcgds.predict(time_cost_path)
        else:
            mcg = create_warehouse_model(fixed_warehouses=False, n_clusters=n_clusters, seed=1011, init=algorithm_type)
            mcg.fit(data, '详细地址', '经度', '纬度', '销售量（吨）', '运输费率（元/吨公里）')
            (df_add_time_points, dict_result) = mcg.predict(time_cost_path)
        df_add_time_points.to_excel(add_time_points_path, index=False)
        map_list = []
        for k in dict_result.keys():
            for v in dict_result[k]:
                map_list.append({'coords': [[k[1], k[2]], [v[1], v[2]]]})
        message_dict['map_list'] = map_list
        return message_dict
    except Exception as e:
        message_dict['status'] = 'fail'
        message_dict['message'] = repr(e)
        return message_dict
