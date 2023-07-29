# Standard library modules
from collections import namedtuple
from datetime import timedelta
from typing import Dict, List


AuditResult = namedtuple('AuditResult', ['id','title', 'score', 'display','numval','numunit'])
AuditCategoryResult = namedtuple('AuditCategoryResult', ['passed', 'failed'])

class LighthouseReport:
    """
    Represents a Lighthouse report.

    Provides a more user-friendly interface to the Lighthouse JSON report.
    """

    def __init__(self, data: Dict, timings: List[str] = []):
        """
        Args:
            data (dict): JSON loaded Lighthouse report
            
            timings (list(str), optional): List of timings to gather
                from Lighthouse report. Defaults to an empty list.
        """

        self.__data = data
        self.__timings = timings

    @property
    def score(self) -> Dict[str, float]:
        """
        Dictionary of Lighthouse category names and their corresponding scores (0 to 1).
        """

        return {
            k: v.get('score', 0)
            for k, v
            in self.__data['categories'].items()
        }

    @property
    def timings(self) -> Dict[str, timedelta]:
        """
        Dictionary of Lighthouse timing names and their corresponding times as timedeltas.
        """

        return {
            k: timedelta(milliseconds=v.get('numericValue')) 
            for k, v
            in self.__data['audits'].items()
            if k in self.__timings
        }

    def audits(self, score_thresh: float = 1) -> Dict[str, AuditCategoryResult]:
        """
        Returns a dictionary of Lighthouse audits, grouped by category, with passed/failed
        keys and lists of passed/failed audits attached.

        Args:
            score_thresh (float, optional): The minimum score required for an audit to be considered
                passed. Defaults to 1 (all audits must pass).
        """

        res = {}
        for category, data in self.__data['categories'].items():
            all_audit_refs = [
                x.get('id')
                for x in data['auditRefs']
            ]
            all_audits = {k: self.__data['audits'][k] for k in all_audit_refs}
            sdm_to_reject = ['manual', 'notApplicable', 'informative']
            passed_audits = [
                AuditResult(**{
                    'id': v['id'],
                    'title': v['title'],
                    'score': v['score'],
                    'display': v.get('displayValue'),
                    'numval': v.get('numericValue'),
                    'numunit': v.get('numericUnit'),
                })
                for k, v in all_audits.items()
                if v.get('score',0) is not None and 
                v.get('score', 0) >= score_thresh and
                v.get('scoreDisplayMode') not in sdm_to_reject
            ]

            failed_audits = [
                AuditResult(**{
                    'id': v['id'],
                    'title': v['title'],
                    'score': v['score'],
                    'display': v.get('displayValue'),
                    'numval': v.get('numericValue'),
                    'numunit': v.get('numericUnit'),
                })
                for k, v in all_audits.items()
                if (v.get('score',0) is None or v.get('score', 0) < score_thresh) and
                v.get('scoreDisplayMode') not in sdm_to_reject
            ]

            res[category] = AuditCategoryResult(passed_audits, failed_audits)
        return res
