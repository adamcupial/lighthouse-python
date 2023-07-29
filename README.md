# Lighthouse runner for python

## About This Repository
This repository is based on the original work of [Adam Cupiał](https://github.com/adamcupial) and was forked from his [lighthouse-python](https://github.com/adamcupial/lighthouse-python) repository. While the original repository had not been updated in five years, I found it to be a valuable resource and decided to update it (I have made some changes, fixed some bugs) and turn it into a package for PyPI. I want to acknowledge the original author for creating the foundation of this project and making it available to the community.


## Description
This library is a simple wrapper around lighthouse-cli runner that runs the audit and parses a result in friendly manner.

## Installation
if lighthouse is not installed:
```bash
npm install -g lighthouse
```

```bash
pip install lighthouse-python-plus
```

## Usage

```python
from lighthouse import LighthouseRunner

TIMINGS = [
    'speed-index'
]

report = LighthouseRunner('https://github.com/adamcupial', form_factor='desktop', quiet=False, timings=TIMINGS).report
assert report.score['performance'] > 0.5
print(report.audits(0.5)['performance'].failed)
```

report has 3 properties:

- score: returns dict where keys are categories and values are scores (0 to 1)
- timings: returns dict where keys are timings and values are timedelta objects
- audits: dict where keys are categories and values are objects with passed and failed lists attached

To see all the usage examples of this library, please check out the [demo](demo) folder.

## Dependencies
 - python 3.6+
 - node package lighthouse>=10.3.0 installed

## Changes
[You can find all changes in CHANGELOG!](CHANGELOG.md)
