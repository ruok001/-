# -*- encoding:utf-8 -*-

import requests
import json
import http.client
import urllib
import datetime
import pandas as pd


class SendMessage():
    def __init__(self):
        self.appID = 'wx76d44eb38e7bad04'
        self.appsecret = '5d9462bef8bdab7cdec771f8f5685b02'
        self.access_token = self.get_access_token()
        self.opend_ids = self.get_openid()

    def get_access_token(self):
        """
        获取微信公众号的access_token值
        """
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.\
            format(self.appID, self.appsecret)
        print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'
        }
        response = requests.get(url, headers=headers).json()
        access_token = response.get('access_token')
        # print(access_token)
        return access_token

    def get_openid(self):
        """
        获取所有粉丝的openid
        """
        next_openid = ''
        url_openid = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s' % (
            self.access_token, next_openid)
        ans = requests.get(url_openid)
        print(ans.content)
        open_ids = json.loads(ans.content)['data']['openid']
        return open_ids

    def sendmsg(self, msg):
        """
        给所有粉丝发送文本消息
        """
        url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={}".format(self.access_token)
        print(url)
        if self.opend_ids != '':
            for open_id in self.opend_ids:
                body = {
                    "touser": open_id,
                    "msgtype": "text",
                    "text":
                    {
                        "content": msg
                    }
                }
                data = bytes(json.dumps(body, ensure_ascii=False).encode('utf-8'))
                print(data)
                response = requests.post(url, data=data)
                # 这里可根据回执code进行判定是否发送成功(也可以根据code根据错误信息)
                result = response.json()
                print(result)
        else:
            print("当前没有用户关注该公众号！")

    def upload_media(self, media_type, media_path):
        """
        上传临时文件到微信服务器，并获取该文件到media_id
        """
        url = 'https://api.weixin.qq.com/cgi-bin/media/upload?access_token={}&type={}'.format(
            self.access_token, media_type)
        print(url)
        meida = {'media': open(media_path, 'rb')}
        rsponse = requests.post(url, files=meida)
        parse_json = json.loads(rsponse.content.decode())
        print(parse_json)
        return parse_json.get('media_id')

    def send_media_to_user(self, media_type, media_path):
        """
        给所有粉丝发送媒体文件，媒体文件以media_id表示
        """
        media_id = self.upload_media(media_type, media_path)
        url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={}'.format(self.access_token)
        if self.opend_ids != '':
            for open_id in self.opend_ids:
                if media_type == "image":
                    body = {
                        "touser": open_id,
                        "msgtype": "image",
                        "image":
                            {
                                "media_id": media_id
                            }
                    }
                if media_type == "voice":
                    body = {
                        "touser": open_id,
                        "msgtype": "voice",
                        "voice":
                            {
                                "media_id": media_id
                            }
                    }
                data = bytes(json.dumps(body, ensure_ascii=False).encode('utf-8'))
                print(data)
                response = requests.post(url, data=data)
                # 这里可根据回执code进行判定是否发送成功(也可以根据code根据错误信息)
                result = response.json()
                print(result)
        else:
            print("当前没有用户关注该公众号！")


if __name__ == "__main__":

    def today_focus_point():
        # 今日热搜
        conn = http.client.HTTPSConnection('api.tianapi.com')  # 接口域名
        params = urllib.parse.urlencode({'key': 'e131803b639c7cd5414fb1ba441bf7a0'})
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        conn.request('POST', '/networkhot/index', params, headers)
        res = conn.getresponse()
        data = res.read().decode(('utf-8'))
        focus_point = pd.read_json(data).newslist
        news = []
        for i in range(5):
            news.append(focus_point[i]['title'])
        return news

    # 天气预报
    rep = requests.get('http://www.tianqiapi.com/api?version=v62&appid=86524544&appsecret=EDDAIA6B&city=仁寿')
    rep.encoding = 'utf-8'
    date = rep.json()['date']
    week = rep.json()['week']
    city = rep.json()['city']
    country = rep.json()['country']
    av_wea = rep.json()['tem']
    low_wea = rep.json()['tem2']
    high_wea = rep.json()['tem1']
    air_level = rep.json()['air_level']
    air_tips = rep.json()['air_tips']

    # 纪念日
    now_date = datetime.datetime.now()
    now_date_str = now_date.strftime('%Y-%m-%d')
    friend_date = datetime.datetime(2010, 8, 1)
    sep1_date = (now_date-friend_date).days
    marry_date = datetime.datetime(2022, 2, 10)
    sep2_date = (now_date-marry_date).days

    def caihongpi():
        # 彩虹屁
        conn = http.client.HTTPSConnection('api.tianapi.com')  # 接口域名
        params = urllib.parse.urlencode({'key': 'e131803b639c7cd5414fb1ba441bf7a0'})
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        conn.request('POST', '/caihongpi/index', params, headers)
        res = conn.getresponse()
        data = res.read().decode(('utf-8'))
        words = pd.read_json(data).newslist
        return words[0]['content']

    hotspot = today_focus_point()
    words = caihongpi()

    information = f'{words}。\n早上好，旭~! \n{now_date_str}，今天是我们恋爱的第{sep1_date}天，距离我们领证' \
                  f'也已经{sep2_date}天了。\n{country}{city}' \
                  f'\n今日平均气温：{av_wea}，最高温：{high_wea}，最低温：{low_wea}。' \
                  f'\n今日空气质量：{air_level}，{air_tips}。' \
                  f'\n今日热搜：\n1、{hotspot[0]}。\n2、{hotspot[1]}。\n3、{hotspot[2]}。' \
                  f'\n4、{hotspot[3]}。\n5、{hotspot[4]}。'

    sends = SendMessage()
    sends.sendmsg(information)
    sends.send_media_to_user("image", './send_information/yyp.jpeg')
