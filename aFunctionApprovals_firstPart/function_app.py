import requests
import json
import pandas as pd
#import pyodbc
import datetime
import logging
import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="aFunctionApprovals")
def aFunctionApprovals(req: func.HttpRequest) -> func.HttpResponse:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()


    def graph_auth ():

        # Graph Authentication details
        # ----------------------------
    
        app_id = '92ee2d9c-3f39-4c07-90d3-8d96445ad818'  # Application Id - on the azure app overview page
        client_secret = 'mrv8Q~mhLP5p5Qbl2YKIHKqEp.Qcxaw1C1_Ppcq6'  # SecretValue Id
        tenantId = 'e9112c5c-e4bb-4ab9-8b4c-3692f43531a7'  # Tenant Id of Azure Suscription

        # Use the redirect URL to create a token url
        token_url = 'https://login.microsoftonline.com/' + tenantId + '/oauth2/token'

        token_data = {
            'grant_type': 'client_credentials',
            'client_id': app_id,
            'client_secret': client_secret,
            'resource': 'https://graph.microsoft.com',
            'scope': 'https://graph.microsoft.com'
        }

        token_r = requests.post(token_url, data=token_data)
        token = token_r.json().get('access_token')

        return token


    def getUserId (token,travelApproverUserPrincipalName) : 

        # Use the token using microsoft graph endpoints
        user_url = 'https://graph.microsoft.com/v1.0/users/' + travelApproverUserPrincipalName

        headers = {
            'Authorization': 'Bearer {}'.format(token)
        }

        user_response_data = json.loads(requests.get(user_url, headers=headers).text)
        logging.info(user_response_data) 
        userId = user_response_data['id']

        return userId

    
    def sendMail(adaptative_card_json): 
    
        # Outlook graph call
        # ---------------------

        # Configurar la URL y las cabeceras para enviar el correo
        
        outlook_url = 'https://graph.microsoft.com/v1.0/users/' + sendMailUserId + '/sendMail'
        headers = {
            'Content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(token)
        }

    
        # Cuerpo del mensaje

        body_message = {
            "message": {
                "subject": "Formulario con Adaptive Card",
                "body": {
                    "contentType": "HTML",
                    "content":
                    "<html>" +
                    "<head>" +
                        "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=us-ascii\">" +
                    "<script type=\"application/adaptivecard+json\">" +
                        adaptative_card_json   +
                        "</script>" +
                        "</head>" +
                        "<body>" +
                        " " +
                        "</body>" +
                        "</html>"

                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": travelApproverUserPrincipalName
                        }
                    }
                ]
            }
        }


        # Send email
        response = requests.post(outlook_url, headers=headers, json=body_message)
        

        return response


    logging.info('Initializing Approval Flow....')  
    

    try:
        req_body = req.get_json()
    
    except ValueError:
    
        pass
    
    else:
        
        
        travelNumber = req_body.get('travelNumber')
        travelNumberName = req_body.get('travelName')
        travelDescription = req_body.get('travelDescription')
        travelCost =  req_body.get('travelCost')
        travelPlace = req_body.get('travelPlace')
        travelStarts = req_body.get('travelStarts')
        travelEnds = req_body.get('travelEnds')
        travelComments = req_body.get('travelComments')
        travelApproverUserPrincipalName = req_body.get('travelApproverUserPrincipalName')

        
        # Graph authentication 

        token = graph_auth ()
        logging.info("function authenticathed throw graph")

        # Get approverUserPrincipalName Id    
        
        sendMailUserId = getUserId (token,travelApproverUserPrincipalName)  
        

        # Manager Graph call manager details
        # ----------------------------
        '''
        manager_url = 'https://graph.microsoft.com/v1.0/contacts/' + travelApproverUserPrincipalName + '/manager'

        headers = {
            'Authorization': 'Bearer {}'.format(token)
        }

        manager_response_data = json.loads(requests.get(manager_url, headers=headers).text)
        '''


        # Compose adaptative card JSON as body approval email
        # ---------------------------------------------------

        adaptative_card_json = """
                            {
                                    "type": "AdaptiveCard",
                                    "body": [
                                        {
                                            "type": "TextBlock",
                                            "size": "Medium",
                                            "weight": "Bolder",
                                            "text": "International Travel Request Review"
                                        },
                                        {
                                            "type": "ColumnSet",
                                            "columns": [
                                                {
                                                    "type": "Column",
                                                    "items": [
                                                        {
                                                            "type": "Image",
                                                            "style": "Person",
                                                            "url": "https://cdn.vectorstock.com/i/1000x1000/31/54/bot-sign-design-robot-logo-template-modern-flat-vector-27973154.webp",
                                                            "altText": "Cloud Automation Robot",
                                                            "size": "Small"
                                                        }
                                                    ],
                                                    "width": "auto"
                                                },
                                                {
                                                    "type": "Column",
                                                    "items": [
                                                        {
                                                            "type": "TextBlock",
                                                            "weight": "Bolder",
                                                            "text": "Cloud Automation Team",
                                                            "wrap": true
                                                        },
                                                        {
                                                            "type": "TextBlock",
                                                            "spacing": "None",
                                                            "text": "Created {NowDateTime}",
                                                            "isSubtle": true,
                                                            "wrap": true
                                                        }
                                                    ],
                                                    "width": "stretch"
                                                }
                                            ]
                                        },  
                                        {
                                            "type": "TextBlock",
                                            "text": "The automation cloud system detected failures in the following travel request order. Please review the details below and reject o resend to the system : ",
                                            "wrap": true
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": "Travel Request Number",
                                            "wrap": true
                                        },
                                        {
                                            "type": "Input.Text",
                                            "id": "textTravelNumber",
                                            "placeholder": "",
                                            "value": "{TextTravelNumberValue}"
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": "Travel Request Name",
                                            "wrap": true
                                        },
                                        {
                                            "type": "Input.Text",
                                            "id": "textTravelName",
                                            "placeholder": "",
                                            "value": "{TextTravelNumberName}"
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": "Travel Request Description",
                                            "wrap": true
                                        },
                                        {
                                            "type": "Input.Text",
                                            "id": "textTravelDescription",
                                            "placeholder": "",
                                            "value": "{TextTravelDescriptionValue}"
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": "Travel Request Cost",
                                            "wrap": true
                                        },
                                        {
                                            "type": "Input.Text",
                                            "id": "textTravelCost",
                                            "placeholder": "",
                                            "value": "{TextTravelNumberCost}"
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": "Travel Request Place",
                                            "wrap": true
                                        },
                                        {
                                            "type": "Input.Text",
                                            "id": "textTravelPlace",
                                            "placeholder": "",
                                            "value": "{TextTravelPlaceValue}"
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": "Travel Date Starts",
                                            "wrap": true
                                        },
                                        {
                                            "type": "Input.Date",
                                            "id": "textTravelDateStart",
                                            "value": "{DateTravelStarts}"
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": "Travel Date Ends",
                                            "wrap": true
                                        },
                                        {
                                            "type": "Input.Date",
                                            "id": "textTravelDateEnd",
                                            "value": "{DateTravelEnds}"
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": "Comments",
                                            "wrap": true
                                        },
                                        {
                                            "type": "Input.Text",
                                            "id": "textTravelComments",
                                            "placeholder": "",
                                            "value": "{TextTravelCommentsValue}",
                                            "isMultiline": true
                                        }
                                    ],
                                                "actions": [
                                            {
                                                "type": "Action.Http",
                                                "id": "accept",
                                                "title": "Accept",
                                                "method": "POST",
                                                "url": "https://afunctionapprovalreceiver.azurewebsites.net/api/aFunctionApprovalReceiver?",  
                                                "body": "{textTravelNumber: {{textTravelNumber.value}}, textTravelName: {{textTravelName.value}}, textTravelDescription: {{textTravelDescription.value}} , textTravelCost: {{textTravelCost.value}} , textTravelPlace: {{textTravelPlace.value}}, textTravelDateStart: {{textTravelDateStart.value}} , textTravelDateEnd: {{textTravelDateEnd.value}} , comment: {{textTravelComments.value}}}",
                                                "headers": [

                                                            {
                                                                "name": "Content-type",
                                                                "value": "application/json"
                                                            }
                                                        ]
                                            }
                                        ]

                                    ,
                                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                                    "version": "1.0"
                                }
                            """    
        
        # Dynamic variables


        adaptative_card_json = adaptative_card_json.replace('{NowDateTime}', utc_timestamp.split('T')[0])
        adaptative_card_json = adaptative_card_json.replace('{TextTravelNumberValue}', travelNumber)
        adaptative_card_json = adaptative_card_json.replace('{TextTravelNumberName}', travelNumberName)
        adaptative_card_json = adaptative_card_json.replace('{TextTravelDescriptionValue}', travelDescription)
        adaptative_card_json = adaptative_card_json.replace('{TextTravelNumberCost}', travelCost)
        adaptative_card_json = adaptative_card_json.replace('{TextTravelPlaceValue}', travelPlace)
        adaptative_card_json = adaptative_card_json.replace('{DateTravelStarts}', travelStarts)
        adaptative_card_json = adaptative_card_json.replace('{DateTravelEnds}', travelEnds)
        adaptative_card_json = adaptative_card_json.replace('{TextTravelCommentsValue}', travelComments)


        email_response = sendMail(adaptative_card_json)
        
        # Verify answer

        if email_response.status_code == 202:
            logging.info('Email sent successfully.')
        else:
            logging.info(f'Error sending email: {email_response.status_code}')
            logging.info(email_response.json())


    return func.HttpResponse( 'First part of the approval flow request finished sucessfully', status_code=200 )
