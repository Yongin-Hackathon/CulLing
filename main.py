from ocr import OCRModule
from summarization import SummarizationModule
from translate import TranslationModule

ocr = OCRModule(
    api_url="https://yf7kxqhpn7.apigw.ntruss.com/custom/v1/25735/6ee9c3f252e90aa37c2d440206a2d8b55e1895e8c79609ba703195b2ab0f1b3d/general",
    secret_key="UFVJdnpiWW9RekxCT3lFUVFnUGVrTnFuWG1OaXBFa1Q=",
)


sum = SummarizationModule(
    client_id="bars43g1ig",
    client_secret="wtC9aURbIOLYYq6HVQiuHxkLroJtr4iiwLTmueOv",
    url="https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize",
)

translate = TranslationModule(
    client_id="BGUkDV36W_HjgcitOlDX", client_secret="GsCcldWbgX", source_lang_type="한국어", target_lang_type="영어"
)


ocr_result = ocr.ocr(image_file="./image/감영병예방_가통.jpeg", image_type="jpg")
sum_result = sum.summarize(text=ocr_result)
translate_result = translate.translate(text=sum_result)
translate_result = translate_result.replace("\n", " ")
print(translate_result)
