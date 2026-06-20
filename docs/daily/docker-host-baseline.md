# Document Docker host baseline

<!-- daily-pr-task: docker-host-baseline -->

Docker hosts should have a predictable baseline before application deployment.

Baseline items:

- Docker service enabled and monitored
- compose plugin available
- app deployment user has required permissions
- log rotation is configured
- disk usage is monitored
- container restart policy is documented

## Portfolio Value

Connects Linux bootstrap automation with Docker Compose production workloads.

## Validation

Review the markdown file and confirm it avoids environment-specific secrets.
