PLANNER_PROMPT_TEMPLATE = """
你是一个顶级的AI规划专家。你的任务是将用户提出的复杂问题分解成一个由多个简单步骤组成的行动计划。
请确保计划中的每个步骤都是一个独立的、可执行的子任务，并且严格按照逻辑顺序排列。
你的输出必须是一个Python列表，其中每个元素都是一个描述子任务的字符串。

问题: {question}

请严格按照以下格式输出你的计划,```python与```作为前后缀是必要的:
```python
["步骤1", "步骤2", "步骤3", ...]
```
"""
import re

class PlannerAgent:
    def __init__(self, llm):
        self.llm = llm

    def plan(self, usr_prompt: str) -> list:
        prompt = PLANNER_PROMPT_TEMPLATE.format(question=usr_prompt)

        message = self.llm.construct_prompt(
            sys_prompt=prompt,
            usr_prompt="请生成详细的行动计划：",
            image_input=None
        )

        response = self.llm.inference(messages=message, temperature=0.5)

        # 提取代码块中的列表
        code_block_pattern = r"```python(.*?)```"
        match = re.search(code_block_pattern, response, re.DOTALL)
        if match:
            code_block = match.group(1).strip()
            try:
                plan = eval(code_block)
                if isinstance(plan, list):
                    return plan
            except Exception as e:
                print(f"解析计划时出错: {e}")

        print("未能生成有效的计划。")
        return []
    

EXECUTOR_PROMPT_TEMPLATE = """
你是一位顶级的AI执行专家。你的任务是严格按照给定的计划，一步步地解决问题。
你将收到原始问题、完整的计划、以及到目前为止已经完成的步骤和结果。
请你专注于解决“当前步骤”，并仅输出该步骤的最终答案，不要输出任何额外的解释或对话。

# 原始问题:
{question}

# 完整计划:
{plan}

# 历史步骤与结果:
{history}

# 当前步骤:
{current_step}

请仅输出针对“当前步骤”的回答:
"""

class Executor:
    def __init__(self, llm):
        self.llm = llm

    def execute(self, usr_prompt: str, plan: list) -> str:
        history = []
        for step in plan:
            history_str = "\n".join([f"步骤: {h[0]}\n结果: {h[1]}" for h in history])

            prompt = EXECUTOR_PROMPT_TEMPLATE.format(
                question=usr_prompt,
                plan=plan,
                history=history_str,
                current_step=step
            )

            message = self.llm.construct_prompt(
                sys_prompt=prompt,
                usr_prompt="请执行当前步骤并提供答案：",
                image_input=None
            )

            response = self.llm.inference(messages=message, temperature=0.5)

            history.append((step, response.strip()))

        if history:
            return history[-1][1]
        return "未能生成最终答案。"
    

class PlanAndSolveAgent:
    def __init__(self, llm):
        self.planner = PlannerAgent(llm)
        self.executor = Executor(llm)

    def run(self, usr_prompt: str, image_input=None) -> str:
        plan = self.planner.plan(usr_prompt)
        if not plan:
            return "未能生成有效的行动计划。"

        final_answer = self.executor.execute(usr_prompt, plan)
        return final_answer