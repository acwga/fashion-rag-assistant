"""
基于Streamlit完成web网页上传服务
"""
import streamlit as st
from knowledge_base import KnowledgeBaseService
import time

# 添加网页标题
st.title('知识库更新服务')

# 添加文件上传组件
uploader_file = st.file_uploader(
    label='请添加你要上传的txt文件',
    type=['txt'],
    accept_multiple_files=False
)

# 初始化知识库服务对象，并将其存储在Session State中，以便在不同的交互中保持状态
if 'service' not in st.session_state:
    st.session_state['service'] = KnowledgeBaseService()

# 如果用户上传了文件，显示文件信息
if uploader_file:
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024

    st.subheader(f'文件名: {file_name}')
    st.write(f'文件类型: {file_type}')
    st.write(f'文件大小: {file_size:.2f} KB')

    text = uploader_file.getvalue().decode('utf-8')
    
    # 显示加载动画，并调用知识库服务的upload_by_str方法将文本上传到知识库中
    with st.spinner('载入知识库中...'):
        time.sleep(2)
        result = st.session_state['service'].upload_by_str(text, file_name)
        st.write(result)