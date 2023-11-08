from lighthouse import  LighthouseRepeatRunner


url="https://github.com"

TIMINGS = [
    'first-contentful-paint',
    'speed-index',
    'interactive',
]

# settings are as the same as the pagespeed.web.dev
additional_settings = [
"--throttling.cpuSlowdownMultiplier=4",
"--throttling.connectionType=4g",
"--throttling.downloadThroughputKbps=1638.4",
"--throttling.rttMs=150",
"--screenEmulation.disabled=false",
"--screenEmulation.width=412",
"--screenEmulation.height=823",
"--screenEmulation.deviceScaleFactor=1.75",
"--axe.enable=true",
"--axe.version=4.7.0",
]

repeat_runner = LighthouseRepeatRunner(url,"desktop",quiet=False,additional_settings=additional_settings,repeats=2,timings=TIMINGS)

print(repeat_runner.report.score)
print(repeat_runner.report.timings)
