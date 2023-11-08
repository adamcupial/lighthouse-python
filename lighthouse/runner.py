# Standard library modules
from collections import namedtuple
from datetime import datetime
from functools import reduce
from itertools import product
import json
import os
import shutil
import subprocess
from typing import List, Union, Dict, Any
from uuid import uuid4

# Third-party modules
from tqdm import tqdm

# Local modules
from .report import LighthouseReport


BASE_TIMINGS = [
    'first-contentful-paint',
    'speed-index',
    'interactive',
    'first-meaningful-paint',
    'first-cpu-idle',
    'estimated-input-latency',
    'time-to-first-byte',
]

class LighthouseRunner:
    """
    Lightweight runner, wraps around lighthouse-cli and parses the result

    Attributes:
        report (LighthouseReport or None): A LighthouseReport object containing the report data, or None if the report 
            could not be loaded.
    """

    def __init__(self, url:str, form_factor:str='mobile', quiet:bool=True,
                 additional_settings:List[str]=[],timings:List[str]=BASE_TIMINGS,
                 output_type:str='none',output_dir:str='./') -> None :
        """ 
        Initialize a new LighthousePerformanceTest object.
        
        Args:
            url (str): The URL to test.
            
            form_factor (str, optional): The form factor to use for the test. Either 'mobile' or 'desktop'.
                Defaults to 'mobile'.
                
            quiet (bool, optional): Whether to suppress output to stdout. Defaults to True.
            
            additional_settings (list, optional): A list of additional parameters to use for the test.
                Defaults to an empty list.
                
            timings (list, optional): A list of performance metrics to measure during the test.
                Defaults to BASE_TIMINGS, which includes several common metrics.
                
            output_type (str, optional): The type of output to generate. Possible values are 'none','both',
                'json', and 'html'. Defaults to 'none'.
                
            output_dir (str, optional): The directory where output files should be written.
                Defaults to the current directory.
        
        Raises:
            AssertionError: If form_factor or output_type are not valid values.
            
        """

        # Check inputs
        assert form_factor in ['mobile', 'desktop'], f"Invalid form_factor: {form_factor}. Allowed values are 'mobile' or 'desktop'."
        assert output_type in ['json','html','both','none'], f"Invalid output_type: {output_type}. Allowed values are 'json', 'html', 'both', or 'none'."
        
        # Generate a unique report name based on the current date and time, plus a random UUID for report path
        self.report_name = str(datetime.now()).replace(" ","_") +"_"+ uuid4().hex
        self.report_path = os.path.join("/tmp",self.report_name)
        
        # Set the timings, output directory, and output type for the test
        self.timings = timings
        self.output_dir = output_dir
        self.output_type = output_type.lower().strip()
        
        # Run the performance test with the given settings and get the report data
        self._run(url, form_factor, quiet, additional_settings)
        self.report = self._get_report()
        
        # Clean up any temporary files
        self._clean()

    def _run(self, url:str, form_factor:str='mobile', quiet:bool=True,
                 additional_settings:List[str]=[]) -> None:
        """
        Run a performance test using the Lighthouse CLI.
        
        Args:
            url (str): The URL to test.
            
            form_factor (str, optional): The form factor to use for the test. Either 'mobile' or 'desktop'.
                Defaults to 'mobile'.
                
            quiet (bool, optional): Whether to suppress output to stdout. Defaults to True.
            
            additional_settings (list, optional): A list of additional parameters to use for the test.
                Defaults to an empty list.

        Raises:
            RuntimeError: If there is an error running the performance test using the Lighthouse CLI, \
            such as a missing or invalid URL, an invalid form factor, a problem with the output path, or an issue with the Lighthouse CLI itself.
            
        """

        try:
            
            # Construct the Lighthouse CLI command
            command = [
                'lighthouse',
                url,
                '--quiet' if quiet else '',
                '--chrome-flags="--headless --no-sandbox"',
                '--preset=perf',
                '--emulated-form-factor={0}'.format(form_factor),
                '--output=json',
                '--output=html',
                '--output-path={0}'.format(self.report_path),
            ]

            # Run the Lighthouse CLI command
            command = command + additional_settings
            subprocess.check_call(' '.join(command), shell=True)
        except subprocess.CalledProcessError as exc:
            # If an error occurs, raise a RuntimeError with a detailed error message
            msg = f"Command '{exc.cmd}' returned an error code: {exc.returncode}, output: {exc.output}"
            raise RuntimeError(msg)

    def _get_report(self) -> Union[LighthouseReport, None]:
        """
        Copy the generated report files to the output directory (if specified) and return a LighthouseReport object 
        containing the report data.

        Returns:
            LighthouseReport or None: A LighthouseReport object containing the report data, or None if the report 
            could not be loaded.
        
        Raises:
            Exception: If there is an error loading the report data from the JSON file.
        """
        
        # Copy the HTML report to the output directory if output_type is 'html' or 'both'
        if self.output_type in ["html","both"]:
            os.makedirs(self.output_dir,exist_ok=True)
            shutil.copy(self.report_path+".report.html", os.path.join(self.output_dir,self.report_name+".html"))
            
        # Copy the JSON report to the output directory if output_type is 'json' or 'both'
        if self.output_type in ["json","both"]:
            os.makedirs(self.output_dir,exist_ok=True)
            shutil.copy(self.report_path+".report.json", os.path.join(self.output_dir,self.report_name+".json"))
            
        # Load the report data from the JSON file and return a LighthouseReport object
        try:
            with open(self.report_path+".report.json", 'r') as fil:
                data = json.load(fil)
                return LighthouseReport(data,self.timings)
        except Exception as e:
            print(f"Error loading report: {e}")
            return None

    def _clean(self) -> None:
        """
        Clean up any temporary files created during the performance test.
        """
        
        # Remove the JSON and HTML report files generated by Lighthouse
        os.remove(self.report_path+".report.json")
        os.remove(self.report_path+".report.html")

