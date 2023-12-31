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
현재 중국어, 영어, 베트남어, 일본어를 지원하고 있습니다. \n
"""
)

st.session_state["language_option"] = st.selectbox(
    "🌏 언어를 선택해주세요 / PLEASE SELECT YOUR LANGUAGE / 请选择您的语言 / ngôn ngữ / 言語",
    ("언어 / Language / 请选择您的语言 / ngôn ngữ / 语言", "CHINESE", "VIETNAM", "ENGLISH", "JAPANESS"),
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
if language_option == "CHINESE":
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
                    translate_result = translate_result.replace("\n", "  \n ")
                st.subheader("摘要翻译结果！", divider="rainbow")
                st.write(translate_result)

                values = st.slider("你对翻译结果满意吗？ 请打分!", step=1, min_value=0, max_value=10, value=10)
                st.write("渐修:", values)

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
                    st.subheader("摘要翻译结果！", divider="rainbow")
                    st.write(translate_result)

                    values = st.slider("你对翻译结果满意吗？ 请打分!", step=1, min_value=0, max_value=10, value=10)
                    st.write("渐修:", values)
elif language_option == "VIETNAM":
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
                    translate_result = translate_result.replace("\n", "  \n")
                st.subheader("Đây là kết quả dịch tóm tắt!", divider="rainbow")
                st.write(translate_result)
                values = st.slider(
                    "Anh có hài lòng với kết quả dịch không? Hãy cho điểm đi ạ!",
                    step=1,
                    min_value=0,
                    max_value=10,
                    value=10,
                )
                st.write("điểm số:", values)

    elif choice == "chụp ảnh":
        camera = st.toggle("chụp ảnh")
        if camera:
            picture = st.camera_input("Chụp hình cho mình đi")
            if picture:
                picture_type = picture.type.split("/")[1]
                st.image(picture)
                translate_finished = False
                if st.button("Xem kết quả dịch thuật"):
                    with st.spinner("Chờ một chút nhé"):
                        ocr_result = ocr.ocr(image_file=picture, image_type="jpg")
                        sum_result = sum.summarize(text=ocr_result)
                        translate_result = translate.translate(text=sum_result)
                        translate_result = translate_result.replace("\n", "  \n")
                    st.subheader("Đây là kết quả dịch tóm tắt!", divider="rainbow")
                    st.write(translate_result)
                    values = st.slider(
                        "Anh có hài lòng với kết quả dịch không? Hãy cho điểm đi ạ!",
                        step=1,
                        min_value=0,
                        max_value=10,
                        value=10,
                    )
                    st.write("điểm số:", values)
elif language_option == "ENGLISH":
    translate = TranslationModule(
        client_id="BGUkDV36W_HjgcitOlDX",
        client_secret="GsCcldWbgX",
        source_lang_type="한국어",
        target_lang_type="영어",
    )
    st.write(
        """
    Please choose a method from the left menu!
    1. Upload a file
    2. Take a picture    
    """
    )
    menu = [
        "Press to Select a method!",
        "Upload",
        "Take a picture",
    ]

    choice = st.sidebar.selectbox("MENU", menu)

    if choice == "Upload":
        uploaded_file = st.file_uploader("Please upload a file.", type=["png", "jpg", "jpeg"])

        if uploaded_file:
            uploaded_image_type = uploaded_file.type.split("/")[1]
            if uploaded_image_type == "jpeg":
                uploaded_image_type = "jpg"
            st.image(uploaded_file)

            if st.button("Translation Result"):
                with st.spinner("Wait for it..."):
                    ocr_result = ocr.ocr(image_file=uploaded_file, image_type=uploaded_image_type)
                    sum_result = sum.summarize(text=ocr_result)
                    translate_result = translate.translate(text=sum_result)
                    translate_result = translate_result.replace("\n", "  \n")
                st.subheader("Summarization Translation Result!", divider="rainbow")
                st.write(translate_result)
                values = st.slider(
                    "Are you satisfied with result? Please leave your score!",
                    step=1,
                    min_value=0,
                    max_value=10,
                    value=10,
                )
                st.write("Score:", values)

    elif choice == "Take a Picture":
        camera = st.toggle("Take a Picture")
        if camera:
            picture = st.camera_input("Please take a picture so that the contents of the document come out well")
            if picture:
                picture_type = picture.type.split("/")[1]
                st.image(picture)

                if st.button("Translation Result"):
                    with st.spinner("Wait for it..."):
                        ocr_result = ocr.ocr(image_file=picture, image_type="jpg")
                        sum_result = sum.summarize(text=ocr_result)
                        translate_result = translate.translate(text=sum_result)
                        translate_result = translate_result.replace("\n", "  \n")
                    st.subheader("Summarization Translation Result!", divider="rainbow")
                    st.write(translate_result)
                    values = st.slider(
                        "Are you satisfied with result? Please leave your score!",
                        step=1,
                        min_value=0,
                        max_value=10,
                        value=10,
                    )
                    st.write("Score:", values)
elif language_option == "JAPANESS":
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

    choice = st.sidebar.selectbox("メニュー", menu)

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
                    translate_result = translate_result.replace("\n", "  \n")
                st.subheader("要約翻訳の結果です！", divider="rainbow")
                st.write(translate_result)
                values = st.slider("翻訳の結果に満足しましたか？ 点数をつけてください！", step=1, min_value=0, max_value=10, value=10)
                st.write("点数:", values)

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
                        translate_result = translate_result.replace("\n", "  \n")
                    st.subheader("要約翻訳の結果です！", divider="rainbow")
                    st.write(translate_result)
                    values = st.slider("翻訳の結果に満足しましたか？ 点数をつけてください！", step=1, min_value=0, max_value=10, value=10)
                    st.write("点数:", values)

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
                    st.header("번역 결과", divider="rainbow")
                    st.markdown(translate_result)
                    # translate_result = translate_result.replace("\n", " ")
                    # st.write(translate_result)
