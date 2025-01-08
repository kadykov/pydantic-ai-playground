# %%
import asyncio
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


agent = Agent(
    "openai:gpt-4o-mini",
    deps_type=MyDeps,
)


@agent.system_prompt
async def get_system_prompt(ctx: RunContext[MyDeps]) -> str:
    response = await ctx.deps.http_client.get(
        "https://example.com",
        headers={"Authorization": f"Bearer {ctx.deps.api_key}"},
    )
    response.raise_for_status()
    return f"Prompt: {response.text}"


async def main():
    async with httpx.AsyncClient() as client:
        deps = MyDeps("foobar", client)
        result = await agent.run(
            "Tell me a joke.",
            deps=deps,
        )
        print(result.data)
        # > Did you hear about the toothpaste scandal? They called it Colgate.


# %%

asyncio.run(main())
