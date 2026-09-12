"""Sets up the Arcade-backed tool suite (Gmail, Slack, Notion) and walks the
user through Arcade's OAuth2 authorization flow for each provider."""

from arcadepy import Arcade
from langchain_arcade import ToolManager

import config


def build_tool_manager() -> tuple[Arcade, ToolManager]:
    arcade_client = Arcade(api_key=config.ARCADE_API_KEY)
    manager = ToolManager(client=arcade_client)
    return arcade_client, manager


def authorize_tools(tools, user_id: str, client: Arcade) -> None:
    """Authorize many tools at once, grouping OAuth scopes by provider so the
    user completes at most one authorization flow per provider."""
    provider_to_scopes: dict[str, set[str]] = {}
    for tool in tools:
        provider = tool.requirements.authorization.provider_id
        provider_to_scopes.setdefault(provider, set())
        if tool.requirements.authorization.oauth2.scopes:
            provider_to_scopes[provider] |= set(tool.requirements.authorization.oauth2.scopes)

    for provider, scopes in provider_to_scopes.items():
        auth_response = client.auth.start(user_id=user_id, scopes=list(scopes), provider=provider)
        if auth_response.status != "completed":
            print(f"Please click here to authorize: {auth_response.url}")
            print("Waiting for authorization completion...")
            client.auth.wait_for_completion(auth_response)


def build_authorized_tools(arcade_client: Arcade, manager: ToolManager) -> list:
    """Register the Gmail/Slack/Notion tools this agent needs, authorize each
    provider, and return them as LangChain-ready tool objects."""
    for tool_name in config.INIT_TOOLS:
        manager.init_tools(tools=[tool_name])
    for tool_name in config.ADDED_TOOLS:
        manager.add_tool(tool_name)
    for toolkit in config.TOOLKITS:
        manager.add_toolkit(toolkit)

    authorize_tools(tools=manager.definitions, user_id=config.ARCADE_USER_ID, client=arcade_client)

    return manager.to_langchain()
