from lighthouse import LighthouseRunner


url="https://github.com"

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

runner = LighthouseRunner(url,"mobile",quiet=False,additional_settings=additional_settings)

print(runner.report.score)
print(runner.report.timings)
print(runner.report.audits)

