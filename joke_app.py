# %%

from dataclasses import dataclass

import httpx
import logfire
import nest_asyncio  # type: ignore
from pydantic_ai import Agent, RunContext

logfire.configure()
logfire.instrument_asyncpg()
nest_asyncio.apply()


@dataclass
class MyDeps:
    api_key: str
    http_client: httpx.AsyncClient

    async def system_prompt_factory(self) -> str:
        response = await self.http_client.get("https://example.com")
        response.raise_for_status()
        return f"Prompt: {response.text}"


joke_agent = Agent(
    "openai:gpt-4o-mini",
    deps_type=MyDeps,
)


@joke_agent.system_prompt
async def get_system_prompt(ctx: RunContext[MyDeps]) -> str:
    return await ctx.deps.system_prompt_factory()


async def application_code(prompt: str) -> str:
    ...
    ...
    # now deep within application code we call our agent
    async with httpx.AsyncClient() as client:
        app_deps = MyDeps("foobar", client)
        result = await joke_agent.run(prompt, deps=app_deps)
    return result.data
