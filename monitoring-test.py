import requests
import json

# only ger null
null = None

# for local test, use http://127.0.0.1:[ PORTA ]/webhook
# for Cloud Functions test, use endpoint threshold.
webhook_url = 'https://127.0.0.1:5000/webhook'
# https://cloud.google.com/monitoring/support/notification-options#webhooks
dataV1_2 =   {
     "incident": {
       "incident_id": "0.opqiw61fsv7p",
       "resource_id": "11223344",
       "resource_name": "internal-project gke-cluster-1-default-pool-e2df4cbd-dgp3",
       "resource": {
         "type": "gce_instance",
         "labels": {
           "instance_id": "11223344",
           "project_id": "internal-project",
           "zone": "us-central1-c"
         }
       },
       "resource_display_name": "gke-cluster-1-default-pool-e2df4cbd-dgp3",
       "resource_type_display_name": "VM Instance",
       "metric": {
         "type": "compute.googleapis.com/instance/cpu/utilization",
         "displayName": "CPU utilization"
       },
       "policy_name": "Monitor-Project-Cluster",
       "policy_user_labels" : {
           "user-label-1" : "important label",
           "user-label-2" : "another label"
       },
       "condition_name": "VM Instance - CPU utilization [MAX]",
       "condition": {
         "name": "projects/internal-project/alertPolicies/1234567890123456789/conditions/1234567890123456789",
         "displayName": "VM Instance - CPU utilization [MAX]",
         "conditionThreshold": {
           "filter": "metric.type='compute.googleapis.com/instance/cpu/utilization' resource.type='gce_instance' metadata.system_labels.'state'='ACTIVE'",
           "aggregations": [
             {
               "alignmentPeriod": "120s",
               "perSeriesAligner": "ALIGN_MEAN"
             }
           ],
           "comparison": "COMPARISON_GT",
           "thresholdValue": 0.9,
           "duration": "0s",
           "trigger": {
             "count": 1
           }
         }
       },
       "url": "https://console.cloud.google.com/monitoring/alerting/incidents/0.lxfiw61fsv7p?project=internal-project",
       "documentation": {
         "content": "TEST ALERT\n\npolicy.name=projects/internal-project/alertPolicies/1234567890123456789\n\npolicy.display_name=Monitored-Project-NO-GROUPBY\n\ncondition.name=projects/nternal-project/alertPolicies/1234567890123456789/conditions/1234567890123456789\n\ncondition.display_name=VM Instance - CPU utilization [MAX]\n\nproject=internal-project\n\nresrouce.project=internal-project \n\nDONE\n",
         "mime_type": "text/markdown"
       },
       "state": "closed",
       "started_at": 1577840461,
       "ended_at": null,
       "summary": "CPU utilization for internal-project gke-cluster-1-16-default-pool-e2df4cbd-dgp3 with metric labels {instance_name=gke-cluster-1-default-pool-e2df4cbd-dgp3} and system labels {state=ACTIVE} returned to normal with a value of 0.835."
     },
     "version": "1.2"
   }
dataV1_1 = {
    "incident": {
      "incident_id": "f2e08c333dc64cb09f75eaab355393bz",
      "resource_id": "i-4a266a2d",
      "resource_name": "webserver-85",
      "state": "open",
      "started_at": 1385085727,
      "ended_at": null,
      "policy_name": "Webserver Health",
      "condition_name": "CPU usage",
      "errors": [{ "error": { "code": 500, "status": "INTERNAL", "message": "Failed to render as 1.2; downgrading to 1.1."} }],
      "url": "https://console.cloud.google.com/monitoring/alerting/incidents?project=PROJECT_ID",
      "summary": "CPU for webserver-85 is above the threshold of 1% with a value of 28.5%"
    },
    "version": "1.1"
   }
r = requests.post(webhook_url, data=json.dumps(dataV1_2), headers={'Content-Type': 'application/json'})