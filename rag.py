from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from file_history_store import get_history

class RagService():
    def __init__(self):

        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name)
        )

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ('system', '以我提供的参考资料为主, 简洁和专业的回答用户问题, 参考资料: {context}'),
                ('system', '并且我提供用户的对话历史记录, 如下:'),
                MessagesPlaceholder('history'),
                ('user', '请回答用户的提问: {input}')
            ]
        )

        self.chat_model = ChatTongyi(model=config.chat_model_name)

        self.chain = self.__get_chain()

    def __get_chain(self):
        """
        获取最终的执行链
        """
        retriever = self.vector_service.get_retriever()

        def format_document(docs):
            """
            该函数的作用是把检索到的文档列表格式化成字符串, 以便在提示词中使用
            """
            if not docs:
                return '无相关参考资料'
            formatted_str = ''
            for doc in docs:
                formatted_str += f'文档片段: {doc.page_content}\n文档元数据: {doc.metadata}\n\n'
            return formatted_str
        
        def format_for_retriever(value):
            """
            该函数的作用是把输入到检索器的{'input': 输入, 'history': 历史记录}内容只保留输入input
            """
            return value['input']

        def format_for_prompt_template(value):
            """
            该函数的作用是把输入到提示词模板的{'input': {'input': 输入, 'history': 历史记录}, 'context': 检索到的文档}
            提取成 {'input': 输入, 'context': 检索到的文档, 'history': 历史记录} 以便在提示词中使用
            """
            new_value = {}
            new_value['input'] = value['input']['input']
            new_value['context'] = value['context']
            new_value['history'] = value['input']['history']
            return new_value

        chain = (
            {
                'input': RunnablePassthrough(),
                'context': RunnableLambda(format_for_retriever) | retriever | format_document
            } | RunnableLambda(format_for_prompt_template) | self.prompt_template | self.chat_model | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_message_key='input',
            history_messages_key='history'
        )

        return conversation_chain

if __name__ == "__main__":
    # session_id 配置
    session_config = {
        'configurable': {
            'session_id': 'user_001'
        }
    }
    res = RagService().chain.invoke({'input': '我的身高170厘米, 尺码推荐'}, session_config)
    print(res)