class LighthouseRepeatRunner:
    """
    A class for running performance tests using Lighthouse, multiple times and returning 
    an averaged report.

    Attributes:
        report (namedtuple): A named tuple containing the averaged timings and score of the 
            Lighthouse performance test. The named tuple has two fields: 'timings' and 'score'.
            Both fields are dictionaries that map performance metric names to their average 
            value across all test repeats.
    """
    
    def __init__(self, url: str, form_factor: str = 'mobile', quiet: bool = True,
                 additional_settings: List[str] = [], repeats: int = 3, timings:List[str]=BASE_TIMINGS):
        """ 
        Initialize a new LighthouseRepeatRunner object.
        
        Args:
            url (str): The URL to test.
            
            form_factor (str, optional): The form factor to use for the test. Either 'mobile' or 'desktop'.
                Defaults to 'mobile'.
                
            quiet (bool, optional): Whether to suppress output to stdout. Defaults to True.
            
            additional_settings (list of str, optional): A list of additional parameters to use for the test.
                Defaults to an empty list.
                
            repeats (int, optional): The number of times to repeat the Lighthouse performance test. 
                Defaults to 3.
            
            timings (list, optional): A list of performance metrics to measure during the test.
                Defaults to BASE_TIMINGS, which includes several common metrics.
        """
        
        # Initialize an empty list to store the Lighthouse reports from each test repeat
        reports = []
        
        # Use tqdm to display a progress bar while running the test repeats
        progress = tqdm(range(1, repeats + 1), desc='Repeating test')

        # Run the Lighthouse test the specified number of times and store the reports in a list
        for i in progress:
            progress.set_description('Run {0}/{1}'.format(i, repeats))
            reports.append(LighthouseRunner(url, form_factor=form_factor,
                                            quiet=quiet,
                                            additional_settings=additional_settings,timings=timings).report) 

        # Calculate the average values for each performance metric across all test repeats
        report = namedtuple('LighthouseAveragedReport', 'timings, score')
        self.report = report(
            timings=self._get_average([getattr(x, 'timings') for x in reports]),
            score=self._get_average([getattr(x, 'score') for x in reports])
        )

    def _get_average(self, obj_lst: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Computes the average value for each performance metric across all Lighthouse reports.
        
        Args:
            obj_lst (list of dict): A list of dictionaries, where each dictionary contains performance
                metrics for a single Lighthouse report.
        
        Returns:
            dict: A dictionary containing the average value for each performance metric across all reports. 
                The keys of the dictionary are the names of the performance metrics, and the values are the 
                average value of that metric across all reports.
        """
        
        ret = {}
        for key in obj_lst[0].keys():
            lst = [x.get(key) for x in obj_lst]
            ret[key] = reduce(lambda a, b: a + b, lst) / len(lst)
        return ret

class BatchRunner:
    """
    Runs Lighthouse reports for a batch of URLs and form factors.
    """
    
    def __init__(self, urls: List[str], form_factors: List[str], quiet: bool = True,
                 additional_settings: dict = None, repeats: int = 3, timings:List[str]=BASE_TIMINGS):
        """
        Args:
            urls (list(str)): List of URLs to run Lighthouse reports on.
            
            form_factors (list(str)): List of form factors to run Lighthouse reports on.
            
            quiet (bool, optional): Whether to suppress Lighthouse output. Defaults to True.
            
            additional_settings (dict, optional): Additional Lighthouse settings to use for all reports.
                Defaults to None.
                
            repeats (int, optional): Number of times to repeat each report. Defaults to 3.
            
            timings (list, optional): A list of performance metrics to measure during the test.
                Defaults to BASE_TIMINGS, which includes several common metrics.
        """
        
        # Ensure urls and form_factors are lists
        if not isinstance(form_factors, (list, )):
            form_factors = list(form_factors)
        if not isinstance(urls, (list, )):
            urls = list(urls)

        # Iterate over all combinations of urls and form_factors
        all_combinations = tqdm(list(product(urls, form_factors)),
                                desc='Running urls')

        self.reports = []

        for url, factor in all_combinations:
            all_combinations.set_description('{0} | {1}'.format(url, factor))
            
            # Run the Lighthouse report for this combination and append it to reports list
            report = LighthouseRepeatRunner(url, factor, quiet,
                                            additional_settings,
                                            repeats=repeats,timings=timings).report
            self.reports.append((url, factor, report))
