from lighthouse import BatchRunner


urls = ["https://amazon.com","https://alibaba.com"]
form_factors = ["mobile","desktop"]

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

batch_runner = BatchRunner(urls,form_factors,quiet=False,additional_settings=additional_settings,repeats=2)

print(batch_runner.reports)
