import azure.functions as func
import logging
import json 

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="aFunctionApprovalReceiver")
def aFunctionApprovalReceiver(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    body = str(req.get_body())    
  
    try:
    
        body = str(req.get_body())    

        # Treating request body string 
                
        body = body.replace('b"',"").replace("textTravelNumber","\"textTravelNumber\"").replace("textTravelName","\"textTravelName\"").replace("textTravelDescription","\"textTravelDescription\"").replace("textTravelCost","\"textTravelCost\"").replace("textTravelPlace","\"textTravelPlace\"").replace("textTravelDateStart","\"textTravelDateStart\"").replace("textTravelDateEnd","\"textTravelDateEnd\"").replace("comment","\"comment\"").replace(":",":\"").replace(",","\",").replace("}\"","\"}")        
        
        # Parsing to JSON
        
        body_json = json.loads(body)
            
    except ValueError:
    
        pass
    
    else:
    
        textTravelNumber = body_json.get('textTravelNumber').strip() 
        textTravelName = body_json.get('textTravelName').strip()
        textTravelDescription = body_json.get('textTravelDescription').strip()
        textTravelCost = body_json.get('textTravelCost').strip()
        textTravelPlace = body_json.get('textTravelPlace').strip()
        textTravelDateStart = body_json.get('textTravelDateStart').strip()
        textTravelDateEnd = body_json.get('textTravelDateEnd').strip()
        comment = body_json.get('comment').strip()

        # Logging response variables

        logging.info("Travel Request Number : " + textTravelNumber)
        logging.info("Travel Request Name : " + textTravelName)
        logging.info("Travel Request Description : " + textTravelDescription)
        logging.info("Travel Request Costr : " + textTravelCost)
        logging.info("Travel Request Place : " + textTravelPlace)
        logging.info("Travel Request Date Start : " + textTravelDateStart)
        logging.info("Travel Request Date End : " + textTravelDateEnd)
        logging.info("Travel Request Comment : " + comment)
  
      
    return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
    )