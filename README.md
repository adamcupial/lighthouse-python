# Lighthouse runner for python

## Description
This library is a simple wrapper around lighthouse-cli runner that runs the audit and parses a result in friendly manner.

## Installation
if lighthouse is not installed:
```bash
npm install -g lighthouse
```

```bash
pip install git+https://github.com/adamcupial/lighthouse-python.git#egg=lighthouse
```

## Usage

```python
from lighthouse import LighthouseRunner

report = LighthouseRunner('https://webdesign-log.pl', form_factor='desktop', quiet=False).report
assert report.score['performance'] > 0.5
print(report.audits['performance'].failed)
```

report has 3 properties:

- score: returns dict where keys are categories and values are scores (0 to 1)
- timings: returns dict where keys are timings and values are timedelta objects
- audits: dict where keys are categories and values are objects with passed and failed lists attached

## Dependencies
 - python 2.7+
 - node package lighthouse installed

## Changes
[You can find all changes in CHANGELOG!](CHANGELOG.md)
