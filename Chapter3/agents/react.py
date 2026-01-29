from backend import OpenAILLM
from tools.tool_registry import regisry, ToolRegistry
import re
from PIL import Image
from typing import List, Union, Optional

REACT_PROMPT_TEMPLATE = """
请注意，你是一个有能力调用外部工具的智能助手。

可用工具如下:
{tools}

请严格按照以下格式进行回应:

Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。
Action: 你决定采取的行动，必须是以下格式之一:
- `{{tool_name}}[{{tool_input}}]`:调用一个可用工具。
- `Finish[最终答案]`:当你认为已经获得最终答案时。
- 当你收集到足够的信息，能够回答用户的最终问题时，你必须在Action:字段后使用 Finish[最终答案] 来输出最终答案。

现在，请开始解决以下问题:
Question: {question}
History: {history}
"""

class ReActAgent:

    def __init__(self, llm: OpenAILLM, tools: ToolRegistry = None, max_steps: int = 5):
        self.llm = llm
        self.registry = tools if tools else regisry
        self.max_steps = max_steps

    def run(self, usr_prompt: str, image_input: Union[Image.Image, List[Image.Image]] = None) -> Optional[str]:

        self.history = []
        current_step = 0

        while current_step < self.max_steps:

            current_step += 1

            tool_desc = self.registry.getAvailableTools()
            history_str = "\n".join(self.history)

            prompt = REACT_PROMPT_TEMPLATE.format(
                tools=tool_desc,
                question=usr_prompt,
                history=history_str
            )
        
            message = self.llm.construct_prompt(
                sys_prompt=prompt,
                usr_prompt="Now, start your response:",
                image_input=image_input
            )

            response = self.llm.inference(messages=message, temperature=1)

            thought, action = self._parse_output(response)

            if not thought:
                # print(f"Thought: {thought}")
                print("No thought detected, stopping.")
                break
            
            if not action:
                print("No action detected, stopping.")
                break
                
            if action.startswith("Finish"):
                final_answer = action[len("Finish["): -1]
                return final_answer

            tool_name, tool_input = self._parse_action(action)
            if tool_name and tool_input:
                tool_func = self.registry.getTool(tool_name)
                if tool_func:
                    tool_result = tool_func(tool_input)
                else:
                    tool_result = f"工具 '{tool_name}' 未找到。"
            else:
                print("Invalid action format, stopping.")
                break

            print(Observation:=f"{tool_result}")

            self.history.append(f"Thought: {thought}")
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {tool_result}")

        print("Reached maximum steps without finishing.")
        return None

    def _parse_output(self, text: str):
        """
        解析 LLM 输出，提取 Thought 和 Action（支持多行）。
        """
        thought = None
        action = None

        thought_match = re.search(
            r"Thought:\s*(.*?)(?=\nAction:|\Z)",
            text,
            re.DOTALL
        )
        if thought_match:
            thought = thought_match.group(1).strip()

        action_match = re.search(
            r"Action:\s*(.*)",
            text,
            re.DOTALL
        )
        if action_match:
            action = action_match.group(1).strip()

        return thought, action
    def _parse_action(self, action_text: str):
        """
        解析 Action 字符串，提取工具名称和输入（支持多行）。
        """
        match = re.match(
            r"(\w+)\[(.*?)\]\s*$",
            action_text,
            re.DOTALL
        )
        if match:
            return match.group(1), match.group(2).strip()
        return None, None
