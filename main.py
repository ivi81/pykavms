#!/usr/bin/python3
# -*- coding:utf-8 -*- 

from inspect import getsourcefile
from os.path import abspath 
from os.path import join 

from os.path import dirname
from os.path import join 
import sys

from avms import client
from avms import resp
#from avms import AVMSSummaryReport


from  tests.test_cfg import load_config

import logging
import http.client as http_client

def load_test_config():
    current_dir_path_= dirname(abspath(getsourcefile(lambda:0)))
    test_file_path=join(current_dir_path_,"tests_data/48569fc2764a5002cbc2f27895fddcaf.zip_")
    current_dir_path_= dirname(abspath(getsourcefile(lambda:0)))
    config_path=join(current_dir_path_,"tests_data/test_cfg.ini")
    conf=load_config(config_path)
    scan_cfg=conf['multiscaner']
    return scan_cfg,test_file_path

def logger_on():
    http_client.HTTPConnection.debuglevel = 1
    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

if __name__ == '__main__':


    test_cfg, fpath=load_test_config()

    #logger_on()
    
    files=(fpath,"bad/file/path") 
    ms=client.AVMScaner( test_cfg['host'], test_cfg['token']) 

    #Отправляем файлы на проверку
    send_files_result=ms.send_files(files)
    
    #Перебираем результат сканирования
    for k in send_files_result:
        v=send_files_result.get(k)

        #проверяем что ответ положительный (200)
        if v.result_is_exist():

           # Извлекаем идентификатор
           id=v.get_analyze_id()
           print ("analyzeId: "+id+"\n")
           if id is not None:

               #получаем кратуий отчет по файлу
               summary_report=ms.get_summary_report(id) 
               if summary_report.result_is_exist():
                  report=summary_report.get_result()
                  print(report) 
               
               #получаем полный отчет по файлу
               #gg=ms.get_full_report(id)

               pass