INITIAL_PROMPT_TEMPLATE = """
你是一位资深的Python程序员。请根据以下要求，编写一个Python函数。
你的代码必须包含完整的函数签名、文档字符串，并遵循PEP 8编码规范。

要求: {task}

请直接输出代码，不要包含任何额外的解释。
"""

REFLECT_PROMPT_TEMPLATE = """
你是一位极其严格的代码评审专家和资深算法工程师，对代码的性能有极致的要求。
你的任务是审查以下Python代码，并专注于找出其在<strong>算法效率</strong>上的主要瓶颈。

# 原始任务:
{task}

# 待审查的代码:
```python
{code}
```

请分析该代码的时间复杂度，并思考是否存在一种<strong>算法上更优</strong>的解决方案来显著提升性能。
如果存在，请清晰地指出当前算法的不足，并提出具体的、可行的改进算法建议（例如，使用筛法替代试除法）。
如果代码在算法层面已经达到最优，才能回答“无需改进”。

请直接输出你的反馈，不要包含任何额外的解释。
"""


REFINE_PROMPT_TEMPLATE = """
你是一位资深的Python程序员。你正在根据一位代码评审专家的反馈来优化你的代码。

# 原始任务:
{task}

# 你上一轮尝试的代码:
{last_code_attempt}
评审员的反馈：
{feedback}

请根据评审员的反馈，生成一个优化后的新版本代码。
你的代码必须包含完整的函数签名、文档字符串，并遵循PEP 8编码规范。
请直接输出优化后的代码，不要包含任何额外的解释。
"""

from backend import OpenAILLM
from memory.simple_memory import SimpleMemory

class ReflectAgent:
    def __init__(self, llm, max_iterations = 3, max_memory_size: int = 1e5):
        self.llm = llm
        self.max_iterations = max_iterations
        self.memory = SimpleMemory(max_size=max_memory_size)

    def run(self, usr_prompt: str, image_input=None) -> str:
        # 初始代码生成
        initial_prompt = INITIAL_PROMPT_TEMPLATE.format(task=usr_prompt)
        message = self.llm.construct_prompt(
            sys_prompt=initial_prompt,
            usr_prompt="请生成代码：",
            image_input=image_input
        )
        code_response = self.llm.inference(messages=message, temperature=0.5)
        self.memory.add(type="execution", content=code_response)

        for _ in range(self.max_iterations):  # 最多进行3轮反思和改进
            last_code = self.memory.get_last_execution()
            reflect_prompt = REFLECT_PROMPT_TEMPLATE.format(
                task=usr_prompt,
                code=last_code
            )
            message = self.llm.construct_prompt(
                sys_prompt=reflect_prompt,
                usr_prompt="请提供反馈：",
                image_input=image_input
            )
            feedback = self.llm.inference(messages=message, temperature=0.5)
            self.memory.add(type="reflection", content=feedback)

            if "无需改进" in feedback:
                break  # 如果不需要改进，结束循环

            refine_prompt = REFINE_PROMPT_TEMPLATE.format(
                task=usr_prompt,
                last_code_attempt=last_code,
                feedback=feedback
            )
            message = self.llm.construct_prompt(
                sys_prompt=refine_prompt,
                usr_prompt="请生成优化后的代码：",
                image_input=image_input
            )
            refined_code = self.llm.inference(messages=message, temperature=0.5)
            self.memory.add(type="execution", content=refined_code)

        return self.memory.get_last_execution()