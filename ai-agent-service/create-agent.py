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

project_client = AIProjectClient.from_connection_string(
    credential = credential,
    conn_str = PROJECT_CONNECTION_STRING
)

with project_client:
    agent = project_client.agents.create_agent(
        model = AI_AGENT_MODEL_DEPLOYMENT,
        name = "my-agent",
        instructions = "You are helpful agent"
    )
    print(f"Created agent, agent ID: {agent.id}")

    # 削除したい場合は以下を実行
    # project_client.agents.delete_agent(agent.id)
    # print("Deleted agent")
