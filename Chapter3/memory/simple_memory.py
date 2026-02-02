from typing import List, Dict, Any, Union, Optional


class SimpleMemory:
    def __init__(self, max_size: int = 1e5):
        self.max_size = max_size
        self.memory: List[Dict[str, Any]] = []

    def add(self, type: str, content: Any) -> None:
        entry = {"type": type, "content": content}
        if len(self.memory) >= self.max_size:
            self.memory.pop(0)  # 移除最旧的记忆
        self.memory.append(entry)

    def get_memory(self) -> List[Dict[str, Any]]:
        return self.memory
    
    def get_trajectory(self) -> str:
        """
        将所有记忆记录格式化为一个连贯的字符串文本，用于构建提示词。
        """
        trajectory_parts = []
        for record in self.memory:
            if record['type'] == 'execution':
                trajectory_parts.append(f"--- 上一轮尝试 (代码) ---\n{record['content']}")
            elif record['type'] == 'reflection':
                trajectory_parts.append(f"--- 评审员反馈 ---\n{record['content']}")
        
        return "\n\n".join(trajectory_parts)
    
    def get_last_execution(self) -> Optional[str]:
        """
        获取最近一次的执行结果 (例如，最新生成的代码)。
        如果不存在，则返回 None。
        """
        for record in reversed(self.memory):
            if record['type'] == 'execution':
                return record['content']
        return None

    def clear(self) -> None:
        self.memory = []