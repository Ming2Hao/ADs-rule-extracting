from google.adk.agents import Agent, LoopAgent, BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator
from google.adk.events import Event, EventActions

# Document reader agent to extract relevant text segments from the maintenance document.
document_reader = Agent(
    model='gemini-2.0-flash',
    name='document_reader',
    description='Document reader',
    instruction='You are a document reader. your duty is to read ALL the document and extract the information. return ONLY the text segments that define which aircraft are affected or excluded including the aircraft modifications and exceptions (applicability). Ignore inspection intervals, compliance times, etc. make sure that you read both of the files thoroughly. you MUST only output the extracted text segments.',
    output_key='document_reader_output'
)

# JSON rule maker agent to create a JSON rule based on the extracted text segments.
json_rule_maker= Agent(
    model='gemini-2.0-flash',
    name='json_rule_maker',
    description='JSON rule maker.',
    instruction='You are a JSON rule maker. your duty is to create a JSON rule based on the text segments extracted by the document reader.You MUST only output JSON matching this schema. No explanations, no prose.{{document_reader_output}}. Here is the schema: {"ad": string, "aircraft": [{"aircraft_model":{"exceptions":[string]}}]}. Make sure to include all the aircraft models mentioned in the text segments along with their exceptions. If no exceptions are mentioned for an aircraft model, use an empty list for exceptions.',
    output_key='json_rule_maker_output'
)

# Compliance reviewer agent to verify the correctness of the JSON rule.
compliance_reviewer= Agent(
    model='gemini-2.0-flash',
    name='compliance_reviewer',
    description='Compliance reviewer.',
    instruction='You are a compliance reviewer. your duty is to review the JSON rule and check if the JSON rule is correct according to the document reader.{{json_rule_maker_output}} {{document_reader_output}} Output "pass" or "fail"',
    output_key='compliance_reviewer_output'
)

# Class to check the compliance status and decide whether to stop or continue the refinement loop.
class CheckStatusAndEscalate(BaseAgent):
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        status = ctx.session.state.get("compliance_reviewer_output", "fail")
        should_stop = (status == "pass")
        yield Event(author=self.name, actions=EventActions(escalate=should_stop))

# Refinement loop to ensure the JSON rule is correct.
refinement_loop = LoopAgent(
    name="make_sure_json_rule_is_correct",
    max_iterations=5,
    sub_agents=[document_reader,json_rule_maker, compliance_reviewer, CheckStatusAndEscalate(name="StopChecker")]
)

# The root agent is used to create json formatted output indicating whether the given aircraft is affected by maintenance requirements.
root_agent = Agent(
    model='gemini-2.0-flash',
    name='root_agent',
    description='Main coordinator.',
    instruction='You are an Aircraft Maintenance Compliance Officer. your duty is to ensure that the aircraft is in compliance with the maintenance requirements. state whether its affected by each AD (yes/no) and briefly why. state it in json format with only the keys: aircraft_model, affected (yes/no), reason',
    sub_agents=[
        refinement_loop
    ]
)

