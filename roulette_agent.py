# %%
import nest_asyncio  # type: ignore
from pydantic_ai import Agent, RunContext

nest_asyncio.apply()

roulette_agent = Agent(
    "openai:gpt-4o-mini",
    deps_type=int,
    result_type=bool,
    system_prompt=(
        "Use the `roulette_wheel` function to see if the "
        "customer has won based on the number they provide."
    ),
)


@roulette_agent.tool
async def roulette_wheel(ctx: RunContext[int], square: int) -> str:
    """check if the square is a winner"""
    print(ctx.deps, square)
    return "winner" if square == ctx.deps else "loser"


# # Run the agent
# success_number = 18
# result = roulette_agent.run_sync("Put my money on square eighteen", deps=success_number)
# print(result.data)
# > True
# %%
success_number = 5
result = roulette_agent.run_sync("I bet five is the winner", deps=success_number)
print(result.data)
# > False

# %%
type(roulette_agent)
