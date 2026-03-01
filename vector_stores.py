from langchain_chroma import Chroma
import config_data as config

class VectorStoreService:
    """
    向量存储服务类, 负责管理向量存储和检索
    """
    def __init__(self, embedding):
        self.embedding = embedding  # 表示嵌入模型函数
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory
        )
    
    def get_retriever(self):
        """
        返回向量检索器, 方便加入chain
        """
        return self.vector_store.as_retriever(search_kwargs={'k': config.similarity_threshold})
    
if __name__ == "__main__":
    from langchain_community.embeddings import DashScopeEmbeddings
    retriever = VectorStoreService(DashScopeEmbeddings(model='text-embedding-v4')).get_retriever()

    res = retriever.invoke('我的体重180斤, 尺码推荐')
    print(res)