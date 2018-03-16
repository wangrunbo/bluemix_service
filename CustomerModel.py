# -*- coding: utf-8 -*-
import requests
from const import URL


class CustomModel(object):

    to_dict = True

    def __init__(self, username, password, model_id):
        self.username = username
        self.password = password
        self.model_id = model_id

    def _res(self, api, method='get', parameters=None, **kwargs):
        url = URL + api

        if parameters is not None:
            url += '?'

            if type(parameters) is str:
                url += parameters
            else:
                from urllib import urlencode

                url += urlencode(parameters, doseq=True)

        kwargs['auth'] = (self.username, self.password)

        res = requests.request(method, url, **kwargs)

        return res.json() if self.to_dict else res.content

    def recognition(self, audio, type=None, base_model='ja-JP_BroadbandModel', language_model_id=None, acoustic_model_id=None):
        api = '/v1/recognize'

        parameters = {'model': base_model}
        if language_model_id is not None:
            parameters['customization_id'] = language_model_id
        if acoustic_model_id is not None:
            parameters['acoustic_customization_id'] = acoustic_model_id

        audio = audio.decode('utf-8')

        if type is None:
            import re

            type = re.search(r'.+\.(.+)', audio)

            if type is None:
                raise Exception('File type not specified!')

            type = type.group(1)

        headers = {"Content-Type": "audio/" + type}

        return self._res(api, 'post', parameters=parameters, data=open(audio, 'rb'), headers=headers)
