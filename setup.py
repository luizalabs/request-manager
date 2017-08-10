import os
from setuptools import setup


def read(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    with open(path) as f:
        return f.read()

setup(
    name='request-manager',
    version='0.0.2',
    description=(
        'Generic HTTP Request'
    ),
    author='LuizaLabs',
    author_email='pypi@luizalabs.com',
    url='https://github.com/luizalabs/request-manager',
    keywords='http requests',
    install_requires=[
        'requests>=2.4.3',
    ],
    packages=['request_manager'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)
