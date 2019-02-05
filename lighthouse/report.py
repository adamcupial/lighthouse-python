from datetime import timedelta
from collections import namedtuple

AuditResult = namedtuple('AuditResult', ['title', 'score', 'display'])
AuditCategoryResult = namedtuple('AuditCategoryResult', ['passed', 'failed'])

BASE_TIMINGS = [
    'first-contentful-paint',
    'speed-index',
    'interactive',
    'first-meaningful-paint',
    'first-cpu-idle',
    'estimated-input-latency',
    'time-to-first-byte',
]


class LighthouseReport(object):
    def __init__(self, data, timings=BASE_TIMINGS):
        self.__data = data
        self.__timings = timings

    @property
    def score(self):
        return {
            k: v.get('score', '0')
            for k, v
            in self.__data['categories'].items()
        }

    @property
    def timings(self):
        return {
            k: timedelta(milliseconds=v.get('rawValue'))
            for k, v
            in self.__data['audits'].items()
            if k in self.__timings
        }

    @property
    def audits(self):
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
                    'title': v['title'],
                    'score': v['score'],
                    'display': v.get('displayValue'),
                })
                for k, v in all_audits.items()
                if v.get('score', 0) == 1 and
                v.get('scoreDisplayMode') not in sdm_to_reject
            ]

            failed_audits = [
                AuditResult(**{
                    'title': v['title'],
                    'score': v['score'],
                    'display': v.get('displayValue'),
                })
                for k, v in all_audits.items()
                if v.get('score', 0) < 1 and
                v.get('scoreDisplayMode') not in sdm_to_reject
            ]

            res[category] = AuditCategoryResult(passed_audits, failed_audits)
        return res
