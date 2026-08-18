# Security Policy

## Reporting a Vulnerability

**DO NOT** open a public GitHub issue to report a security vulnerability.

Security vulnerabilities should be reported responsibly to the project maintainers.

### How to Report

1. Email the project owner with:
   - Vulnerability description
   - Affected components
   - Steps to reproduce (if applicable)
   - Potential impact
   - Suggested mitigation (if any)

2. Include the following in the subject line:
   ```
   [SECURITY] ANSOP Vulnerability Report: [Brief Description]
   ```

3. Allow 7 days for initial response before considering public disclosure.

### Security Scope

This policy applies to:

- Authentication mechanisms
- Authorization and access control
- Data encryption and secrets management
- Input validation and injection vulnerabilities
- API security
- Database security
- Network security
- Audit logging
- Approval workflow enforcement
- Safety controls in response engine

### Out of Scope

- Social engineering (use common sense)
- Physical security
- Third-party library vulnerabilities (report to upstream maintainers)
- Development/test infrastructure
- Theoretical vulnerabilities with no practical impact

## Security by Design

ANSOP is built with security as a primary concern:

### Core Principles

1. **Fail Closed**: Unknown actions default to reject
2. **No Offensive Capability**: Platform cannot attack external systems
3. **Lab Safety**: All responses restricted to explicitly configured lab devices
4. **Transparent**: No opaque security decisions
5. **Auditable**: Complete chain-of-custody for every action
6. **Approval-Enforced**: High-impact actions require human review

### Security Controls

#### Authentication & Authorization

- JWT-based token authentication
- Bcrypt password hashing with salt
- Role-based access control (RBAC) enforced server-side
- Token expiry and refresh mechanisms
- Session timeout

#### Data Security

- Parameterized SQL queries (SQLAlchemy ORM)
- Environment-based secrets management
- No hardcoded credentials
- Encrypted database connections (in production)
- Audit logging of all data access

#### Input Validation

- Pydantic schema validation on all API inputs
- Type checking with MyPy
- Rate limiting on public endpoints
- CORS restrictions
- CSRF token validation

#### Network Security

- TLS/SSL in production
- Secure default ports
- Firewall restrictions
- Lab device allowlists
- Network isolation

#### Response Execution

- Safety validation layer on all responses
- Target authorization checks
- Device registration verification
- Approval workflow enforcement
- Command template validation (no string concatenation)
- Dry-run mode support
- Action logging before execution

#### Audit & Logging

- Immutable-style audit records
- No deletion of audit logs
- Correlation IDs for tracing
- Sensitive data filtering (no passwords, keys, tokens logged)
- Structured logging with JSON
- Timestamp and actor tracking

### Threat Model

#### Attack Scenarios Addressed

| Threat | Mitigation |
|--------|-----------|
| Unauthorized detection submission | JWT authentication + role validation |
| Malicious approval bypass | Server-side approval validation, no client-side "approved" flag |
| Unapproved response execution | Safety layer validates approval before response |
| Response targeting external systems | Target authorization checks against device allowlist |
| SQL injection | SQLAlchemy ORM parameterization |
| Command injection in network commands | Command templates, no untrusted input in shell execution |
| Privilege escalation | RBAC with role-based endpoint enforcement |
| Audit log tampering | Application-level audit records; DB-level constraints |
| Token theft | Short token expiry, refresh tokens, secure storage recommendations |
| Detection spoofing | Event validation, source verification where possible |
| Rate-based DoS | Rate limiting on detection API |

#### Assumptions

- PostgreSQL is secured and access-controlled
- Docker host is not compromised
- Network is isolated from external threats
- JWT signing key is kept secret
- `.env` file with secrets is not committed to Git
- Lab network devices are configured securely
- Administrators follow secure operational practices

---

## Secure Development Practices

### Code Review

- All changes reviewed before merge
- Security implications considered
- Automated testing required
- Manual security testing for sensitive components

### Dependency Management

- Pinned versions in requirements.txt
- Regular dependency updates
- Vendor audit trail for critical libraries
- No unapproved third-party integrations

### Testing

- Unit tests for security-critical functions
- Integration tests for approval workflow
- Manual penetration testing
- Fuzzing of input validation

### Deployment

- Secrets injected at runtime via environment variables
- No test credentials in Docker images
- Database connections use environment secrets
- All services run as non-root users
- Network policies restrict inter-service communication

---

## Compliance Considerations

ANSOP is designed for educational purposes and isolated laboratory environments.

### Applicable Standards

- OWASP Top 10
- CWE/SANS Top 25
- NIST Cybersecurity Framework (core concepts)
- ISO/IEC 27001 (conceptual alignment, not full compliance)

### Not Intended For

- Production security operations
- External threat detection and response
- Compliance-sensitive environments without audit approval
- Attacking or compromising systems outside the laboratory

---

## Incident Response

If a security vulnerability is discovered:

1. **Immediate**: Notify project maintainers privately
2. **Assessment**: Understand impact and scope
3. **Mitigation**: Develop a fix and test it
4. **Notification**: Inform affected users (via advisory)
5. **Release**: Publish patched version
6. **Documentation**: Post-incident review and lessons learned

---

## Contact

For security concerns, contact the project maintainer.

Do not open public issues or discussions about security vulnerabilities.

---

**Last Updated**: 2025-08-18  
**Policy Version**: 1.0
