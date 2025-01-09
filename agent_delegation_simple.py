# %%
import logfire
import nest_asyncio  # type: ignore
from pydantic_ai import Agent, RunContext
from pydantic_ai.usage import UsageLimits

logfire.configure()

logfire.instrument_asyncpg()
nest_asyncio.apply()


joke_selection_agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt=(
        "Use the `joke_factory` to generate some jokes, then choose the best. "
        "You must return just a single joke."
    ),
)
joke_generation_agent = Agent("google-gla:gemini-1.5-flash", result_type=list[str])


@joke_selection_agent.tool
async def joke_factory(ctx: RunContext[None], count: int) -> list[str]:
    r = await joke_generation_agent.run(
        f"Please generate {count} jokes.",
        usage=ctx.usage,
    )
    return r.data


result = joke_selection_agent.run_sync(
    "Tell me a joke.",
    usage_limits=UsageLimits(request_limit=5, total_tokens_limit=300),
)
print(result.data)
# > Did you hear about the toothpaste scandal? They called it Colgate.
print(result.usage())


# %%
