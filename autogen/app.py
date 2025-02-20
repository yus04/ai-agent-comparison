import os
import asyncio
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

load_dotenv()

AUTOGEN_AOAI_DEPLOYMENT_NAME = os.getenv("AUTOGEN_AOAI_DEPLOYMENT_NAME")
AUTOGEN_AOAI_MODEL = os.getenv("AUTOGEN_AOAI_MODEL")
AUTOGEN_AOAI_API_KEY = os.getenv("AUTOGEN_AOAI_API_KEY")
AUTOGEN_AOAI_API_VERSION = os.getenv("AUTOGEN_AOAI_API_VERSION")
AUTOGEN_AOAI_ENDPOINT = os.getenv("AUTOGEN_AOAI_ENDPOINT")

async def main() -> None:
    model_client = AzureOpenAIChatCompletionClient(
        azure_deployment = AUTOGEN_AOAI_DEPLOYMENT_NAME,
        model = AUTOGEN_AOAI_MODEL,
        api_key = AUTOGEN_AOAI_API_KEY,
        api_version = AUTOGEN_AOAI_API_VERSION,
        azure_endpoint = AUTOGEN_AOAI_ENDPOINT,
    )

    writer = AssistantAgent(
        name = "writer",
        description = "writer",
        system_message = "You are a writer. Please write a short story about a Tokyo.",
        model_client = model_client,
    )

    critic = AssistantAgent(
        name = "critic",
        description = "critic",
        system_message = "You are a critic. Please provide feedback on the story.",
        model_client = model_client,
    )

    # 'APPROVE' というテキストが受信されたらチャットを終了するテキスト終了条件
    termination = TextMentionTermination("APPROVE")

    # writer と critic が交互に参加するグループチャット
    group_chat = RoundRobinGroupChat([writer, critic], termination_condition = termination, max_turns = 12)

    # run_stream は中間メッセージをストリームする非同期ジェネレーターを返す
    stream = group_chat.run_stream(task = "Write a short story about a Tokyo in 2050.")
    # Console はストリームを表示するシンプルな UI
    await Console(stream)

asyncio.run(main())
