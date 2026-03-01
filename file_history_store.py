import json
import os
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import message_to_dict, messages_from_dict

def get_history(session_id):
    """
    获取指定会话ID的聊天历史记录对象。
    """
    return FileChatMessageHistory(session_id, './chat_history')

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        self.session_id = session_id            # 会话ID
        self.storage_path = storage_path        # 不同会话id的存储文件, 所在的文件夹路径
        self.file_path = os.path.join(self.storage_path, self.session_id)       # 完整的文件路径

        # 确保文件夹存在
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_messages(self, messages):
        """
        将新的消息列表添加到现有的聊天历史中，并将更新后的历史保存到文件中。
        """
        all_messages = list(self.messages)      # 已有的消息列表
        all_messages.extend(messages)           # 新的和已有的融合成一个list
        new_messages = [message_to_dict(message) for message in all_messages]   # 将消息对象转为字典列表
        
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(new_messages, f)          # 将数据写入文件
    
    @property
    def messages(self):
        """
        从文件中读取聊天历史记录，并将其转换为消息对象列表返回。
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                message_data = json.load(f)
                return messages_from_dict(message_data)   # 将字典列表转回消息对象列表
        except FileNotFoundError:
            return []
        
    def clear(self):
        """
        清空当前会话的聊天历史记录，并将空列表写入文件。
        """
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump([], f)