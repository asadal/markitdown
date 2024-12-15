import streamlit as st
import os
import tempfile
from markitdown import MarkItDown

# MarkItDown 초기화
markitdown = MarkItDown()

# 페이지 상태 초기화 함수
def reset_state():
    st.session_state.clear()  # 세션 상태 초기화
    st.rerun()  # 페이지 리로드

# 파일 업로드 후 변환 및 다운로드
def handle_file_upload(uploaded_file):
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        try:
            # 파일을 마크다운으로 변환
            result = markitdown.convert(temp_file_path)
            markdown_content = result.text_content

            # 변환 결과를 세션 상태에 저장
            st.session_state["markdown_content"] = markdown_content
            st.session_state["uploaded_filename"] = uploaded_file.name

        except Exception as e:
            st.error(f"File conversion failed: {e}")
        finally:
            # 임시 파일 삭제
            os.remove(temp_file_path)

# Streamlit UI
st.title("File to Markdown Converter")

# 초기화 버튼
if st.button("초기화"):
    reset_state()

# 파일 업로드 위젯
uploaded_file = st.file_uploader("Upload a file (PDF, PPTX, DOCX, XLSX, JPG)", type=["pdf", "pptx", "docx", "xlsx", "jpg"])

# 파일 업로드 및 처리
if uploaded_file:
    handle_file_upload(uploaded_file)

# 변환된 마크다운 표시 및 다운로드
if "markdown_content" in st.session_state:
    st.text_area("Converted Markdown", st.session_state["markdown_content"], height=300)
    markdown_filename = os.path.splitext(st.session_state["uploaded_filename"])[0] + ".md"
    st.download_button(
        label="Download Markdown File",
        data=st.session_state["markdown_content"],
        file_name=markdown_filename,
        mime="text/markdown"
    )

# 출처 : https://github.com/microsoft/markitdown
