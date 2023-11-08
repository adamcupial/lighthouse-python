from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

project_urls = {
  'Github': 'https://github.com/sh-alireza/lighthouse-python-plus',
}

setup(
    name='lighthouse_python_plus',
    version='1.2.0',
    description='Lighthouse runner is a Python package that wraps the Lighthouse tool for easy integration into Python projects.',
    author='alireza sharifi',
    author_email='sharifialireza276@gmail.com',
    project_urls=project_urls,
    packages=find_packages(),
    install_requires=[
        'tqdm>=4.30',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
