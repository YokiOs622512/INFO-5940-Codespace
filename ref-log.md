# Reflection Document

## What I learn from implementing a multi-agent workflow?
1. I learned that when implementing a multi-agent workflow, it is important to write detailed and precise prompts for each agent. The prompts should be as clear as possible to ensure the agent fully understands the instructions. Moreover, the language used should not be vague. Some sentences that are easy for humans to interpret may be misunderstood by the agent. For example, when writing the prompt for the Reviewer Agent, I initially wrote that if there were no changes to the itinerary, the agent should output None. What I meant was to literally output the word None, but the agent interpreted it as producing no output at all. This experience taught me the importance of giving explicit, unambiguous instructions in multi-agent prompt design.

## Challenges faced and how I address them.
- **Reviewer Agent Part**
1. The first challenge I faced was when the Reviewer Agent stopped generating the revised itinerary after producing the Delta List. I solved this problem by strengthening the prompt instructions to explicitly require the agent to generate the full itinerary immediately after the Delta List section.

2. The second challenge occurred when, after validating the information in the raw plan, the Reviewer Agent did not regenerate detailed itineraries for the days that required no changes. I solved this by refining the prompt rules. I specify that the agent must not skip, merge, or summarize days, and must reproduce the full itinerary exactly as in the original plan for any unchanged sections.

- **Planner Agent Part**
1. The challenge I faced in the Planner Agent was that it produced inconsistent cost calculations. For example, if the actual total cost was $800 but the user requested a $1,500 budget travel plan, the Planner Agent would pretend to use the entire budget and return a total around $1,400. I solved this problem by adding a rule to the prompt instructing the agent not to artificially adjust the total cost to match the user’s budget.

## Design choices
1. To avoid having the agent artificially adjust the total cost, I first specified that each day’s plan should include a brief summary of the daily expenses, followed by a final total cost at the end of the itinerary. I then defined explicit rules for how the costs should be calculated, detailing which items must be included, such as lodging, meals, transportation, and activity fees.

# GenAI Usage
1. Use GenAI to fix the logic and grammar in ref-log.md.
2. Use GenAI to understand the code logic in assign_2.py.
3. Use GenAI to understand what a good system prompt for an agent should include.
    - role
    - goal
    - rule
    - step
    - output format
4. Use GenAI to identify which part of the prompt caused the Reviewer Agent to generate a partial itinerary.
5. Use GenAI to identify which part of the prompt caused the Planner Agent to produce artificially adjusted total costs.