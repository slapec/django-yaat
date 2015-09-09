# coding: utf-8

from setuptools import setup

vcs_dependencies = [
    # This is not the same django-restify that is listed on PyPI
    'git+https://github.com/lovasb/django-restify.git#egg=django-restify',
    # This is a special fork where order_with_respect_to can be a tuple
    'git+https://github.com/lovasb/django-ordered-model.git#egg=django-ordered-model'
]

setup(
    name='django-yaat',
    version='0.1.0',
    packages=['yaat'],
    install_requires=['Django>=1.8.4', 'django-restify', 'django-ordered-model'],
    dependency_links=vcs_dependencies,
    description='The django-restify resource of the yaat AngularJs module',
    author='Slapec',
    url='https://github.com/slapec/django-yaat',
    license='MIT',
    zip_safe=True,
)
