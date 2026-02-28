"""
知识库
"""
import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

def check_md5(md5_str):
    """
    检查传入的md5字符串是否被处理过
    如果被处理过, 则返回True, 否则返回False
    """
    # 如果md5文件不存在, 则创建一个空文件, 并返回False
    if not os.path.exists(config.md5_path):
        open(config.md5_path, 'w', encoding='utf-8').close()
        return False
    # 读取md5文件, 检查是否存在传入的md5字符串
    for line in open(config.md5_path, 'r', encoding='utf-8'):
        if line.strip() == md5_str:
            return True
    return False

def save_md5(md5_str):
    """
    将传入的md5字符串保存到数据库中
    """
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')

def get_string_md5(input_str, encoding='utf-8'):
    """
    将传入的字符串转换为md5字符串
    """
    str_bytes = input_str.encode(encoding)  # 将字符串转换为字节
    md5_obj = hashlib.md5()                 # 创建md5对象
    md5_obj.update(str_bytes)               # 更新md5对象
    md5_hex = md5_obj.hexdigest()           # 获取md5十六进制字符串
    return md5_hex

class KnowledgeBaseService:
    """
    知识库服务类
    """
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)
        # 创建Chroma向量数据库对象
        self.chroma = Chroma(
            collection_name=config.collection_name,                                 # 向量数据库表名
            embedding_function=DashScopeEmbeddings(model='text-embedding-v4'),      # 向量化函数
            persist_directory=config.persist_directory                              # 数据库本地存储文件夹
        )
        # 创建文本分割器对象
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,           # 分割后的文本段最大长度
            chunk_overlap=config.chunk_overlap,      # 连续文本段之间的重叠数量
            separators=config.separators,        # 自然段落划分的符号
            length_function=len                     # 长度统计的依据函数
        )

    def upload_by_str(self, data, filename):
        """
        将传入的字符串向量化, 并存入向量数据库中
        """
        md5_hex = get_string_md5(data)  # 获取字符串的md5值
        # 检查md5值是否已经存在, 如果存在则跳过处理, 否则继续处理
        if check_md5(md5_hex):
            return '[跳过], 内容已经存在向量库中'
        # 如果字符串长度超过最大分割长度, 则进行分割处理
        if len(data) > config.max_split_char_num:
            knowledge_chunks = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]
        # 将处理后的文本向量化, 并存入向量数据库中
        metadata = {
            'source': filename,
            'create_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'operator': 'wzh'
        }
        self.chroma.add_texts(
            texts=knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks]
        )
        # 将md5值保存到数据库中
        save_md5(md5_hex)
        return '[成功], 内容已经存入向量库中'

if __name__ == '__main__':
    service = KnowledgeBaseService()
    r = service.upload_by_str('999', 'testfile')
    print(r)