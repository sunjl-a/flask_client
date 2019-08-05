import requests
def city_name():
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9063'
    city_code = requests.get(url)
    city_code_list = city_code.text.split("|")
    city_dict = {}
    for k, i in enumerate(city_code_list):
        if '@' in i:
            # 城市名作为字典的键，城市编号作为字典的值
            city_dict[city_code_list[k + 1]] = city_code_list[k + 2]
    return city_dict

def get_info(train_date, from_station, to_station):
    # 将城市名转换成城市编号
    city_dict = city_name()
    from_station = city_dict[from_station]
    to_station = city_dict[to_station]
    # 发送请求
    params = {
        'leftTicketDTO.train_date': train_date,
        'leftTicketDTO.from_station': from_station,
        'leftTicketDTO.to_station': to_station,
        'purpose_codes': 'ADULT'
    }
    # 通过try……except方式分别对不同的URL进行访问
    try:
        url = 'https://kyfw.12306.cn/otn/leftTicket/query'
        r = requests.get(url, params=params)
        info_text = r.json()['data']['result']
    except:
        url = 'https://kyfw.12306.cn/otn/leftTicket/queryA'
        r = requests.get(url, params=params)
        info_text = r.json()['data']['result']
    # 获取响应内容并提取有效数据
    info_list = []
    for i in info_text:
        info_dict = {}
        train_info = i.split('|')
        info_dict['train_no'] = train_info[3]
        info_dict['start_time'] = train_info[8]
        info_dict['end_time'] = train_info[9]
        info_dict['interval_time'] = train_info[10]
        info_dict['second_seat'] = train_info[30]
        info_dict['frist_seat'] = train_info[31]
        info_dict['special_seat'] = train_info[32]
        info_list.append(info_dict)
    return info_list

if __name__ == '__main__':
    train_date = '2018-10-29'
    from_station = '广州'
    to_station = '武汉'
    info = get_info(train_date, from_station, to_station)
    print(str(info))
