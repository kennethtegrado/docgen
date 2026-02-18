You are helping create a **Gantt Chart** using the docgen tool.

**Project name:** $ARGUMENTS

## Step 1: Determine Chart Type

Ask the user:
- Do you want a **high-level** gantt (sequential phases, simple) or a **detailed** gantt (multiple tasks per phase, dependencies)?

## Step 2: Gather Information

### For High-Level:
- What is the project title?
- What is the start date?
- What are the phases and their durations? (e.g., "Discovery: 2 weeks, Implementation: 6 weeks, Testing: 2 weeks")

### For Detailed:
- What are the phases?
- For each phase, what are the tasks?
- For each task: start date, duration, status (done/active/planned)?
- Are there milestones to mark?
- Are there dependencies between tasks?

## Step 3: Generate

Use the docgen gantt module to generate the chart:

```python
source .venv/bin/activate && python -c "
from docgen.gantt import generate_high_level_gantt, generate_gantt
# ... generate based on user input
"
```

Or construct the mermaid directly based on user input.

## Step 4: Present & Iterate

Show the generated mermaid gantt chart to the user. Ask if they want to:
- Adjust durations
- Add/remove phases or tasks
- Change the start date
- Add milestones or critical path markers

Iterate until they're satisfied.

## Step 5: Save

Save the final gantt chart to the project's docs folder if a project exists, or create a standalone file.
