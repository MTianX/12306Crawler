from prettytable import PrettyTable as pt
import json

def display(datas):
    index = 0
    with open('StationNames.txt','r',encoding='utf-8') as f:
        StationNames_str = f.read()
    StationNames = json.loads(StationNames_str)
    NewStationNames = {v:k for k,v in StationNames.items()}

    tb = pt(("序号 车次 出发站 到达站 出发时间 到达时间 历时 一等座 二等座").split(' '))
    for data in datas:
        for i in data:
            if data[i] == '':
                data[i] = '--'
        tb.add_row(
            [str(index), data['车次'],
             NewStationNames[data['出发站']].replace(' ', ''),
             NewStationNames[data['到达站']].replace(' ', ''),
             data['出发时间'],
             data['到达时间'],
             data['历时'],
             data['一等座'],
             data['二等座']])
        index = index + 1
    print(tb)


if __name__ == '__main__':
    with open('train_data.txt', 'r', encoding='utf-8') as f:
        data_str = f.read()
    train_datas = json.loads(data_str)
    display(train_datas)
