# Python Standard Library
from itertools import product

# Third party modules
from tqdm import tqdm

# Local imports
from .runner import LighthouseRepeatRunner


class BatchRunner(object):
    def __init__(self, urls, form_factors, quiet=True,
                 additional_settings=None, repeats=3):

        if not isinstance(form_factors, (list, )):
            form_factors = list(form_factors)
        if not isinstance(urls, (list, )):
            urls = list(urls)

        all_combinations = tqdm(list(product(urls, form_factors)),
                                desc='Running urls')

        self.reports = []

        for url, factor in all_combinations:
            all_combinations.set_description('{0} | {1}'.format(url, factor))
            report = LighthouseRepeatRunner(url, factor, quiet,
                                            additional_settings,
                                            repeats).report
            self.reports.append((url, factor, report))

