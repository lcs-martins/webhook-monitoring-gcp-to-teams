# webhook-monitoring-gcp-to-teams
A webhook in python to convert json data POST from GCP Monitoring to Teams channel, by using Incoming Webhook's Adaptive Cards.

# IN BUILDING :construction::construction_worker:
TODO list
- Auth security layer
- A pipeline to check, validate and test

## ABOUT
This webhook can work with json data from Google Monitoring in versions 1.1 and 1.2, and need update to incremented future new releases versions.

This code is a outline and work without security autenthication, use at your own risk, but you can incremented security layer if want or just wait i'm start that task (:D)

This code use Flask (python libary) and Incoming Webhook's Adaptive Card in your core logic, and is limited by this technologies and your licenses of use.

## HOW USE

##### Requirements
1. Access to GCP and Cloud Shell
2. Have the following permissions on project accounts:
+ Cloud Build service account:
    + [Project No.*]@cloudbuild.gserviceaccount.com**
        + roles/iam.serviceAccountUser (Service Account User)
        + roles/cloudfunctions.developer (Cloud Functions Developer)
        <sub><sup>* Project number is different from project ID.</sup></sub>
        <sub><sup>** This syntax can be changed by google without flagging, the official google documentation in case of problems.</sup></sub>
+ Your google account.
    + so-and-so@xpto.com.br
        + roles/cloudfunctions.developer (Cloud Functions Developer)
3. Activate a Cloud Resource Manager API in the console, [ menu ] > Apis and Services.
4. Create an endpoint (url) for the webhook of the channel you will receive as messages, [ channel ] > [ menu ] > Connectors > search "Incoming Webhook" > Configure what you need > save the url

##### Usage

1. Open the cloud shell (don't forget to select the Function's target project to run cloud shell) and clone this repository.

2. Edit the [.env.yaml](.env.yaml) file and set the required variables.

3. Edit the [cloudbuild.yaml](cloudbuild.yaml) file to change the execution environment of the Function (this includes the Function name).

4. Run it from the cloned root:
```
gcloud builds submit
```
5. Create a webhook notification channel in [GCP Monitoring](https://cloud.google.com/monitoring/support/notification-options#webhooks) and point out the endpoint address of the function. Don't forget to add the channel as policies it should alert.