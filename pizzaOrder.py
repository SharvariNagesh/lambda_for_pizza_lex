import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def error_message(message):
    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": message
            }
        }
    }
    logger.debug("Response = ". format(response))
    return response

def check_authority(event):
    if(event['bot']['name'] != 'pizzaOrderTest'):
      return {
          'isValid' : False,
          'message': "Caller not authorized!",
          'close' : True
      }
    else:
        return {
          'isValid' : True,
        }

def getPizzaSize(event):
    if(event['currentIntent']['slots']):
       return event['currentIntent']['slots']['pizzaSize']

def validateSize(size):
    sizes_available = ['small', 'medium', 'large']
    if  size.lower() not in sizes_available:
        return False

    return True

def orderPizza(size):
    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": "Thank you for ordering {} pizza with us." . format(size)
            }
        }
    }
    logger.debug("Response = ". format(response))
    return response

def elisitSize(event):
    response = {
        "dialogAction": {
            "type": "ElicitSlot",
            "message": {
                "contentType": "PlainText",
                "content": "What size pizza would you like?"
            },
            "intentName": "PizzaOrder",
            "slots": {
              "pizzaSize": "small",
              "pizzaSize": "medium",
              "pizzaSize": "large"
            },
            "slotToElicit" : "pizzaSize"
        }
    }
    return response

def lambda_handler(event, context):
    # This is deployed from the commandline using serverless
    logger.debug('slots={}'.format(event))

    response = check_authority(event)
    if(not response['isValid']):
        return error_message(response['message'])

    size = getPizzaSize(event)
    if(size == None):
       return elisitSize(event)
    sizeValid = validateSize(size)
    if(sizeValid):
        return orderPizza(size)
    else:
        return elisitSize(event)

    logger.debug("Response = ". format(response))

