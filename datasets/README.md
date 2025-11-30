# Sample Datasets

This directory contains sample datasets for testing the threat hunting query generator.

## Dataset Sources

1. **Kaggle Cybersecurity Datasets**: https://www.kaggle.com/datasets/xwolf12/cyber-security-datasets
2. **CIC Datasets**: https://www.unb.ca/cic/datasets/index.html
3. **Mendeley Data**: https://data.mendeley.com/datasets
4. **Synthetic Data**: Generated security logs and threat events

## Sample Threat Descriptions

These are example natural language descriptions that can be used to test the query generator:

1. "Find all failed login attempts from external IP addresses in the last 24 hours"
2. "Identify suspicious PowerShell activity that may indicate malicious script execution"
3. "Detect unusual data exfiltration patterns from internal hosts to external destinations"
4. "Find evidence of lateral movement through compromised accounts"
5. "Identify potential command and control communication with known malicious domains"
6. "Detect brute force attacks against SSH services"
7. "Find anomalous network traffic patterns that may indicate data exfiltration"
8. "Identify potentially malicious file downloads from suspicious domains"
9. "Detect privilege escalation attempts through unusual process creation"
10. "Find evidence of credential dumping tools like mimikatz in system logs"

## Query Examples

Sample queries for different platforms:

### Splunk SPL

```
index=security sourcetype=windows EventCode=4625 | stats count by user, src_ip | where count > 10
```

### KQL (Microsoft Sentinel)

```
SecurityEvent
| where EventID == 4625
| summarize count() by TargetUserName, IpAddress
| where count_ > 10
```

### Elasticsearch DSL

```json
{
  "query": {
    "bool": {
      "must": [{ "match": { "event.code": "4625" } }],
      "filter": [{ "range": { "@timestamp": { "gte": "now-24h" } } }]
    }
  }
}
```
