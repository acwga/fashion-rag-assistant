from rag import RagService
import config_data as config
import streamlit as st

# 标题
st.title('服装商品智能客服')
# 分隔符
st.divider()

# 初始化消息列表
if 'message' not in st.session_state:
    st.session_state['message'] = [{'role': 'assistant', 'content': '你好, 有什么可以帮助你?'}]

# 初始化RAG服务
if 'rag' not in st.session_state:
    st.session_state['rag'] = RagService()

# 显示历史消息
for message in st.session_state['message']:
    st.chat_message(message['role']).write(message['content'])

# 用户输入框
prompt = st.chat_input()

if prompt:
    # 在页面输出用户的提问
    st.chat_message('user').write(prompt)
    st.session_state['message'].append({'role': 'user', 'content': prompt})
    # AI客服回复
    ai_res_list = []
    with st.spinner('AI思考中...'):
        res_stream = st.session_state['rag'].chain.stream({'input': prompt}, config.session_config)

        def capture(generator, cache_list):
            """
            该函数用于捕获生成器的输出，并将其存储在缓存列表中，以便后续使用。
            """
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk

        st.chat_message('assistant').write_stream(capture(res_stream, ai_res_list))
        st.session_state['message'].append({'role': 'assistant', 'content': ''.join(ai_res_list)})