import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

load_dotenv()

PROJECT_CONNECTION_STRING = os.getenv("PROJECT_CONNECTION_STRING")
AI_AGENT_MODEL_DEPLOYMENT = os.getenv("AI_AGENT_MODEL_DEPLOYMENT")

# Azure CLI でログインしている場合は以下のコードで認証情報を取得
# az login --tenant <tenant_id>　でログインしておく
credential = DefaultAzureCredential()

# 以下を変更
thread_id = "thread-id"

project_client = AIProjectClient.from_connection_string(
    credential = credential,
    conn_str = PROJECT_CONNECTION_STRING
)

with project_client:
    message = project_client.agents.create_message(
        thread_id = thread_id,
        role = "user",
        content = "Could you please help me?",
    )
    print(f"Created message, message ID: {message.id}")
