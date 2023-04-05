#!/usr/bin/python3
# -*- coding:utf-8 -*-


from requests.models import Response
from json import JSONDecodeError

# __all__=(' AVMSAnalize')


class AVMSResponce:
    '''
    Класс для работы с ответом AVS Multiscaner
    '''

    def __init__(self, http_resp):

        self._resp = dict()
        #try:
        json_text = http_resp.json()
        if http_resp.status_code == 200:
            self._resp['ok'] = json_text
        else:
            self._resp['error'] = json_text['Description']
       # except JSONDecodeError as json_err:
        #    self._resp['error'] = f"Response is not json format, http status code = {http_resp.status_code}"
        #    err_msg = json_err.msg

    def is_err(self):
        '''
        Проверка на ошибку
        '''
        if self._resp.get('error') is not None:
            return True
        return False

    def get_err(self):
        '''
        Получение текста ошибки
        '''
        return self._resp.get('error')

    def result_is_exist(self):
        '''
        Проверка наличия результата
        '''
        if self._resp.get('ok') is not None:
            return True
        return False

    def get_result(self):
        '''
        Получение результата
        '''
        return self._resp.get('ok')


class AVMSAnalize(AVMSResponce):
    '''
    Класс для работы с ответом AVS Multiscaner
    содержащим результат сканирования
    '''

    def __init__(self, *vargs):
        super().__init__(*vargs)
        pass

    def get_analyze_id(self):
        '''
        получение AnalyzeId
        '''
        result = self.get_result()
        analyze_id = result.get('AnalyzeID')
        return analyze_id


class AVMSSummaryReport(AVMSResponce):
    '''
    Класс для работы с ответом AVS Multiscaner
    содержащим краткий отчет о сканировании файла
    '''

    def __init__(self, *vargs):
        super().__init__(*vargs)

    def get_result(self):
        return super().get_result()


class AVMSFullReport(AVMSResponce):
    '''
    Класс для работы с ответом AVS Multiscaner
    содержащим полный отчет о сканировании файла
    '''

    def __init__(self, *vargs):
        super().__init__(*vargs)

    def get_result(self):
        return super().get_result()


class AVMSProcessingError(AVMSResponce):
    '''
    Класс для работы с сообщением об ошибке взникшей в процессе работы 
    с AVS Multiscaner
    '''

    def __init__(self, err_msg):
        self._resp = dict()
        self._resp['error'] = err_msg
