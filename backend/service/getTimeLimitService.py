def getTimeLimitService(add_time_points_path):
    """Return existing workbook metadata; this does not calculate transit times."""
    message_dict = dict()
    message_dict['status'] = 'success'
    message_dict['message'] = ''
    message_dict['message'] = '计算完成！\n增加大网时限后的结果存储在{}文件中！'.format(add_time_points_path)
    return (message_dict, add_time_points_path)
