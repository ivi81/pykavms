#!/usr/bin/python3
# -*- coding:utf-8 -*- 

from http import client
from os.path import basename

import requests
from urllib.parse import urljoin
import sys

if "simplejson" in sys.modules:
    import simplejson as json
else:
    import json


from .resp import AVMSResponce
from .resp import AVMSAnalize
from .resp import AVMSSummaryReport
from .resp import AVMSFullReport
from .resp import AVMSProcessingError

#__all__=('AVMScaner')

def file_open_error_track_(fn):
    """
    Декоратор осуществляющий обработку ошибок подключения
    """
    def file_open_error_wraper (self,*args,**kwargs):

        try:
           return fn(self,*args,**kwargs)
        except FileNotFoundError as e:
          print(e.errno)
          err_msg="неудалось открыть файл"
          print(f"error:{err_msg}"+f": filename = {e.filename}\n")
          return AVMSProcessingError(err_msg)
       

    return file_open_error_wraper

def connection_error_track_(fn):
    """
    Декоратор осуществляющий обработку ошибок подключения
    """
    def http_responce_wraper (self,*args,**kwargs):

        try:
           return fn(self,*args,**kwargs)
        except ConnectionError:
          err_msg="неудалось подключиться к ресурсу."
          print(f"error:{err_msg}")
          return AVMSProcessingError(err_msg)
    return http_responce_wraper

def json_decode_error_track_(fn):
    """
    Декоратор осуществляющий обработку ошибок декодирования json
    """
    def http_responce_wraper (self,*args,**kwargs):

        try:
           return fn(self,*args,**kwargs)
        except json.JSONDecodeError:
            err_msg="получен ответ не в json формате"
            print(f"error:{err_msg}")
            return AVMSProcessingError(err_msg)
             
    return http_responce_wraper

