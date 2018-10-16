
class Configure():

    # 用户名
    USER_NAME = 'xxxxx@163.com'
    # 密码
    USER_PWD = 'xxxxx'

    # 出发站
    FROM_STATION = '海口东'
    # 到达站
    TO_STATION = '三亚'
    # 乘车日期（格式: YYYY-mm-dd）
    TRAIN_DATE = '2018-10-17'

    #购票人姓名
    PASSENGERS_NAME = 'xxxxx'
    # 购票人身份证号
    PASSENGERS_ID = '460xxxxx'
    #购票人电话
    PASSENGERS_TELL = '186xxxxx'
    # 票类型（单程:dc 往返:wc）
    TOUR_FLAG = 'dc'


    # 座位类别（商务座(9),特等座(P),一等座(M),二等座(O),高级软卧(6),软卧(4),硬卧(3),软座(2),硬座(1),无座(1)）
    SEAT_TYPE_CODE = 'O'
    # # 购票人类别（成人票:1,儿童票:2,学生票:3,残军票:4）
    # PASSENGER_TYPE_CODE = '1'
    # 座位选择 A靠窗，B中间，C过道,D过道,F靠窗
    #1A 1B 1C|过道|1D  1F
    #2A 2B 2C|过道|2D  2F
    CHOOSE_SEATS = ['1F']
