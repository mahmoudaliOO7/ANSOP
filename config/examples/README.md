# Configuration Examples

This directory contains example configurations for testing and demonstration.

## Files

- `example_detection.json` — Sample security detection event
- `example_rule.json` — Sample rule configuration
- `example_incident.json` — Sample incident creation

## Using Examples

### Submitting a Detection

```bash
curl -X POST http://localhost:8000/api/v1/detections \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @example_detection.json
```

### Creating a Rule

```bash
curl -X POST http://localhost:8000/api/v1/rules \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @example_rule.json
```

## Generation Script

To generate random test detections:

```python
python scripts/generate_detection.py \
  --source suricata \
  --severity high \
  --output detection.json
```

## Demo Scenarios

See `docs/demo-scenario.md` for guided demonstration walkthrough.
