# @Author:77
# -*- codeing = utf-8 -*-
# @TIME : 2022/9/27 18:11
# @File : Test_QRcode.py
# @Software: PyCharm
import requests
import time

header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        'Referer': "https://www.nowcoder.com/"
}

s=requests.session()
while True:
    flag = 0
    response = s.get(url='https://www.nowcoder.com', headers=header)
    # print(response.text)
    r = s.get('https://www.nowcoder.com/oauth2/login/wechat_qr_code?_=1663254775727', headers=header)
    # print('二维码已生成！')
    qrcodeurl = r.text.split('l":"')[1]
    qrcodeurl = qrcodeurl.split('","')[0]
    ticket = qrcodeurl.split('showqrcode?')[1]
    f = open("qrcode.txt", "w")
    f.write(ticket)
    f.close()
    # 二维码链接
    qr_url = ("https://mp.weixin.qq.com/cgi-bin/showqrcode?" + ticket)
    print('二维码链接为:' + qr_url)
    re_url = ("https://www.nowcoder.com/oauth2/login/wechat_mp_status" + '?' + ticket)
    while True:
        # print("开始轮询二维码状态")
        r = s.get(url=re_url, headers=header)

        # print(r.text)
        code = r.text.split('"code":')[1]
        code = code.split('}')[0]
        # print(code)
        if code == '2':
            # print('二维码已失效，请重新刷新')
            flag=1
            break
        if code == '1':
            # print('二维码未扫描')
            continue
        if code == '0':
            flag = 1
            print('登陆成功')
            break
        time.sleep(1)
    if flag == 1:
        break
    time.sleep(5)
print("最终获取cookie为:")
print(requests.utils.dict_from_cookiejar(s.cookies))