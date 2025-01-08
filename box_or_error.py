# %%
import logfire
import nest_asyncio  # type: ignore
from pydantic import BaseModel
from pydantic_ai import Agent

logfire.configure()
logfire.instrument_asyncpg()
nest_asyncio.apply()


class Box(BaseModel):
    width: int
    height: int
    depth: int
    units: str


agent: Agent[None, Box | str] = Agent(
    "openai:gpt-4o-mini",
    result_type=Box | str,  # type: ignore
    system_prompt=(
        "Extract me the dimensions of a box, "
        "if you can't extract all data, ask the user to try again."
    ),
)

result = agent.run_sync("The box is 10x20x30")
print(result.data)
# > Please provide the units for the dimensions (e.g., cm, in, m).

result = agent.run_sync("The box is 10x20x30 cm")
print(result.data)
# > width=10 height=20 depth=30 units='cm'

# %%
