# Network Device Configuration

This directory contains configuration for lab network devices that ANSOP can manage.

## Structure

- `nornir_inventory.yaml` — Nornir device inventory (for network automation)
- `devices.yaml` — ANSOP device registry
- `example_devices.yaml` — Example device configurations

## Device Registry Format

```yaml
devices:
  - id: "firewall-lab-01"
    name: "Lab Firewall 01"
    type: "firewall"
    vendor: "paloaltonetworks"
    ip_address: "192.168.1.10"
    port: 22
    username_env: "LAB_DEVICE_USERNAME"
    password_env: "LAB_DEVICE_PASSWORD"
    enabled: true
    features:
      - "block_ip"
      - "unblock_ip"
      - "create_rule"
    tags:
      - "lab"
      - "edge"
```

## Device Types

- `firewall` — Firewall appliance (PaloAlto, Fortinet, etc.)
- `router` — Network router
- `ids` — Intrusion detection system
- `ids_ips` — IDS/IPS hybrid
- `switch` — Network switch
- `proxy` — Web/application proxy
- `simulator` — Simulated device (for testing)

## Safety Considerations

1. **Allowlist Only**: Only devices explicitly configured here can be targeted
2. **Lab-Isolated**: Devices should be in isolated lab networks
3. **Credentials**: Use environment variables for sensitive data
4. **Testing**: Test all response actions in dry-run mode first
5. **Approval**: High-risk actions require human approval

## Using with Nornir

For network automation using Nornir, create `nornir_inventory.yaml`:

```yaml
---
all:
  vars:
    data:
      lab_device: true
  hosts:
    firewall-lab-01:
      hostname: 192.168.1.10
      username: admin
      password: "{{ env('LAB_DEVICE_PASSWORD') }}"
      port: 22
      platform: paloaltonetworks_panos
      groups:
        - firewall
  groups:
    firewall:
      vars:
        nornir_netmiko:
          device_type: paloaltonetworks_panos
```

## Environment Variables

Store credentials as environment variables:

```bash
export LAB_DEVICE_USERNAME=admin
export LAB_DEVICE_PASSWORD=secure_password
```

Never commit credentials to Git.
