
#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
from setuptools import setup, find_packages
setup(name='avms',
      version=os.getenv('PACKAGE_VERSION','0.0.dev0'),
      url='',
      license='MIT',
      author='Ippolitov Ilya',
      author_email='',
      description='Antivirus Multiscaner Client for python3',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False,
      setup_requires=['nose>=1.0'],
      test_suite='nose.collector')