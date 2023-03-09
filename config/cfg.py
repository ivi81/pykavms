#!/usr/bin/python3
# -*- coding:utf-8 -*-

import configparser as confp
import sys

from inspect import getsourcefile
from os.path import abspath 
from os.path import join 
from os.path import basename
from os.path import dirname

def load_config(path):
    """
    Загружаем конфигурационный файл
    """
    current_dir_path_= dirname(abspath(getsourcefile(lambda:0)))
    path=join(current_dir_path_,path)
    conf=dict()
    dir_path=dirname(path)
    with open(path) as config_file:
        cfg=confp.ConfigParser()
        cfg.read_file(config_file)
        try:
            conf['multiscaner']=dict()
            conf['multiscaner']['host']=cfg.get('multiscaner','host')
            conf['multiscaner']['port']=cfg.get('multiscaner','port')
            conf['multiscaner']['login']=cfg.get('multiscaner','login')
            conf['multiscaner']['passw']=cfg.get('multiscaner','passw')
            conf['multiscaner']['token']=cfg.get('multiscaner','token')
        except  confp.NoOptionError as NoOptErr:
            print("выполнение программы прервано, ошибка в конфигурационном файле: {0}".format(NoOptErr.message))
            sys.exit()
    return(conf)