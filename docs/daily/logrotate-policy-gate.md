# Add logrotate policy gate

<!-- daily-pr-task: logrotate-policy-gate -->

Linux services need bounded log retention without truncation races or unbounded disk growth. This offline policy gate validates unique absolute log paths, an approved rotation frequency, minimum retention, compression, a bounded size trigger, and exactly one safe reopen strategy: copytruncate or a postrotate reload. It evaluates intended Ansible variables without touching host logs.

## Portfolio Value

Adds deterministic safeguards for log retention, disk pressure, compression, and safe file reopening so bootstrap automation produces operationally complete service logging.

## Validation

Run `python3 -m unittest discover -s tests` and confirm bounded compressed policies with one reopen strategy pass while empty input, duplicate or unsafe paths, invalid frequencies, weak retention, invalid sizes, disabled compression, ambiguous reopen strategies, and invalid policy values fail.
