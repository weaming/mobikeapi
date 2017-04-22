# coding: utf-8
import time
from pprint import pprint
import traceback
import requests


class API(object):
    def __init__(self, mobileNo=''):
        assert mobileNo, 'Give your phone number'
        self.mobileNo = mobileNo
        self.citycode = '0755'
        self.uuid = '62fc9433be988b6d32eed51306fd04b8'
        self.authtoken = '7f5e19162393713911c382983c68fe63'
        self.userid = ''

        self.api = 'https://api.mobike.com/mobike-api'
        self.capi = 'https://capi.mobike.com/mobike-api'
        self.lapi = 'https://lapi.mobike.com/mobike-api'
        self.uapi = 'https://uapi.mobike.com/mobike-api'

        self.top = 22.620226
        self.bottom = 22.456602
        self.left = 113.808199
        self.right = 114.136072
        self.offsetX = 0.02
        self.offsetY = 0.02
        print (self.left - self.right)/self.offsetX
        print (self.top - self.bottom)/self.offsetY

        self.logined = self.uuid and self.authtoken
        self.new_session()

    def new_session(self):
        s = requests.Session()
        s.headers = self.get_http_headers()
        self.s = s

    def get_http_headers(self):
        headers = {
            'Accept-Encoding': 'gzip',
            'platform': '1',
            'mobileNo': self.mobileNo,
            'eption': 'a153f', #TODO
            'time': '%.f' % (time.time() * 1000),
            'lang': 'en',
            'version': '4.2.4',
            'citycode': self.citycode,
            'os': '25',
        }
        if self.logined:
            headers.update({
                'uuid': self.uuid,
                'accesstoken': self.authtoken,
            })
        return headers

    def post(self, url, data=None):
        """post and get json data or return None"""
        resp = self.s.post(url, data)

        try:
            js = resp.json()
        except Exception as e:
            print('%s: %s:\n%r' % (resp.status_code, url, e))
            #print(resp.text)
        else:
            if resp.status_code != 200:
                print(resp.status_code, url)

            if 'message' in js:
                print('message: %s' % js['message'])
            if 'messages' in js:
                print('messages: %s' % js['messages'])

            if 'code' in js:
                print('code: %s' % js['code'])

            return js


    def config(self, location=(None, None)):
        """
        :location: (纬度，经度)
        """
        _api = '/api/config/v1.do'
        api = self.capi + _api
        data = {
            'citycode': self.citycode,
            'version': '100', #TODO
            'latitude': location[0],
            'longitude': location[1],
        }
        return self.post(api, data)

    def nearby_bikes_info(self, biketype=0, location=('', '')):
        """
        biketype:
            0: 所有车型
            1: Mobike
            2: Mobike Lite
        """
        _api = '/rent/nearbyBikesInfo.do'
        api = self.api + _api
        data = {
            'cityCode': self.citycode,
            'biketype': biketype,
            'scope': '500', #TODO
            'userid': self.userid,
            'latitude': location[0],
            'longitude': location[1],
        }
        return self.post(api, data=data)

    def logout(self):
        _api = '/usermgr/logout.do'
        api = self.uapi + _api
        return self.post(api, data={'userid': self.userid})

    def getverifycode(self):
        """1. 发送短信验证码"""
        _api = '/usermgr/getverifycode.do'
        api = self.uapi + _api
        return self.post(api, data={'mobileNo': self.mobileNo})

    def login(self, location=('', ''), captcha=''):
        """
        2. 登录
        :location: 经纬度
        :capcha: 验证码
        返回值：
            code：
                200：验证码错误
                0：登录成功
        """
        _api = '/usermgr/login.do'
        api = self.uapi + _api
        js = self.post(api, data={
            'citycode': self.citycode,
            'mobileNo': self.mobileNo,
            'capt': captcha,
            'latitude': location[0],
            'longitude': location[1],
        })
        if js is not None:
            if js['code'] == 0:
                self.info = info = js['object']
                pprint(info)
                self.authtoken = info['authtoken']
                self.pushkey = info['pushkey'] #TODO
                self.rsacode = info['rsacode'] #TODO
                self.userid = info['userid']
                self.username = info['username'] #TODO

                # new logined session
                self.logined = True
                self.new_session()
        return js

    def getridestate(self):
        """
        example response:
        {u'lastTimes': 0, u'code': 0, u'message': u'', u'object': {u'orderid': u'', 'lastTimes': 0, u'bikeid
        ': u'0755', u'biketype': 0, u'ride': 0, u'longitude': 0.0, u'redpackRidingtime': 10, u'duration': u'
        ', u'second': None, u'cost': u'', u'starttime': None, u'redMoney': 42200, u'active': False, u'latitu
        de': 0.0, u'redBikeFreetime': 120, u'kcal': u''}}
        """
        _api = '/rentmgr/getridestate.do'
        api = self.lapi + _api
        js = self.post(api, data={'userid': self.userid})
        if js and js['code'] == 0:
            self.ride_state = js['object']
            self.ride_state['lastTimes'] = js['lastTimes']
        return js

    def binding_uid(self):
        _api = '/usermgr/bindinguid.do'
        api = self.uapi + _api
        js = self.post(api, data={
            'channel': '1', #TODO
            'userid': self.userid,
            'uuid': self.uuid,
        })
        if js and js['code'] == 0:
            self.obj = js['object'] #TODO
        return js

    def scan_region(self, **kw):
        def frange(start, end, offset=0.1):
            if start > end:
                offset = -abs(offset)
                while start >= end:
                    yield start
                    start += offset
            else:
                offset = abs(offset)
                while start <= end:
                    yield start
                    start += offset

        # custom your region
        for k, v in kw.items():
            if hasattr(self, k):
                setattr(self, k, v)

        for x in frange(self.left, self.right, self.offsetX):
            for y in frange(self.bottom, self.top, self.offsetY):
                location = (y, x)
                yield self.nearby_bikes_info(location=location)
                time.sleep(0.3)
