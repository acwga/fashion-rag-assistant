
md5_path = './md5.text'

# Chroma向量数据库配置
collection_name = 'rag'
persist_directory = './chroma_db'

# spliter文本分割配置
chunk_size = 1000
chunk_overlap = 100
separators = ['\n\n', '\n', '.', '!', '?', '。', '！', '？', ' ', '']
max_split_char_num = 1000

# 向量存储服务类配置
similarity_threshold = 1
embedding_model_name = 'text-embedding-v4'
chat_model_name = 'qwen3-max'