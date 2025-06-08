import logging
logging.basicConfig(level=logging.DEBUG)
from julep import Client
import time
import yaml
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

JULEP_API_KEY = os.environ["JULEP_API_KEY"]
AGENT_UUID = uuid.uuid4()
TASK_UUID = uuid.uuid4()
client = Client(api_key=JULEP_API_KEY, environment="production")

name="Julep Food Tour Planning Agent"
about="A agent that can generate a detailed itinerary for visiting tourist attractions in some locations, considering the current weather conditions."

food_tour_yaml=f"""

name: Julep Foodie Tour Planner
description: Suggests a food tour for each city based on current weather and iconic dishes.

input_schema:
  type: object
  properties:
    locations:
      type: array
      items:
        type: string
      description: List of cities to plan a foodie tour for.

tools:
- name: weather
  type: integration
  integration:
    provider: weather
    setup:
      openweathermap_api_key: "{os.getenv('OPENWEATHERMAP_API_KEY')}"

- name: internet_search
  type: integration
  integration:
    provider: brave
    setup:
      brave_api_key: "{os.getenv('BRAVE_API_KEY')}"

main:
- over: $ steps[0].input.locations
  map:
    tool: weather
    arguments:
      location: $ _

- over: $ steps[0].input.locations
  map:
    tool: internet_search
    arguments:
      query: $ '3 iconic dishes in ' + _


- over: $ list(zip(steps[0].input.locations, steps[1].output))
  map:
    tool: internet_search
    arguments:
      query: $ 'top-rated restaurants in ' + _[0] + ' for ' + ', '.join(_[1])

- evaluate:
    zipped: |-
      $ list(
        zip(
          steps[0].input.locations,
          [output['result'] for output in steps[0].output],
          steps[1].output,
          steps[2].output
        )
      )

- over: $ _['zipped']
  parallelism: 3
  map:
    prompt:
    - role: system
      content: >-
        You are a culinary travel planner. For each city, craft a one-day foodie itinerary
        with breakfast, lunch, and dinner. Consider the weather (e.g., suggest indoor vs outdoor),
        3 iconic dishes, and top restaurants serving them.
    - role: user
      content: >-
        Location: _[0]
        Weather: _[1]
        Iconic Dishes: _[2]
        Restaurants: _[3]
    unwrap: true

- evaluate:
    final_plan: |-
      $ '\\n---------------\\n'.join(activity for activity in _)
"""

agent = client.agents.create_or_update(
    agent_id=AGENT_UUID,
    name=name,
    about=about,
    model="gpt-4o"
)

task_definition = yaml.safe_load(food_tour_yaml)

# Create the task
task = client.tasks.create_or_update(
    task_id=TASK_UUID,
    agent_id=AGENT_UUID,
    **task_definition
)

# Create the execution
execution = client.executions.create(
    task_id=task.id,
    input={
        "locations": ["Dadar"]
    }
)

print("Started an execution. Execution ID:", execution.id)

execution = client.executions.get(execution.id)

while execution.status != "succeeded":
    time.sleep(5)
    execution = client.executions.get(execution.id)
    print(execution.output)
    print("Execution status: ", execution.status)
    print("-"*50)

execution = client.executions.get(execution.id)

if 'final_plan' in execution.output:
    print(execution.output['final_plan'])
else:
    print(execution.output)
