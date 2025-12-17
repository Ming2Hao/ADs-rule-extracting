from google.adk.agents import Agent

# The root agent is used to create json formatted output indicating whether the given aircraft is affected by maintenance requirements.
root_agent = Agent(
    model='gemini-2.0-flash',
    name='root_agent',
    description='Main coordinator.',
    instruction='You are an Aircraft Maintenance Compliance Officer. your duty is to ensure that the aircraft is in compliance with the maintenance requirements. state whether its affected by each AD (yes/no) and briefly why. create it in json format with only the keys: aircraft_model, affected (yes/no), reason'
)