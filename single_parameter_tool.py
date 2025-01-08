# %%
import logfire
import nest_asyncio  # type: ignore
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel

logfire.configure()
logfire.instrument_asyncpg()
nest_asyncio.apply()

agent = Agent()


class Foobar(BaseModel):
    """This is a Foobar"""

    ok: bool
    fps: int
    platform: str
    packages: list[str]
    dependencies: dict[str, str]
    x: int
    y: str
    z: float = 3.14


@agent.tool_plain
def foobar(f: Foobar) -> str:
    return str(f)


test_model = TestModel()
result = agent.run_sync("hello", model=test_model)
print(result.data)
# > {"foobar":"x=0 y='a' z=3.14"}
print(test_model.agent_model_function_tools)

# %%
