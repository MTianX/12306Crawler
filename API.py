class API(object):
    # 验证码获取请求API
    captcha_image = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.27051697971861355'
    # 验证码验证请求API
    captcha_check = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
    # 登录页面
    user = 'https://kyfw.12306.cn/otn/login/init'
    # 登录api
    login_url = 'https://kyfw.12306.cn/passport/web/login'
    #uamtk验证
    uamtk = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
    #uamtk客户端
    uamauthclient = 'https://kyfw.12306.cn/otn/uamauthclient'
    #用户界面
    initMy12306 = 'https://kyfw.12306.cn/otn/index/initMy12306'
    #注销
    loginOut = 'https://kyfw.12306.cn/otn/login/loginOut'
    #车票预订界面
    leftTicket_init = 'https://kyfw.12306.cn/otn/leftTicket/init'
    #站台电码
    station_name = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9069'


    #用户在线检查
    checkUser = 'https://kyfw.12306.cn/otn/login/checkUser'

    leftTicket = 'https://kyfw.12306.cn/otn/leftTicket/'
    # 订单提交
    submitOrderRequest = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
    #订单提交页面
    initDc = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'

    #获取队列
    getQueueCount = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'

    #获取联系人
    getPassengerDTOs = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
    #获取订单提交验证码图片
    getPassCodeNew = 'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=passenger&rand=randp&0.8774672370613226'
    #订单信息检查
    checkOrderInfo = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
    #单人表单
    confirmSingleForQueue = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
    #订单提交结果
    resultOrderForDcQueue = 'https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue'






