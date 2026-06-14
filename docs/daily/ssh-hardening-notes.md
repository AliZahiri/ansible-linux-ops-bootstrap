# Add SSH hardening notes

<!-- daily-pr-task: ssh-hardening-notes -->

SSH hardening should be staged carefully so automation access is not accidentally locked out.

Recommended sequence:

- confirm non-root sudo user access
- install and test SSH keys
- restrict password authentication after key access works
- limit SSH networks where possible
- keep a break-glass access path documented

## Portfolio Value

Shows production-safe Linux hardening thinking, not just a checklist.

## Validation

Review the markdown file and confirm it warns against locking out automation.
