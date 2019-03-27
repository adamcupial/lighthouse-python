# this python file uses the following encoding utf-8
from setuptools import setup, find_packages

setup(
    name='lighthouse',
    version='1.0.2',
    description='Lightouse runner',
    author='Adam Cupial',
    author_email='cupial.adam@gmail.com',
    url='n/a',
    packages=find_packages(),
    install_requires=[
        'tqdm>=4.30',
    ]
)
