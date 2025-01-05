# %%
import logfire
import nest_asyncio
from pydantic import BaseModel
from pydantic_ai import Agent

logfire.configure()


logfire.instrument_asyncpg()

nest_asyncio.apply()


class City(BaseModel):
    name: str
    country: str


agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt="Be concise, reply with one sentence.",
    result_type=City,
)

result_sync = agent.run_sync("What is the capital of Italy?")
print(result_sync.data)

# %%
