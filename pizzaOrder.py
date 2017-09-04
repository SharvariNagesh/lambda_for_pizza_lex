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
    if(event['currentIntent']['slots']): # and event['currentIntent']['slots']['pizzaSize']):
       return event['currentIntent']['slots']['pizzaSize']
    else:
       return None


def getPizzaType(event):
    if(event['currentIntent']['slots']): # and event['currentIntent']['slots']['pizzaType']):
       return event['currentIntent']['slots']['pizzaType']
    else:
       return None

def getPizzaCrust(event):
    if(event['currentIntent']['slots']): # and event['currentIntent']['slots']['pizzaType']):
       return event['currentIntent']['slots']['pizzaCrust']
    else:
       return None

def validateSize(size):
    sizes_available = ['small', 'medium', 'large']
    if  size.lower() not in sizes_available:
        return False

    return True

def orderPizza(size, type, crust):
    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": "Thank you for ordering {} {} {} crust pizza with us." . format(size, type,crust)
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

def elicitCrust(event):
    logger.debug("Inside elicitCrust")
    response = {
        "dialogAction": {
            "type": "ElicitSlot",
            "message": {
                "contentType": "PlainText",
                "content": "What crust would you like?"
            },
            "intentName": "PizzaOrder",
            "slots": {
                "pizzaSize": getPizzaSize(event),
                "pizzaType": getPizzaType(event),
                "pizzaCrust": "None"
            },
            "slotToElicit" : "pizzaCrust"
        }

    }
    return response

def lambda_handler(event, context):
    logger.debug('slots={}'.format(event))
    print ('slots={}'.format(event))
    # response = check_authority(event)
    # if(not response['isValid']):
    #     return error_message(response['message'])

    size = getPizzaSize(event)
    if(size == None):
       return elisitSize(event)

    crust = getPizzaCrust(event)
    if(crust == None):
        logger.debug('No crust information. Sending an elicit request')
        return elicitCrust(event)

    sizeValid = validateSize(size)
    type = getPizzaType(event)
    if(crust !=None):
        return orderPizza(size, type, crust)
    else:
        return elisitSize(event)

    logger.debug("Response = ". format(response))

