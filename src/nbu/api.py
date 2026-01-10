import json
import requests

from .requests_models import Request as RequestModel 

class Client:
    def __init__(self, url, api_client=None):
        self._url = url
        self._api_client = api_client or requests

    def send(self, request_model: RequestModel):
        try:
            response = self._api_client.request(
                method=request_model.method,
                url=f"{self._url}/{request_model.path}",
                params = request_model.get_payload()
            )

            response.raise_for_status()
            data = response.json()
            
            if not data:
                raise ValueError("Empty response data")
                
            return data
        #TODO: create logging and error handling
        except requests.exceptions.JSONDecodeError:
            print(f"Response is not JSON. Status: {response.status_code}")
            print(f"Content-Type: {response.headers.get('Content-Type')}")
            print(f"Response body: {response.text[:500]}")
            #raise ValueError("API returned non-JSON response")
        
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e}")
            #raise 
        
        except Exception as e:
            print(e) 
            #logger.error(f"Error fetching data from {request_model.path}: {e}")
            #raise
