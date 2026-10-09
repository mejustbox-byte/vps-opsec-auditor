# Development Environment

Use a clean checkout and the runtime version declared by the project. Install
dependencies using [INSTALL.md](../INSTALL.md), then run the checks listed in
[CONTRIBUTING.md](../CONTRIBUTING.md) and CI.

Keep provider credentials, account exports, and customer data outside the
source tree. Validate provider-specific behavior only in a separate authorized
test account; synthetic fixtures do not establish live provider behavior.
