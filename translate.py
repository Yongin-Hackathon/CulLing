import os
import sys
from typing import Any, List, Dict, Tuple, Optional
import urllib.request
client_id = "BGUkDV36W_HjgcitOlDX" # 개발자센터에서 발급받은 Client ID 값
client_secret = "GsCcldWbgX" # 개발자센터에서 발급받은 Client Secret 값

class TranslationModule():
    def __init__(self,
                 client_id:str,
                 client_secret:str, 
                 source_lang_type: str, 
                 target_lang_type: str):   
        
        self.lang_code_dict = {
            "한국어" : "ko",
            "영어" : "en",
            "일본어" : "ja",
            "중국어 간체" : "zh-CN",
            "중국어 번체" : "zh-TW",
            "베트남어" : "vi",
            "인도네시아어" : "id",
            "태국어" : "th",
            "독일어" : "de",
            "러시아어" : "ru",
            "스페인어" : "es",
            "이탈리아어" : "it",
            "프랑스어" : "fr"
        }
        
        self.client_id = client_id
        self.client_secret = client_secret
        self.source_lang_code = self.lang_code_dict[source_lang_type]
        self.target_lang_code = self.lang_code_dict[target_lang_type]
        

    def set_client_info(self, client_id:str, client_secret:str):
        self.client_id = client_id
        self.client_secret = client_secret

    
    def translate(self, text: str):
        encText = urllib.parse.quote(text)
        data = f"source={self.source_lang_code}&target={self.target_lang_code}&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)

        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            response_body = response_body.decode('utf-8')
            result = response_body.split('"')[27]

        else:
            print("Error Code:" + rescode)

        return result