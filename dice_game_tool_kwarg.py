# %%
import random

import logfire
import nest_asyncio  # type: ignore
from pydantic_ai import Agent, RunContext, Tool

logfire.configure()
logfire.instrument_asyncpg()
nest_asyncio.apply()


def roll_die() -> str:
    """Roll a six-sided die and return the result."""
    return str(random.randint(1, 6))


def get_player_name(ctx: RunContext[str]) -> str:
    """Get the player's name."""
    return ctx.deps


agent_a = Agent(
    "google-gla:gemini-1.5-flash",
    deps_type=str,
    tools=[roll_die, get_player_name],
)
agent_b = Agent(
    "google-gla:gemini-1.5-flash",
    deps_type=str,
    tools=[
        Tool(roll_die, takes_ctx=False),
        Tool(get_player_name, takes_ctx=True),
    ],
)
dice_result = agent_b.run_sync("My guess is 4", deps="Anne")
print(dice_result.data)
# > Congratulations Anne, you guessed correctly! You're a winner!
