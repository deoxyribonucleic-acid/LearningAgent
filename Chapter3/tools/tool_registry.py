from typing import Any, Dict, List

class ToolRegistry:

    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def registerTool(self, name: str, description: str):
        """
        向工具箱中注册一个新工具。
        """
        def decorator(func):
            if name in self.tools:
                print(f"警告:工具 '{name}' 已存在，将被覆盖。")
            self.tools[name] = {
                "description": description,
                "func": func,
            }
            print(f"工具 '{name}' 已注册。")
            return func   # ⭐ 必须
        return decorator

    def getTool(self, name: str) -> callable:
        """
        根据名称获取一个工具的执行函数。
        """
        return self.tools.get(name, {}).get("func")

    def getAvailableTools(self) -> str:
        """
        获取所有可用工具的格式化描述字符串。
        """
        return "\n".join([
            f"- {name}: {info['description']}" 
            for name, info in self.tools.items()
        ])
    
regisry = ToolRegistry()