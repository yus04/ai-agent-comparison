import os
import asyncio
from typing import Annotated
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)

load_dotenv()

SEMANTIC_KERNEL_AOAI_DEPLOYMENT_NAME = os.getenv("SEMANTIC_KERNEL_AOAI_DEPLOYMENT_NAME")
SEMANTIC_KERNEL_AOAI_API_KEY = os.getenv("SEMANTIC_KERNEL_AOAI_API_KEY")
SEMANTIC_KERNEL_AOAI_BASE_URL = os.getenv("SEMANTIC_KERNEL_AOAI_BASE_URL")

class LightsPlugin:
    lights = [
        {"id": 1, "name": "Table Lamp", "is_on": False},
        {"id": 2, "name": "Porch light", "is_on": False},
        {"id": 3, "name": "Chandelier", "is_on": True},
    ]

    @kernel_function(
        name = "get_lights",
        description = "ライトのリストとその現在の状態を取得する",
    )
    def get_state(
        self,
    ) -> Annotated[str, "the output is a string"]:
        """ライトのリストとその現在の状態を取得する。"""
        return self.lights

    @kernel_function(
        name = "change_state",
        description = "ライトの状態を変更する",
    )
    def change_state(
        self,
        id: int,
        is_on: bool,
    ) -> Annotated[str, "the output is a string"]:
        """ライトの状態を変更する。"""
        for light in self.lights:
            if light["id"] == id:
                light["is_on"] = is_on
                return light
        return None

async def main():
    # カーネルを初期化する
    kernel = Kernel()

    # Azure OpenAIチャット補完を追加する
    chat_completion = AzureChatCompletion(
        deployment_name = SEMANTIC_KERNEL_AOAI_DEPLOYMENT_NAME,
        api_key = SEMANTIC_KERNEL_AOAI_API_KEY,
        base_url = SEMANTIC_KERNEL_AOAI_BASE_URL,
    )
    kernel.add_service(chat_completion)

    # プラグインを追加する
    kernel.add_plugin(
        LightsPlugin(),
        plugin_name = "Lights",
    )

    # プランニングを有効にする
    execution_settings = AzureChatPromptExecutionSettings()
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto(auto_invoke=True)

    # 会話履歴を作成する
    history = ChatHistory()

    # 対話型チャットを開始する
    userInput = None
    while True:
        # ユーザーの入力を収集する
        userInput = input("User > ")

        # ユーザーが 'exit' と入力した場合、ループを終了する
        if userInput == "exit":
            break

        # ユーザーの入力を履歴に追加する
        history.add_user_message(userInput)

        # AIからの応答を取得する
        result = await chat_completion.get_chat_message_content(
            chat_history = history,
            settings = execution_settings,
            kernel = kernel,
        )

        # 結果を表示する
        print("Assistant > " + str(result))

        # エージェントのメッセージを履歴に追加する
        history.add_message(result)

# main関数を実行する
if __name__ == "__main__":
    asyncio.run(main())
