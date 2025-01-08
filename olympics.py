# %%
import logfire
import nest_asyncio  # type: ignore
from pydantic import BaseModel
from pydantic_ai import Agent

logfire.configure()
logfire.instrument_asyncpg()
nest_asyncio.apply()


class CityLocation(BaseModel):
    city: str
    country: str


agent = Agent("google-gla:gemini-1.5-flash", result_type=CityLocation)
result = agent.run_sync("Where were the olympics held in 1980?")
print(result.data)
# > city='London' country='United Kingdom'
print(result.usage())

# %%
