# Add MOTD ops banner policy

<!-- daily-pr-task: motd-ops-banner-policy -->

An operations MOTD banner can remind operators which environment they are entering and who owns the host. It should avoid secrets and sensitive topology details.

Banner fields:

- environment name
- owner/team
- support contact
- no secrets

## Portfolio Value

Shows operational hosts expose useful login context without leaking secrets.

## Validation

Run the unit test and confirm banner avoids secrets and includes environment ownership.
