#!/usr/bin/python3
# -*- coding:utf-8 -*-

import unittest

from inspect import getsourcefile
from os.path import abspath 
from os.path import join 
from os.path import basename
from os.path import dirname

import configparser as confp
from avms import AVMultiScaner
from config import cfg


#Test cases to test AVMultiScaner methods
class TestAVMultiScaner(unittest.TestCase):
  #setUp method is overridden from the parent class TestCase
  def setUp(self):
    current_dir_path_= dirname(abspath(getsourcefile(lambda:0)))
    config_path=join(current_dir_path_,"tests/test_cfg.ini")
    conf=cfg.load_config(config_path)

    self.test_file_path=join(current_dir_path_,"./48569fc2764a5002cbc2f27895fddcaf.zip_")

    self.avms = AVMultiScaner(conf['multiscaner'])

  def test_send_file(self):
      r= self.avms.send_file(self.test_file_path)
      print(r)
    #self.assertEqual(self.avms.send_file(self.test_file_path), 1)

'''
  def test_get_summary_report(self):
    self.assertEqual(self.avms.get_summary_report(), 5)

  def test_resend_file(self):
    self.assertEqual(self.avms.resend_file(), 21)

  def test_get_full_report(self):
    self.assertEqual(self.avms.get_summary_report(), 5)

'''

if __name__ == '__main__':
    unittest.main()