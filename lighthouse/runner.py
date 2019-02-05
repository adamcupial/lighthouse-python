# Python Standard Library
import json
import os
import subprocess
import tempfile

# Own
from report import LighthouseReport


class LighthouseRunner(object):
    def __init__(self, url, form_factor='mobile', quiet=True):
        _, self.__report_path = tempfile.mkstemp(suffix='.json')
        self._run(url, form_factor, quiet)
        self.report = self._get_report()
        self._clean()

    def _run(self, url, form_factor, quiet):
        subprocess.call([
            'lighthouse',
            url,
            '--quiet' if quiet else '',
            '--chrome-flags',
            '"--headless"',
            '--preset',
            'full',
            '--emulated-form-factor',
            form_factor,
            '--output',
            'json',
            '--output-path',
            '{0}'.format(self.__report_path),
        ])

    def _get_report(self):
        try:
            with open(self.__report_path, 'r') as fil:
                return LighthouseReport(json.load(fil))
        except ValueError:
            pass  # @TODO

    def _clean(self):
        os.remove(self.__report_path)
