
md5_path = './md5.text'

# Chroma向量数据库配置
collection_name = 'rag'
persist_directory = './chroma_db'

# spliter文本分割配置
chunk_size = 1000
chunk_overlap = 100
separators = ['\n\n', '\n', '.', '!', '?', '。', '！', '？', ' ', '']
max_split_char_num = 1000