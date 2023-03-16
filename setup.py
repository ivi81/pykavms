
#!/usr/bin/python3
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages
setup(name='avms',
      version='0.0.1',
      url='https://github.com/the-gigi/conman',
      license='MIT',
      author='Ippolitov Ilya',
      author_email='the.gigi@gmail.com',
      description='Antivirus Multiscaner Client for python3',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False,
      setup_requires=['nose>=1.0'],
      test_suite='nose.collector')