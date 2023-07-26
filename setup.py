from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

project_urls = {
  'Github': 'https://github.com/adamcupial/lighthouse-python',
}

setup(
    name='lighthouse_python',
    version='1.0.3',
    description='Lighthouse runner is a Python package that wraps the Lighthouse tool for easy integration into Python projects.',
    author='Adam Cupial',
    author_email='cupial.adam@gmail.com',
    project_urls=project_urls,
    packages=find_packages(),
    install_requires=[
        'tqdm>=4.30',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
