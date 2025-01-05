# %%
import nest_asyncio
from pydantic_ai import Agent

nest_asyncio.apply()

agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt="Be concise, reply with one sentence.",
)

result = agent.run_sync('Where does "web 2.0" come from?')
print(result.data)

# %%
