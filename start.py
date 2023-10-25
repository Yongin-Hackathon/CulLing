import streamlit as st
import pandas as pd
from io import StringIO
from datetime import datetime
import time
from ocr import OCRModule

from summarization import SummarizationModule
from translate import TranslationModule

st.set_page_config(page_title="한국어 요약 번역 도우미", page_icon="🔎", layout="wide")
st.header("안녕하세요😁 한국어 요약 번역 도우미입니다.")
st.write(
    """
한국어에 익숙하지 않은 분들을 위한 각종 공지문 및 안내문 요약 번역 도우미입니다. \n
언어를 선택하세요. \n
"""
)

st.session_state["language_option"] = st.selectbox(
    "🌏 PLEASE SELECT YOUR LANGUAGE / 请选择您的语言",
    ("Language / 语言", "chinese", "vietnam", "english", "japaness", "korean"),
)
st.session_state["type"] = "upload"
language_option = st.session_state["language_option"]
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
    client_id="BGUkDV36W_HjgcitOlDX",
    client_secret="GsCcldWbgX",
    source_lang_type="한국어",
    target_lang_type="영어",
)
# 각 언어별로 선택하면 해당 언어로 보여준다
if language_option == "chinese":
    st.write(
        """
    请上传文件或拍照!         
    """
    )
    menu = ["업로드", "사진찍기", "About"]

    choice = st.sidebar.selectbox("메뉴", menu)

    if choice == "업로드":
        uploaded_file = st.file_uploader("选择文件", type=["png", "jpg", "jpeg"])

        if uploaded_file:
            image_type = uploaded_file.type.split("/")[1]
            st.write(image_type)
            st.image(uploaded_file)
            st.button("번역", type="primary")

    elif choice == "사진찍기":
        picture = st.camera_input("拍照留念")
        if picture:
            st.image(picture)

    # with st.spinner("Wait for it..."):
    #     time.sleep(5)
    # st.success("Done!")

elif language_option == "vietnam":
    st.write(
        """
    Các bạn hãy upload file lên hoặc chụp hình nhé!         
    """
    )

    menu = ["tải lên", "Chụp ảnh", "About"]

    choice = st.sidebar.selectbox("thực đơn", menu)

    if choice == "tải lên":
        uploaded_file = st.file_uploader("chọn một tập tin", type=["png", "jpg", "jpeg"])

        if uploaded_file:
            image_type = uploaded_file.type.split("/")[1]
            st.write(image_type)
            st.image(uploaded_file)
            st.button("sự dịch", type="primary")

    elif choice == "Chụp ảnh":
        picture = st.camera_input("Chụp ảnh")
        if picture:
            st.image(picture)
elif language_option == "english":
    pass
elif language_option == "japaness":
    pass
elif language_option == "korean":
    st.write(
        """
    왼쪽 메뉴에서 방법을 선택해주세요!
    1. 파일을 업로드
    2. 사진을 찍기      
    """
    )
    menu = [
        "눌러서 선택하세요!",
        "업로드",
        "사진찍기",
    ]

    choice = st.sidebar.selectbox("메뉴", menu)

    if choice == "업로드":
        uploaded_file = st.file_uploader("파일을 업로드해주세요.", type=["png", "jpg", "jpeg"])

        if uploaded_file:
            uploaded_image_type = uploaded_file.type.split("/")[1]
            if uploaded_image_type == "jpeg":
                uploaded_image_type = "jpg"
            st.image(uploaded_file)

            if st.button("번역 결과 보기"):
                with st.spinner("Wait for it..."):
                    ocr_result = ocr.ocr(image_file=uploaded_file, image_type=uploaded_image_type)
                    sum_result = sum.summarize(text=ocr_result)
                    translate_result = translate.translate(text=sum_result)
                translate_result = translate_result.replace("\n", " ")
                st.write(translate_result)

    elif choice == "사진찍기":
        camera = st.toggle("사진찍기")
        if camera:
            picture = st.camera_input("사진을 찍어 주세요.")
            if picture:
                picture_type = picture.type.split("/")[1]
                st.image(picture)

                if st.button("번역 결과 보기"):
                    with st.spinner("Wait for it..."):
                        ocr_result = ocr.ocr(image_file=picture, image_type="jpg")
                        sum_result = sum.summarize(text=ocr_result)
                        translate_result = translate.translate(text=sum_result)
                    translate_result = translate_result.replace("\n", " ")
                    st.write(translate_result)
