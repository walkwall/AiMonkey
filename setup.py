# -*- coding: utf-8 -*-
__author__ = ''

"""
"""
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='AI_Monkey',
    keywords='',
    version=1.0,
    packages=find_packages(),
    url='',
    license='MIT',
    author='',
    author_email='',
    description='',
    install_requires=[
        'pyyaml', 'Appium-Python-Client', 'selenium', 'termcolor', 'uiautomator', 'click'
    ]
)