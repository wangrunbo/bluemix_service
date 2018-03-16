# -*- coding: utf-8 -*-
from .CustomerModel import CustomModel


class CustomLanguageModel(CustomModel):

    def create_model(self, name, base_model, description = ''):
        api = '/v1/customizations'

        data = {
            'name': name,
            'base_model_name': base_model,
            'description': description
        }

        return self._res(api, 'post', json=data)

    def add_words(self, words):
        api = '/v1/customizations/' + self.model_id + '/words'

        return self._res(api, 'post', json={'words': words})

    def modify_word(self, word, modify):
        api = '/v1/customizations/' + self.model_id + '/words/' + word

        return self._res(api, 'put', json=modify)

    def add_corpora(self, name, file, encoding=None):
        api = '/v1/customizations/' + self.model_id + '/corpora/' + name

        text = open(file.decode('utf-8'), 'rb').read()

        if encoding is not None:
            text = unicode(text, encoding).encode('utf-8')

        return self._res(api, 'post', data=text)

    def train(self):
        api = '/v1/customizations/' + self.model_id + '/train'

        return self._res(api, 'post')

    def list_model(self, model_id):
        api = '/v1/customizations/' + model_id

        return self._res(api)

    def list_models(self):
        api = '/v1/customizations'

        return self._res(api)

    def list_corpora(self, name=None):
        api = '/v1/customizations/' + self.model_id + '/corpora'

        if name is not None:
            api += '/' + name

        return self._res(api)

    def list_words(self, options=None):
        api = '/v1/customizations/' + self.model_id + '/words'

        return self._res(api, parameters=options)

    def clear(self):
        api = '/v1/customizations/' + self.model_id + '/reset'

        return self._res(api, 'post')

    def delete_corpora(self, name):
        api = '/v1/customizations/' + self.model_id + '/corpora/' + name

        return self._res(api, 'delete')

    def delete_word(self, name):
        api = '/v1/customizations/' + self.model_id + '/words/' + name

        return self._res(api, 'delete')

    def delete_words(self, name_list):
        result = []
        for name in name_list:
            result.append(self.delete_word(name))

        return result

    def delete(self):
        api = '/v1/customizations/' + self.model_id

        return self._res(api, 'delete')
