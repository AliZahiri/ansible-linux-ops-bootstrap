# Add SSH authentication method contract gate

<!-- daily-pr-task: ssh-authentication-method-contract-gate -->

SSH hardening must preserve an explicit authentication contract after distribution defaults and included files are resolved. This offline gate requires public-key authentication, disables password and keyboard-interactive login, forbids direct root login, and validates the effective AuthenticationMethods expression.

## Portfolio Value

Adds effective-config validation for SSH authentication paths so include ordering or distro defaults cannot silently re-enable passwords or direct root access.

## Validation

Run python3 -m unittest discover -s tests and confirm public-key-only access passes while disabled keys, passwords, keyboard-interactive authentication, direct root login, missing methods, and mixed authentication chains fail.
