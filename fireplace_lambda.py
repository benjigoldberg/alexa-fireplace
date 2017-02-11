"""Copy this file into your AWS Lambda Functions, making sure to wire it with
the Alexa Skills Kit. Below, the `FIREPLACE_URL` variable must have the
{{ HOSTNAME }} portion set to your server's URL.
"""

import json
import logging
import urllib2
import uuid

# If you are concerned about speed or costs of logging 
# you should probably set the log level higher than INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

FIREPLACE_URL = "https://{{ HOSTNAME }}/fireplace"


def lambda_handler(event, context):
    """This is the function that is invoked by the AWS function caller.
    Context is unused but passed through anyway. The event variable holds
    all the details pertaining to _why_ this lambda is being invoked as well
    as any necessary details for communicating with the server, like the
    Access Token.
    """
    logger.info('Received Event: {}'.format(json.dumps(event, indent=2)))
    
    if event['header']['name'] == 'DiscoverAppliancesRequest':
        discovered_devices = handle_discovery(event, context)
        logger.info(json.dumps(discovered_devices, indent=2))
        return discovered_devices
    
    if event['header']['namespace'] == 'Alexa.ConnectedHome.Control':
        control_result = handle_control(event, context)
        logger.info(json.dumps(control_result, indent=2))
        return control_result
        
    if event['header']['name'] == 'HealthCheckRequest':
        health_check_result = handle_health_check(event, context)
        logger.info(json.dumps(health_check_result, indent=2))
        return health_check_result

    logger.error('Received unknown request, {}'.format(event['header']['namespace']))
    return None


def _create_header(response_name, namespace):
    """Common functionality for formatting the ASK Response Header"""
    return {
        'messageId': uuid.uuid4().hex,
        'name': response_name,
        'namespace': namespace,
        'payloadVersion': '2'
    }


def handle_health_check(event, context):
    """ASK periodically pings the lambda function to see if the device is 
    healthy. If you want a more accurate health check, connect this to 
    your server and check for a `2XX` response. Here, we simply always acknowledge
    success.
    """
    return {
        'header': _create_header('HealthCheckResponse',
                                 'Alexa.ConnectedHome.System'),
        'payload': {
            "description": "The system is currently healthy",
            "isHealthy": True
        }
    }


def handle_discovery(event, context):
    """When ASK scans for after enabling the skill, return that we have
    one fireplace, supplying a fake appliance ID, manufacturer, etc.
    
    Note that `friendlyName` is how you invoke your fireplace. If you have
    multiple fireplaces, you should modify this to return multiple
    fireplace payloads, each one with a different `applianceId` and `friendlyName`.
    Or, perhaps you'd like multiple names for the same device. In either case, 
    do that here.
    
    Note that the `applianceId` Key should be unique but static for every
    fireplace you want to control in your home. If it changes between discoveries,
    a bunch of bogus "offline" fireplaces will pile up in your device list.
    
    Note that `actions` here are set to `turnOn` and `turnOff`. Depending on how 
    you configured your server and Raspberry Pi, it may be possible that you could add
    more controls here. Perhaps you can set the level of your blower fan by voice command
    for example. "Alexa, set the blower fan to 30%". You would need to specify that in the
    actions below and then add logic to handle that in the `handle_control` function.
    """
    fireplace = {
        'applianceId': 'alexa_fireplace', # This should be unique but static
        'manufacturerName': 'benjigoldberg', # Use your username
        'modelName': 'Alexa Fireplace',
        'version': '1',
        'friendlyName': 'Fireplace',
        'friendlyDescription': 'Living Room Fireplace',
        'isReachable': True,
        'actions': ['turnOn', 'turnOff'],
        'additionalApplianceDetails': {}
    }
    
    return {
        'header': _create_header('DiscoverAppliancesResponse',
                                 'Alexa.ConnectedHome.Discovery'),
        'payload': {
            'discoveredAppliances': [fireplace]   
        }
    }
    
    
def handle_control(event, context):
    """When ASK sends a Turn On or Turn Off request, this function is invoked.
    This method simply pings the server with the appropriate payload
    and access token, and then reports failure or success to ASK.
    
    Note that error handling isn't fully implemented, so Alexa won't be able to
    accurately report failures unless you do so.
    """
    turn_on = event['header']['name'] == 'TurnOnRequest'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer:{}'.format(event['payload']['accessToken'])
    }
    data = {
        'blower_fan': turn_on,
        'flame': turn_on
    }
    http_request = urllib2.Request(FIREPLACE_URL, json.dumps(data), headers)
    try:
        executed_request = urllib2.urlopen(http_request)
        executed_request.close()
    except urllib2.HTTPError as exc:
        logger.error('Failed to POST to Fireplace Server.')
        logger.error('Status Code: {}'.format(exc.code))
        logger.error('Response: {}'.format(exc.read()))

    response_type = 'TurnOnConfirmation' if turn_on else 'TurnOffConfirmation'
    response = {
        'header': _create_header(response_type,
                                 'Alexa.ConnectedHome.Control'),
        'payload': {}  
    }
    return response
