import requests
import uuid
import time
import json


class OCRModule():
    def __init__(self,
                 api_url: str,
                 secret_key: str) -> None:
        
        self.api_url = api_url
        self.secret_key = secret_key

        self.headers = {
          'X-OCR-SECRET': secret_key
        }

    def set_client_info(self, api_url: str, secret_key: str):
        self.api_url = api_url
        self.secret_key = secret_key

    
    def ocr(self, image_file, image_type) -> str:
        request_json = {
            'images': [
                {
                    'format': f'{image_type}',
                    'name': 'demo'
                }
            ],
            'requestId': str(uuid.uuid4()),
            'version': 'V2',
            'timestamp': int(round(time.time() * 1000))
        }
        payload = {'message': json.dumps(request_json).encode('UTF-8')}
        if isinstance(image_file, str):
            files = [
                ('file', open(image_file,'rb'))
            ]
        else:
            files = [
                ('file', image_file)
            ]

        response = requests.request("POST", self.api_url, headers=self.headers, data = payload, files = files)
        response_json = json.loads(response.text.encode('utf8'))

        text_list = []
        for i in range(len(response_json["images"][0]["fields"])):
            text_list.append(response_json["images"][0]["fields"][i]["inferText"])

        result = ' '.join(text_list)

        return result


        