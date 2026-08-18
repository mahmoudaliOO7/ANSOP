# Security Rules Configuration

This directory contains rule definitions for the ANSOP decision engine.

## Structure

- `example_rules.yaml` — Example rule definitions
- `custom_rules.yaml` — User-defined rules (create as needed)

## Rule Format

Rules are defined in YAML format:

```yaml
version: "1.0"
rules:
  - id: "rule-001"
    name: "Block High-Risk External Connection"
    enabled: true
    priority: 100
    conditions:
      - field: "severity"
        operator: ">="
        value: "high"
      - field: "threat_score"
        operator: ">="
        value: 75
    actions:
      - type: "BLOCK_IP"
        target: "firewall-lab-01"
        requires_approval: true
```

## Rule Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique rule identifier |
| name | string | Human-readable rule name |
| enabled | boolean | Enable/disable rule evaluation |
| priority | integer | Rule evaluation priority (higher = sooner) |
| conditions | array | Conditions to evaluate |
| actions | array | Actions to execute if conditions match |
| description | string | Rule documentation |

## Conditions

Conditions support:

- **Operators**: `==`, `!=`, `<`, `>`, `<=`, `>=`, `in`, `not_in`, `contains`, `not_contains`
- **Fields**: Any detection field (severity, threat_score, source_ip, etc.)
- **Values**: Literals or references (e.g., `allowlist:internal_ips`)

## Actions

Supported actions:

- `BLOCK_IP` — Block source IP
- `UNBLOCK_IP` — Unblock source IP
- `ISOLATE_HOST` — Isolate host from network
- `QUARANTINE_FILE` — Quarantine suspicious file
- `DISABLE_ACCOUNT` — Disable user account
- `ENABLE_LOGGING` — Enable detailed logging
- `CUSTOM` — Custom action (requires integration)

## Loading Rules

Rules are loaded at application startup from this directory. Edit and restart to apply changes, or use the API for runtime rule management.
