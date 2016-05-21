import json
import random
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen, http, Request
import app.secrets

class VkError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class VkAuth:

    def __init__(self):
        self.token = ''
        self.default_ua = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'

    def get_mocked_user_agent(self):
        try:
            req = Request(url='http://api.useragent.io/')
            response = urlopen(req).read()
            response = json.loads(response.decode('utf-8'))
            return response['ua']
        except:
            try:
                req = Request(url='http://labs.wis.nu/ua/')
                response = urlopen(req).read()
                response = json.loads(response.decode('utf-8'))
                return response['ua']
            except:
                return self.default_ua

    def call_api(self, method, params):

        if isinstance(params, list):
            params_list = params[:]
        elif isinstance(params, dict):
            params_list = params.items()
        else:
            params_list = [params]
        params_list += [('access_token', self.token)]
        url = 'https://api.vk.com/method/%s?%s' % (method, urlencode(params_list))
        try:
            req = Request(url=url, headers={'User-agent': random.choice(self.get_mocked_user_agent())})
            response = urlopen(req).read()
            result = json.loads(response.decode('utf-8'))
            try:
                if 'response' in result.keys():
                    return result['response']
                else:
                    raise VkError('no response on answer: ' + result['error']['error_msg'].__str__())
            except VkError as err_:
                print(err_.value)
        except URLError as err_:
            print('URLError: ' + err_.errno.__str__() + ", " + err_.reason.__str__())
        except http.client.BadStatusLine as err_:
            print("".join(['ERROR Vk.call_api', err_.__str__()]))
        except ConnectionResetError as err_:
            print("".join(['ERROR ConnectionResetError', err_.__str__()]))
        except ConnectionAbortedError as err_:
            print("".join(['ERROR ConnectionAbortedError', err_.__str__()]))
        return list()

    def get_username_and_email(self):
        vk_auth_page = 'http://localhost/vk_auth'
        req_url = 'https://oauth.vk.com/authorize?client_id=' + app.secrets.vk_client_id + \
                  '&scope=status&redirect_uri=' + vk_auth_page + \
                  '&response_type=code&v=5.52'
        req = Request(url=req_url)
        response = urlopen(req).read()
        a = 5
