from .tool_registry import regisry

@regisry.registerTool(
    name="AskUser",
    description=(
        "向用户提出澄清性问题并等待用户输入。"
        "当信息不足、存在歧义或需要用户决策时使用。"
    ),
)
def ask_user(question: str) -> str:
    """
    向用户提问并返回用户输入。

    参数:
        question (str): 需要向用户询问的问题

    返回:
        str: 用户的回答
    """
    print("\n🤖 Agent 向你提问：")
    print(question)
    print("\n✍️ 请输入你的回答（回车确认）：")

    try:
        user_input = input("> ").strip()
        return user_input if user_input else "(用户未提供有效回答)"
    except EOFError:
        return "(用户未提供输入)"