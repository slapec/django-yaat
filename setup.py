# coding: utf-8

from setuptools import setup

setup(
    name='django-yaat',
    version='0.0.1',
    packages=['yaat'],
    description='The django-restify resource of the yaat AngularJs module',
    author='Slapec',
    url='https://github.com/slapec/django-yaat',
    license='MIT',
    zip_safe=True,
    install_requires = ['django-restify'],
)