class AVMScaner():

    """
    Класс для работы с api antivirus multiscaner

    Attributes
    ----------
    url : str
        доменное имя на котором находится antivirus multiscaner
    token : str
        ключ доступа который используется для доступа к api
        и пердается в поле Api-key включаемом в заголовок http-запроса к api

    Methods
    -------
    send_file(filePath, exec_env='Win10_x64', exec_time=100, network_conn=False, comment=None)
        Отправляет файл на проверку в antivirus multiscaner

    send_files(filePaths, exec_env='Win10_x64', **kwargs)
        Отправляет несколько файлов (от одного) на проверку в antivirus multiscaner
          
    get_summary_report(analyzeID)
        Запрашивает у antivirus multiscaner краткие отчеты о сканирования
        переданных ранее файлов
    """
    
    def __init__(self, url,token):

        self._token=token
        self._host=url
        self._endpoint=f"https://{self._host}/api/v1/tasks"
        self._header={f"Api-token":self._token}
    
    def send_file(self,filePath,
                  exec_env='Win10_x64',
                  exec_time=100, 
                  network_conn=False,
                  comment=None):
        """
        Метод отправки одного файла на анализ в antivirus multiscaner
         
        Parameters
        ----------
            filePath : str 
              путь в локальной файловой системе к отправляемому файлу

            exec_time : int (optional)
              Время выполнения файла в изолированной среде (в секундах). 
              Может принимать значение от 30 до 500. Значение по умолчанию: 100.

            network_conn : bool (optional)
               Включение или выключение сетевой активности. 
               Может быть True или False по умолчанию False.

            comment : str (optional)
                Комментарий к отправляемому файлу (до 75 любых символов).
        
        Result
        ------ 
            возвращает объект класса avms_resp.AVMSAnalize, 
            в случае возникновения ошибок обработки возвращается 
            объект класса avms_resp.AVMSProcessingError
        """
        return self._send_file(filePath,exec_env,exec_time,network_conn,comment)          

    @file_open_error_track_       
    @connection_error_track_
    @json_decode_error_track_
    def _send_file(self,filePath,
                  exec_env='Win10_x64',
                  exec_time=100, 
                  network_conn=False,
                  comment=None):

        fname=basename(filePath)

        with open(filePath,'rb') as payload:

            params=dict(file_name=fname,exec_env=exec_env ,exec_time=exec_time, allow_network_con=network_conn,comment=comment)           
            resp=requests.post(url=self._endpoint,headers=self._header,data=payload,params=params)
            avms_resp=AVMSAnalize(resp)
                        
            return avms_resp 
            
    def send_files(self,
                  filePaths,
                  exec_env='Win10_x64',
                  **kwargs,
                  ):
        """
        Метод отправки списка файлов (от одного) на анализ.

        Parameters
        ----------
            filePaths : str | list | tuple
              пути к файлам отправляемым на проверку, 
              в случае если отправляется один образец (файл) то может быть строкой.

            exec_env : str | list | tuple, default : Win10_x64 (optional)
              список операционнх систем в среде окружения которых будет произведен анализ образца,
              в случае если отправляется на анализ в одну Ос то название можно передать в качестве строки.
              Значения данной пременной должны быть строго из списка(WinXP, Win7_x64, Win7, Win10_x64), 
              по умолчанию Win10_x64.
                    
            kwargs : словарь необязательных параметров (exec_time, network_conn, comment), см. параметры send_file
        
        Result
        ------ 
            result : dict(filePath = avms_resp.AVMSAnalize| avms_resp.AVMSProcessingError)
              результат является словарем ключи которого являются путями файлов (образцов) перданнх на анализ, а
              значения объектами класса avms_resp.AVMSAnalize, в случае возникновения ошибок обработки значение 
              содержит объектами класса avms_resp.AVMSProcessingError
        """        
        filePaths=chek_for_str(filePaths)
        exec_env=chek_for_str(exec_env)
        result=dict()
        
        for fPath in filePaths:
            for env in exec_env:
                result[fPath]=self._send_file(fPath,env,**kwargs)
        return result
     
    def get_summary_report(self, analyzeID):
        """
        Метод получения краткого отчета об анализе

        Parameters
        ----------
            analyzeID : идетификатор аналза

        Result
        ------ 
            возвращает объект класса avms_resp.AVMSSummaryReport, 
            в случае возникновения ошибок обработки возвращается 
            объект класса avms_resp.AVMSProcessingError

        """
        return self._get_summary_report(analyzeID)
    
    @connection_error_track_
    def _get_summary_report(self, analyzeID):

        url=urljoin(self._endpoint+"/",analyzeID)
        resp=requests.get(url=url,headers=self._header)
        avms_resp=AVMSSummaryReport(resp)
        return avms_resp

    def get_summary_reports(self, ids ):
        """
        Метод получения кратких отчетов об анализе нескольких образцов
        
        Parameters
        ----------
           ids : str | list | tuple
              список идетификаторов отчетов, 
              так же можно передавать один идентификатор ввиде строки
        
        Result
        ------
           result : dict(id = avms_resp.AVMSSummaryReport| avms_resp.AVMSProcessingError)
              результат является словарем ключи которого являются идентификаторами
              полученных отчетов анализа, а значения объектами класса avms_resp.VMSSummaryReport,
              в случае возникновения ошибок обработки значение содержит объектами класса avms_resp.AVMSProcessingError
        """
        ids=chek_for_str(ids)
        result=dict()

        for id in ids:
           result[id]=self._get_summary_report(id)
        return result
   
    @connection_error_track_
    def resend_file(self, analyzeID):
        """
        Повторная отправка файла на анализ
        """
        requests.post(f"https://{self._endpoint}/{analyzeID}",)
    
    @connection_error_track_
    def get_full_report(self, analyzeID):
        """
        Получение полного отчета об анализе
        """
        url=urljoin(self._endpoint+"/",analyzeID)
        resp=requests.get(url=url,headers=self._header)
        avms_resp=AVMSFullReport(resp)
        return avms_resp

   
def chek_for_str(string):
    '''
    Если вдруг передали штучную строку
    то заменяем ее на кортеж
    '''
    if type(string) is str:
        return(string,)
    return string