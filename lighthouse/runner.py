# this python file uses the following encoding utf-8

# Python Standard Library
import json
import os
import subprocess
import tempfile

# Own
from report import LighthouseReport


class LighthouseRunner(object):
    """
    Lightweight runner, wraps around lighthouse-cli and parses the result

    Attributes:
        report (LighthouseReport): object with simplified report
    """

    def __init__(self, url, form_factor='mobile', quiet=True,
                 additional_settings=None):
        """
        Args:
            url (str): url to test
            form_factor (str, optional): either mobile or desktop,
                default is mobile
            quiet (bool, optional): should not output anything to stdout,
                default is True
            additional_settings (list, optional): list of additional params
        """

        assert form_factor in ['mobile', 'desktop']

        _, self.__report_path = tempfile.mkstemp(suffix='.json')
        self._run(url, form_factor, quiet, additional_settings)
        self.report = self._get_report()
        self._clean()

    def _run(self, url, form_factor, quiet, additional_settings=None):
        report_path = self.__report_path

        additional_settings = additional_settings or []

        try:
            command = [
                'lighthouse',
                url,
                '--quiet' if quiet else '',
                '--chrome-flags="--headless"',
                '--preset=full',
                '--emulated-form-factor={0}'.format(form_factor),
                '--output=json',
                '--output-path={0}'.format(report_path),
            ]

            command = command + additional_settings
            subprocess.check_call(' '.join(command), shell=True)
        except subprocess.CalledProcessError as exc:
            msg = '''
                Command "{0}"
                returned an error code: {1},
                output: {2}
            '''.format(exc.cmd, exc.returncode, exc.output)
            raise RuntimeError(msg)

    def _get_report(self):
        with open(self.__report_path, 'r') as fil:
            return LighthouseReport(json.load(fil))

    def _clean(self):
        os.remove(self.__report_path)
