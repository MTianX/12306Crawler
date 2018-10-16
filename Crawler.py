#coding=utf-8
import requests
import json
import re
import time
import codecs
from API import API
from Configure import Configure
import urllib.parse
from display import display
from decorator import log


#八张验证码图片的位置，模拟坐标
#从上到下，从左至右
#1  2   3   4
#5  6   7   8
PngData = {
        '1':'41,36',
        '2':'102,49',
        '3':'180,45',
        '4':'252,43',
        '5':'41,118',
        '6':'109,116',
        '7':'181,116',
        '8':'259,119'
}

headers = {
        'Referer': 'https://kyfw.12306.cn/otn/login/init',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Host':'kyfw.12306.cn',
}


class Crawlerkyfw():
    def __init__(self):
        self.Session = requests.Session()
        with open('StationNames.txt','r',encoding='utf-8') as f:
            str = f.read()
        self.StationName = json.loads(str)
        self.train_date = Configure.TRAIN_DATE
        self.from_station_input = Configure.FROM_STATION
        self.to_station_input = Configure.TO_STATION
        self.from_station = self.StationName[self.from_station_input]
        self.to_station = self.StationName[self.to_station_input]
        self.seatType = Configure.SEAT_TYPE_CODE
        self.choose_seats = Configure.CHOOSE_SEATS

        self.name = Configure.PASSENGERS_NAME
        self.IDcard = Configure.PASSENGERS_ID
        self.tell = Configure.PASSENGERS_TELL

    @log
    def captcha_input(self):
        #请求验证码，并输入，返回正确图片位置
        res1 = self.Session.get(API.captcha_image, headers=headers)  # 请求验证码
        with open('code.jpeg', 'wb') as f:
            f.write(res1.content)
        print("正在写入验证码图片")
        InputData = input("输入正确的验证码：").split(',')
        Data = ''
        for i in InputData:
            if Data.strip() == "":
                Data = PngData[i]
            else:
                Data = Data + ',' + PngData[i]

        captcha_data = {
            'answer': Data,
            'login_site': 'E',
            'rand': 'sjrand'
        }
        print(captcha_data)
        res2 = self.Session.post(API.captcha_check, data=captcha_data, headers=headers)
        #提交验证码
        print(res2.text)
        return res2.text

    @log
    def uamtkCheck(self):
        # 用户密码验证成功后请求uamtk验证，验证通过后即正常登录
        # 第一次
        data = {
            'appid': 'otn'}
        res1 = self.Session.post(API.uamtk, data=data, headers=headers)
        uamtk_data1 = json.loads(res1.text)
        # 第二次
        data = {
            'tk': uamtk_data1['newapptk']
        }
        headers['Referer'] = 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin'
        #更新Referer

        res2 = self.Session.post(API.uamauthclient, data=data, headers=headers)
        uamtk_data2 = json.loads(res2.text)
        return uamtk_data2

    @log
    def login(self):
        #登录的一系列动作
        res = self.Session.get(API.user,headers = headers)
        data = {
            'username': Configure.USER_NAME,
            'password': Configure.USER_PWD,
            'appid': 'otn'
        }
        try:
            if json.loads(self.captcha_input())['result_code'] == '4':#判断验证码是否通过
                res1 = self.Session.post(API.login_url,data= data,headers= headers)#推送用户名密码
                res1_data = json.loads(res1.text)
                res2_data = self.uamtkCheck()
                print(res2_data)
                if res2_data['result_code'] == 0:
                    res4 = self.Session.get(API.initMy12306,headers= headers)#请求用户界面
                    if res4.text.find(res2_data['username']):
                        print("%s,登录成功"%res2_data['username'])
                        return 1
                    else:
                        return 0

        except:
            print('error')
            return 0
        # print(res.text)

    @log
    def loginOut(self):
        #注销
        try:
            headers['Referer'] = 'https://kyfw.12306.cn/otn/index/initMy12306'
            res1 = self.Session.get(API.loginOut,headers = headers)
            res2 = self.Session.get(API.user,headers = headers)
            headers['Referer'] = 'https://kyfw.12306.cn/otn/login/init'
            data = {
                'appid':'otn'
            }
            res3 = self.Session.post(API.uamtk,headers = headers,data = data)
            if json.loads(res3.text)['result_code'] == 3:
                print("用户已注销")
        except:
            print("error")

    @log
    def TicketCheck(self):
        #余票查询

        #查询接口
        url = 'https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date={}' \
              '&leftTicketDTO.from_station={}' \
              '&leftTicketDTO.to_station={}' \
              '&purpose_codes=ADULT'.format(self.train_date,self.from_station,self.to_station)

        headers['Referer'] = 'https://kyfw.12306.cn/otn/leftTicket/init'
        try:
            res1 = self.Session.get(url = API.leftTicket_init,headers = headers)
            res = self.Session.get(url,headers = headers)
            TicketData = json.loads(res.text)['data']['result']
            train_data = []
            for i in TicketData:
                data = i.split('|')
                into ={
                    '车次':data[3],
                    '日期': data[13],
                    '起始站': data[4],
                    '终点站': data[5],
                    '出发站': data[6],
                    '到达站': data[7],
                    '出发时间': data[8],
                    '到达时间': data[9],
                    '历时': data[10],
                    '一等座': data[31],
                    '二等座': data[30],
                    '高级软卧':data[21],
                    '软卧':data[23],
                    '硬卧':data[28],
                    '硬座':data[29],
                    'secretStr': data[0]
                }
                train_data.append(into)
            str = json.dumps(train_data,ensure_ascii=False)
            with codecs.open('train_data.txt','w+',encoding='utf-8') as f:
                f.write(str)
            display(train_data)
            InputData = int(input("输入选择的序号："))
            self.select_train = train_data[InputData]
            print('选择的序号为{},车次为{}'.format(InputData,self.select_train['车次']))
        except:
            print('error')
            pass

    @log
    def GetStationNames(self):
        #获取站名
        try:
            res = requests.get(API.station_name,headers = headers)
            data = res.text.split('@')
            StationNames = {}
            for i in data[1:]:
                StationData  = i.split('|')
                into = {
                    StationData[1]:StationData[2]
                }
                StationNames.update(into)
            StationNames_str = json.dumps(StationNames,ensure_ascii=False)
            with open('StationNames.txt','w',encoding='utf-8') as f:
                f.write(StationNames_str)
        except:
            print('error')

    @log
    def checkUser(self):
        #检查用户是否在线
        try:
            headers['Referer'] = API.leftTicket_init
            data = {
                '_json_att': ''
            }
            res1 = self.Session.post(API.checkUser,headers = headers,data=data)
            return json.loads(res1.text)['data']['flag']
        except:
            pass

    @log
    def leftTicket(self):
        headers['Referer'] = API.leftTicket_init
        try:
            data = {
                'back_train_date': self.train_date,
                'purpose_codes': 'ADULT',
                'query_from_station_name': self.from_station_input,
                'query_to_station_name': self.to_station_input,
                'secretStr': urllib.parse.unquote(self.select_train['secretStr']),
                'tour_flag': 'dc',
                'train_date': self.train_date,
                'undefined': ''
            }
            print(data)
            res2 = self.Session.post(API.submitOrderRequest,headers = headers,data = data)
            print(res2.text)
            return json.loads(res2.text)['status']
        except:
            pass

    @log
    def initDc(self):
        #初始化订单提交页面
        data = {
            '_json_att': ''
        }
        try:
            res3 = self.Session.post(API.initDc, headers=headers, data=data)
            self.RepeatSubmitToken = re.findall("globalRepeatSubmitToken = (.*?);", res3.text)[0].replace("'",'')
            ticketInfoForPassengerForm_str = re.findall("ticketInfoForPassengerForm=(.*?);",res3.text)[0].replace("'", '"')
            print(ticketInfoForPassengerForm_str)
            self.ticketInfoForPassengerForm = json.loads(ticketInfoForPassengerForm_str)
        except:
            pass

    @log
    def GetconfirmPassenger(self):
    #获取联系人
        headers['Referer'] = API.initDc
        data = {
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.RepeatSubmitToken
        }
    # 联系人数据处理
        try:
            res4 = self.Session.post(API.getPassengerDTOs, headers=headers, data=data)
            return json.loads(res4.text)
        except:
            pass

    @log
    def checkOrderInfo(self):
        headers['Referer'] = API.initDc
        data = {
            '_json_att': '',
            'bed_level_order_num': '000000000000000000000000000000',
            'cancel_flag': '2',
            'oldPassengerStr': '{0},1,{1},1_'.format(self.name,self.IDcard),
            'passengerTicketStr': 'O,0,1,{0},1,{1},{2},N'.format(self.name,self.IDcard,self.tell),
            'randCode': '',
            'REPEAT_SUBMIT_TOKEN': self.RepeatSubmitToken,
            'tour_flag': 'dc',
            'whatsSelect': '1'
        }
        try:
            res6 = self.Session.post(API.checkOrderInfo, headers=headers, data=data)
            return json.loads(res6.text)['data']['submitStatus']
        except:
            pass

    @log
    def getQueueCount(self):
        #获取队列
        headers['Referer'] = API.initDc
        #处理时间
        new_train_date = list(filter(None, str(time.asctime(time.strptime(self.train_date, "%Y-%m-%d"))).split(" ")))

        data = {
            '_json_att': '',
            'fromStationTelecode': self.ticketInfoForPassengerForm['orderRequestDTO']['from_station_telecode'],
            'leftTicket': self.ticketInfoForPassengerForm['leftTicketStr'],
            'purpose_codes': self.ticketInfoForPassengerForm['purpose_codes'],
            'REPEAT_SUBMIT_TOKEN': self.RepeatSubmitToken,
            'seatType': self.seatType,
            'stationTrainCode': self.select_train['车次'],
            'toStationTelecode': self.ticketInfoForPassengerForm['orderRequestDTO']['to_station_telecode'],
            'train_date': '{0} {1} 0{2} {3} 00:00:00 GMT+0800 (中国标准时间)'.format(new_train_date[0],new_train_date[1],new_train_date[2],new_train_date[4]),
            'train_location': self.ticketInfoForPassengerForm['train_location'],
            'train_no': self.ticketInfoForPassengerForm['orderRequestDTO']['train_no']
        }
        try:
            res7 = self.Session.post(API.getQueueCount, headers=headers, data=data)
            print(data)
            print(res7.text)
            return json.loads(res7.text)['status']
        except:
            pass

    @log
    def confirmSingleForQueue(self):
        #提交单人表单
        headers['Referer'] = API.initDc
        data = {
            '_json_att': '',
            'choose_seats': self.choose_seats,
            'dwAll': 'N',
            'key_check_isChange': self.ticketInfoForPassengerForm['key_check_isChange'],
            'leftTicketStr': self.ticketInfoForPassengerForm['leftTicketStr'],
            'oldPassengerStr': '{0},1,{1},1_'.format(self.name,self.IDcard),
            'passengerTicketStr': 'O,0,1,{0},1,{1},{2},N'.format(self.name,self.IDcard,self.tell),
            'purpose_codes': self.ticketInfoForPassengerForm['purpose_codes'],
            'randCode': '',
            'REPEAT_SUBMIT_TOKEN': self.RepeatSubmitToken,
            'roomType': '00',
            'seatDetailType': '000',
            'train_location': self.ticketInfoForPassengerForm['train_location'],
            'whatsSelect': '1'
        }
        res = self.Session.post(API.confirmSingleForQueue,headers = headers,data = data)
        return json.loads(res.text)['data']['submitStatus']

    @log
    def queryOrderWaitTime(self):
        headers['Referer'] = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        while(1):
            random = str(int(round(time.time() * 1000)))
            url = 'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random={}&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN={}'.format(
            random, self.RepeatSubmitToken)
            res = self.Session.post(url,headers = headers)
            res_data = json.loads(res.text)['data']['orderId']
            if res_data:
                print(res_data)
                self.orderId = res_data
                break;
            time.sleep(3)
        return 1

    @log
    def resultOrderForDcQueue(self):
        headers['Referer'] = API.initDc
        data = {
            '_json_att': '',
            'orderSequence_no': self.orderId,
            'REPEAT_SUBMIT_TOKEN': self.RepeatSubmitToken
        }
        try :
            res = self.Session.post(API.resultOrderForDcQueue,headers = headers,data = data)
            return json.loads(res.text)['data']['submitStatus']
        except:
            pass

    @log
    def payOrder(self):
        headers['Referer'] = API.initDc
        random = str(int(round(time.time() * 1000)))
        url = 'https://kyfw.12306.cn/otn//payOrder/init?random={}'.format(random)
        data = {
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN':self.RepeatSubmitToken
        }
        res = self.Session.post(url,headers = headers,data = data)
        return res.text

    @log
    def order(self):
        #下单流程
        #1.检查用户是否在线
        #如果用户在线
        print('1.检查用户是否在线')
        time.sleep(1)
        if self.checkUser():
        #2.订单提交
            print('2.订单提交')
            time.sleep(1)
            if self.leftTicket():
            #3.初始化订单提交页面
                print('3.初始化订单提交页面')
                time.sleep(1)
                self.initDc()
            #4.获取联系人
                print('4.获取联系人')
                time.sleep(1)
                Passenger = self.GetconfirmPassenger()
            #5.获取验证码，可能在人多时启用
                print('5.获取验证码')
                time.sleep(1)
                headers['Referer'] = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
                res5 = self.Session.get(API.getPassCodeNew,headers = headers)
            #6.检查订单信息
                print('6.检查订单信息')
                time.sleep(1)
                if self.checkOrderInfo():
                    #7.获取队列
                    print('7.获取队列')
                    time.sleep(1)
                    if self.getQueueCount():
                        #8.提交单人表单
                        print('8.提交单人表单')
                        time.sleep(1)
                        if self.confirmSingleForQueue():
                            #9.订单查询
                            print('9.订单查询')
                            time.sleep(1)
                            if self.queryOrderWaitTime():
                                #10.结果确认
                                print('10.结果确认')
                                time.sleep(1)
                                if self.resultOrderForDcQueue():
                                    #11.获取支付页面
                                    print('11.获取支付页面')
                                    time.sleep(1)
                                    self.payOrder()






if __name__ == '__main__':
    S = Crawlerkyfw()
    if S.login():
        S.TicketCheck()
        S.order()
        S.loginOut()


