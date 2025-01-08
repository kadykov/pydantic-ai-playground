# %%
from datetime import date

import logfire
import nest_asyncio  # type: ignore
from pydantic_ai import Agent, RunContext

logfire.configure()


logfire.instrument_asyncpg()
nest_asyncio.apply()


agent = Agent(
    "openai:gpt-4o-mini",
    deps_type=str,
    system_prompt="Use the customer's name while replying to them.",
)


@agent.system_prompt
def add_the_users_name(ctx: RunContext[str]) -> str:
    return f"The user's name is {ctx.deps}."


@agent.system_prompt
def add_the_date() -> str:
    return f"The date is {date.today()}."


result = agent.run_sync("What is the date?", deps="Frank")
print(result.data)
# > Hello Frank, the date today is 2032-01-02.

# %%
