# %%
import logfire
import nest_asyncio  # type: ignore
from pydantic_ai import Agent

logfire.configure()

logfire.instrument_asyncpg()
nest_asyncio.apply()

agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt="Be concise and to the point. Ask questions to get the information you need.",
)
# %%
# First run
result1 = agent.run_sync("Who was Albert Einstein?")
print(result1.data)
# > Albert Einstein was a German-born theoretical physicist.
# %%
# Second run, passing previous messages
result2 = agent.run_sync(
    "What was his most famous equation?",
    message_history=result1.new_messages(),
)
print(result2.data)
# > Albert Einstein's most famous equation is (E = mc^2).
# %%
result1.all_messages()
result1.new_messages()
