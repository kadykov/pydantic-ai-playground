# %%
import logfire
import nest_asyncio  # type: ignore
from pydantic_ai import Agent

logfire.configure()


logfire.instrument_asyncpg()
nest_asyncio.apply()

agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt="""
    Ты специалист по исправлению опечаток в субтитрах, сгенерированных с помощью распознавания речи.
    Исправь ошибки распознавания речи, отформатируй текст, добавь пропущенные знаки препинания, раздели текст на предложения и параграфы.
    """,
)

with open("unformatted.txt") as file:
    unformatted_text = file.read()

result = agent.run_sync(unformatted_text)

with open("formatted.txt", "w") as file:
    file.write(result.data)
print(result.data)

# %%
