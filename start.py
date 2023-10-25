import streamlit as st
import pandas as pd
from io import StringIO
from datetime import datetime
import time
from ocr import OCRModule

from summarization import SummarizationModule
from translate import TranslationModule

st.set_page_config(page_title="CulLing", page_icon="./image/culling_logo.svg", layout="wide")
st.image("./image/culring.png")
st.header("CulLing (Culture and Linguistic)")
st.write(
    """
**CulLing은 한국어에 익숙하지 않은 분들을 위한 각종 공지문 및 안내문을 요약 후 번역해주는 서비스입니다.** \n
현재 중국어, 일본어, 베트남어를 지원하고 있습니다. \n
"""
)

st.session_state["language_option"] = st.selectbox(
    "🌏 언어를 선택해주세요 / PLEASE SELECT YOUR LANGUAGE / 请选择您的语言",
    ("언어 / Language / 语言", "chinese", "vietnam", "english", "japaness", "korean"),
)

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

# 각 언어별로 선택하면 해당 언어로 보여준다
if language_option == "chinese":
    translate = TranslationModule(
        client_id="BGUkDV36W_HjgcitOlDX",
        client_secret="GsCcldWbgX",
        source_lang_type="한국어",
        target_lang_type="중국어 간체",
    )
    st.write(
        """
    请从左边的菜单中选择方法！
    1. 文件上传
    2. 拍照     
    """
    )
    menu = [
        "点击后选择吧！",
        "文件上传",
        "拍照",
    ]

    choice = st.sidebar.selectbox("菜单", menu)

    if choice == "文件上传":
        uploaded_file = st.file_uploader("请上传文件", type=["png", "jpg", "jpeg"])

        if uploaded_file:
            uploaded_image_type = uploaded_file.type.split("/")[1]
            if uploaded_image_type == "jpeg":
                uploaded_image_type = "jpg"
            st.image(uploaded_file)

            if st.button("显示翻译结果"):
                with st.spinner("请稍等"):
                    ocr_result = ocr.ocr(image_file=uploaded_file, image_type=uploaded_image_type)
                    sum_result = sum.summarize(text=ocr_result)
                    translate_result = translate.translate(text=sum_result)
                translate_result = translate_result.replace("\n", " ")
                st.write(translate_result)

    elif choice == "拍照":
        camera = st.toggle("拍照")
        if camera:
            picture = st.camera_input("请拍张照片，让文件看清楚。")
            if picture:
                picture_type = picture.type.split("/")[1]
                st.image(picture)

                if st.button("显示翻译结果"):
                    with st.spinner("请稍等"):
                        ocr_result = ocr.ocr(image_file=picture, image_type="jpg")
                        sum_result = sum.summarize(text=ocr_result)
                        translate_result = translate.translate(text=sum_result)
                    translate_result = translate_result.replace("\n", " ")
                    st.write(translate_result)
elif language_option == "vietnam":
    translate = TranslationModule(
        client_id="BGUkDV36W_HjgcitOlDX",
        client_secret="GsCcldWbgX",
        source_lang_type="한국어",
        target_lang_type="베트남어",
    )
    st.write(
        """
    Vui lòng chọn phương pháp từ menu bên trái.
    1. tải lên tập tin
    2. chụp ảnh      
    """
    )
    menu = [
        "Các bạn nhấn vào rồi chọn!",
        "tải lên",
        "chụp ảnh ",
    ]

    choice = st.sidebar.selectbox("thực đơn", menu)

    if choice == "tải lên":
        uploaded_file = st.file_uploader("xin vui lòng tải lên một tệp tin", type=["png", "jpg", "jpeg"])

        if uploaded_file:
            uploaded_image_type = uploaded_file.type.split("/")[1]
            if uploaded_image_type == "jpeg":
                uploaded_image_type = "jpg"
            st.image(uploaded_file)

            if st.button("Xem kết quả dịch thuật"):
                with st.spinner("Chờ một chút nhé"):
                    ocr_result = ocr.ocr(image_file=uploaded_file, image_type=uploaded_image_type)
                    sum_result = sum.summarize(text=ocr_result)
                    translate_result = translate.translate(text=sum_result)
                translate_result = translate_result.replace("\n", " ")
                st.write(translate_result)

    elif choice == "chụp ảnh":
        camera = st.toggle("chụp ảnh")
        if camera:
            picture = st.camera_input("Chụp hình cho mình đi")
            if picture:
                picture_type = picture.type.split("/")[1]
                st.image(picture)

                if st.button("Xem kết quả dịch thuật"):
                    with st.spinner("Chờ một chút nhé"):
                        ocr_result = ocr.ocr(image_file=picture, image_type="jpg")
                        sum_result = sum.summarize(text=ocr_result)
                        translate_result = translate.translate(text=sum_result)
                    translate_result = translate_result.replace("\n", " ")
                    st.write(translate_result)
elif language_option == "english":
    translate = TranslationModule(
        client_id="BGUkDV36W_HjgcitOlDX",
        client_secret="GsCcldWbgX",
        source_lang_type="한국어",
        target_lang_type="중국어 간체",
    )
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
elif language_option == "japaness":
    translate = TranslationModule(
        client_id="BGUkDV36W_HjgcitOlDX",
        client_secret="GsCcldWbgX",
        source_lang_type="한국어",
        target_lang_type="일본어",
    )
    st.write(
        """
    左側のメニューから方法をお選びください！
    1. アップロードファイル
    2. 写真を撮ります    
    """
    )
    menu = [
        "押して選択してください！",
        "アップロードする",
        "写真を撮ります",
    ]

    choice = st.sidebar.selectbox("메뉴", menu)

    if choice == "アップロードする":
        uploaded_file = st.file_uploader("ファイルをアップロードしてください", type=["png", "jpg", "jpeg"])

        if uploaded_file:
            uploaded_image_type = uploaded_file.type.split("/")[1]
            if uploaded_image_type == "jpeg":
                uploaded_image_type = "jpg"
            st.image(uploaded_file)

            if st.button("翻訳結果を見ます"):
                with st.spinner("少々お待ちください"):
                    ocr_result = ocr.ocr(image_file=uploaded_file, image_type=uploaded_image_type)
                    sum_result = sum.summarize(text=ocr_result)
                    translate_result = translate.translate(text=sum_result)
                translate_result = translate_result.replace("\n", " ")
                st.write(translate_result)

    elif choice == "写真を撮ります":
        camera = st.toggle("写真を撮ります")
        if camera:
            picture = st.camera_input("写真を撮ってください")
            if picture:
                picture_type = picture.type.split("/")[1]
                st.image(picture)

                if st.button("翻訳結果を見ます"):
                    with st.spinner("少々お待ちください"):
                        ocr_result = ocr.ocr(image_file=picture, image_type="jpg")
                        sum_result = sum.summarize(text=ocr_result)
                        translate_result = translate.translate(text=sum_result)
                    translate_result = translate_result.replace("\n", " ")
                    st.write(translate_result)

elif language_option == "korean":
    translate = TranslationModule(
        client_id="BGUkDV36W_HjgcitOlDX",
        client_secret="GsCcldWbgX",
        source_lang_type="한국어",
        target_lang_type="중국어 간체",
    )
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
