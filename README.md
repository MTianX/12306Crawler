12306购票小程序
环境：python3.6 PyCharm

1.在Configure.py填入配置信息，运行Crawler.py

2.验证码输入有四种
    1）第三方打码平台
    2）深度学习服务器（百度识图，自建的深度学习服务器）
    3）历遍12306验证码，由md5建立数据库
    4）手动输入
    目前只写了手动输入，抓取的验证码图片为code.jpeg

所需库：
    requests
    json
    re
    time
    codecs
    urllib
    functools
