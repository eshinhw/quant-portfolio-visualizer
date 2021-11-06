import os
import json
import time
from urllib import request

class Auth:
    def __init__(self, user_id, **kwargs):
        print(os.getcwd())

        if os.name == 'nt':
            if os.path.exists('./' + user_id):
                token_path = os.path.expanduser(f'./{user_id}/.questrade.json')
            else:
                os.mkdir(f'./{user_id}')
                token_path = os.path.expanduser(f'./{user_id}/.questrade.json')

        else:
            if os.path.exists('/home/eshinhw/pPortfolioAnalytics/' + user_id):
                token_path = os.path.expanduser(f'/home/eshinhw/pPortfolioAnalytics/{user_id}/.questrade.json')
            else:
                os.mkdir(f'/home/eshinhw/pPortfolioAnalytics/{user_id}')
                token_path = os.path.expanduser(f'/home/eshinhw/pPortfolioAnalytics/{user_id}/.questrade.json')

        # if os.path.exists('./' + user_id):
        #     if os.name == 'nt':
        #         token_path = os.path.expanduser(f'./{user_id}/.questrade.json')
        #     if os.name == 'posix':
        #         token_path = os.path.expanduser(f'/home/eshinhw/qPortfolioAnalytics/{user_id}/.questrade.json')
        # else:
        #     if os.name == 'nt':
        #         os.mkdir(f'./{user_id}')
        #         token_path = os.path.expanduser(f'./{user_id}/.questrade.json')
        #     if os.name == 'posix':
        #         os.mkdir(f'/home/eshinhw/qPortfolioAnalytics/{user_id}')
        #         token_path = os.path.expanduser(f'/home/eshinhw/qPortfolioAnalytics/{user_id}/.questrade.json')


        if 'config' in kwargs:
            self.config = kwargs['config']
        else:
            raise Exception('No config supplied')
        if 'token_path' in kwargs:
            self.token_path = kwargs['token_path']
        else:
            self.token_path = token_path

        if 'refresh_token' in kwargs:
            self.__refresh_token(kwargs['refresh_token'])

    def __read_token(self):
        try:
            with open(self.token_path) as f:
                str = f.read()
                return json.loads(str)
        except IOError:
            raise('No token provided and none found at {}'.format(self.token_path))

    def __write_token(self, token):
        with open(self.token_path, 'w') as f:
            json.dump(token, f)
        os.chmod(self.token_path, 0o600)

    def __refresh_token(self, token):
        req_time = int(time.time())
        r = request.urlopen(self.config['Auth']['RefreshURL'].format(token))
        if r.getcode() == 200:
            token = json.loads(r.read().decode('utf-8'))
            token['expires_at'] = str(req_time + token['expires_in'])
            self.__write_token(token)

    def __get_valid_token(self):
        try:
            self.token_data
        except AttributeError:
            self.token_data = self.__read_token()
        finally:
            if time.time() + 60 < int(self.token_data['expires_at']):
                return self.token_data
            else:
                self.__refresh_token(self.token_data['refresh_token'])
                self.token_data = self.__read_token()
                return self.token_data

    @property
    def token(self):
        return self.__get_valid_token()