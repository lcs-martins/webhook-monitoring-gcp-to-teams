from flask import Flask, request, abort
import requests
import json
from copy import deepcopy
from datetime import datetime

# RECEIVE VIA ENV VARS IN CLOUD FUNCTION
WEBHOOK_TEAMS_URL   = 'INCOMING WEBHOOK TEAMS URL'
NOTIFY_LIST         = {
    'Hello My' : 'my@hello.com'
}

app = Flask(__name__)

# MAIN FUNCTION 
@app.route('/webhook', methods=['POST'])
# remove 'self' from params for local test, add 'self' for cloud function env
def webhook():
    if request.method == 'POST':
        gerAdaptiveCard(request.json)
        return 'success', 200
    else:
        abort(400)


def gerAdaptiveCard(data):    
    
    # Get version
    ALERT_VERSION = data['version']
    print ('monitoring json version received: ' + ALERT_VERSION)

    # Open AdaptiveCard template
    # necessary for generation alert messanger
    f =  open('AdaptiveCard.json')
    AdaptiveCard = json.load(f)
    
    # for mentions
    MENTIONS            = NOTIFY_LIST
    MENTIONS_block      = list()

    # ger alert mentions
    MENTIONS_ids = 'Atenção!!! '
    MENTIONS_template = \
                        {
                            "type": "mention",
                            "text": "<at>mention1</at>", 
                            "mentioned": { 
                                "id": "SOUUO A ID lucas.lopes@somagrupo.com.br",
                                "name": "SOU A NAME Lucas Lopes"
                            }
                        }

    for key, value in MENTIONS.items():
        MENTIONS_ids += "| <at>" + key + "</at> "
        
        MENTIONS_template['text'] = "<at>" + key + "</at>"
        MENTIONS_template['mentioned']['id'] = value
        MENTIONS_template['mentioned']['name'] = key
        
        MENTIONS_block.append(deepcopy(MENTIONS_template))

    if ALERT_VERSION == '1.2':
        #
        # VARS CONSTRUCT VERSION 1.2
        #

        # ger alert title
        ALERT_NAME          = \
            "[" + data['incident']['state'].upper() + "]" \
            + " " + data['incident']['metric']['displayName'] \
            + " on " + data['incident']['resource_display_name'] \
            + " in " + data['incident']['resource']['labels']['project_id']

        AdaptiveCard['attachments'][0]['content']['body'][0]['text'] = ALERT_NAME
        
        # ger alert properties
        FACTSET             = \
                        {
                            'Recurso':  data['incident']['resource_display_name'],
                            'Tipo':     data['incident']['resource']['type'],
                            'Projeto':  data['incident']['resource']['labels']['project_id'],
                            'Alerta':   data['incident']['policy_name'],
                            'Métrica':  data['incident']['metric']['displayName'],
                            'Gatilho':  data['incident']['condition']['conditionThreshold']['thresholdValue'],
                            'Duracao':  data['incident']['condition']['conditionThreshold']['duration'],
                            'Início':   datetime.fromtimestamp(data['incident']['started_at']).isoformat(),
                            'Fim':      datetime.fromtimestamp(data['incident']['ended_at']).isoformat() if data['incident']['ended_at'] else 'in progress'
                        }
        FACTSET_list        = list()
        FACTSET_template    = \
                        { 
                            "title": "key:",
                            "value": "value"
                        }
        
        for key, value in FACTSET.items():
            FACTSET_template['title'] = key
            FACTSET_template['value'] = value
            
            FACTSET_list.append(deepcopy(FACTSET_template))

        # ger alert link
        URL_ALERT = data['incident']['url']

    elif ALERT_VERSION == '1.1':
        #
        # VARS CONSTRUCT VERSION 1.1
        #

        # ger alert title
        ALERT_NAME          = \
            "[" + data['incident']['state'].upper() + "]" \
            + " " + data['incident']['condition_name'] \
            + " on " + data['incident']['resource_name'] \
        
        AdaptiveCard['attachments'][0]['content']['body'][0]['text'] = ALERT_NAME

        # ger alert properties
        FACTSET             = \
                        {
                            'Recurso':  data['incident']['resource_name'],
                            'Alerta':   data['incident']['policy_name'],
                            'Métrica':  data['incident']['condition_name'],
                            'Início':   datetime.fromtimestamp(data['incident']['started_at']).isoformat(),
                            'Fim':      datetime.fromtimestamp(data['incident']['ended_at']).isoformat() if data['incident']['ended_at'] else 'in progress'
                        }
        FACTSET_list        = list()
        FACTSET_template    = \
                        { 
                            "title": "key:",
                            "value": "value"
                        }
        
        for key, value in FACTSET.items():
            FACTSET_template['title'] = key
            FACTSET_template['value'] = value
            
            FACTSET_list.append(deepcopy(FACTSET_template))

        # ger alert link
        URL_ALERT = data['incident']['url']

    else:
        print('ERROR: json monitoring version not parameterized. Check Google Monitoring doc for information.')

    #
    # Ger values for AdaptiveCard template
    #

    AdaptiveCard['attachments'][0]['content']['body'][1]['text']        = MENTIONS_ids
    AdaptiveCard['attachments'][0]['content']['msteams']['entities']    = MENTIONS_block
    AdaptiveCard['attachments'][0]['content']['body'][2]['facts']       = FACTSET_list
    AdaptiveCard['attachments'][0]['content']['actions'][0]['url']      = URL_ALERT

    r = requests.post(WEBHOOK_TEAMS_URL, data=json.dumps(AdaptiveCard), headers={'Content-Type': 'application/json'})

if __name__ == '__main__':
    app.run(debug=True)