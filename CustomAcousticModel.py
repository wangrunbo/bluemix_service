# -*- coding: utf-8 -*-
from .CustomerModel import CustomModel

class CustomAcousticModel(CustomModel):

    def create_model(self, name, base_model, description = ''):
        api = '/v1/acoustic_customizations'

        data = {
            'name': name,
            'base_model_name': base_model,
            'description': description
        }

        return self._res(api, 'post', json=data)

    def add_resource(self, name, audio, type=None, parameters=None):
        api = '/v1/acoustic_customizations/' + self.model_id + '/audio/' + name

        audio = audio.decode('utf-8')

        if type is None:
            import re

            type = re.search(r'.+\.(.+)', audio)

            if type is None:
                raise Exception('File type not specified!')

            type = type.group(1)

        headers = {"Content-Type": "audio/" + type}

        return self._res(api, 'post', parameters=parameters, data=open(audio, 'rb'), headers=headers)

    def modify_resource(self, name, audio, type, parameters=None):
        if parameters is None:
            parameters = {}

        parameters['allow_overwrite'] = 'true'

        return self.add_resource(name, audio, type, parameters)

    def train(self, language_model_id=None):
        api = '/v1/acoustic_customizations/' + self.model_id + '/train'

        if language_model_id is None:
            parameters = None
        else:
            parameters = {'custom_language_model_id': language_model_id}

        return self._res(api, 'post', parameters=parameters)

    def check_train_result(self):
        api = '/v1/acoustic_customizations/' + self.model_id

        return self._res(api)

    def list_model(self, model_id):
        api = '/v1/acoustic_customizations/' + model_id

        return self._res(api)

    def list_models(self):
        api = '/v1/acoustic_customizations'

        return self._res(api)

    def list_resources(self, name=None):
        api = '/v1/acoustic_customizations/' + self.model_id + '/audio'

        if name is not None:
            api += '/' + name

        return self._res(api)

    def clear(self):
        api = '/v1/acoustic_customizations/' + self.model_id + '/reset'

        return self._res(api, 'post')

    def delete(self):
        api = '/v1/acoustic_customizations/' + self.model_id

        return self._res(api, 'delete')

    def delete_resource(self, name):
        api = '/v1/acoustic_customizations/' + self.model_id + '/audio/' + name

        return self._res(api, 'delete')
