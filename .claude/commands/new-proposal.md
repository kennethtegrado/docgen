You are helping scaffold and fill a **Project Proposal** document using the docgen tool.

**Project name:** $ARGUMENTS

## Step 1: Scaffold

Run this command to create the project structure:
```
source .venv/bin/activate && python -m docgen.init_project "$ARGUMENTS" proposal
```

## Step 2: Interactive Q&A

Read the generated markdown file at `projects/$ARGUMENTS/docs/$ARGUMENTS-proposal.md` first.

Ask questions in these rounds, waiting for answers before proceeding:

### Round 1 - Context & Problem
- Who is the client/audience?
- What problem are you solving for them?
- What is the current situation or pain point?

### Round 2 - Solution
- What is your proposed solution? (high-level)
- What are the key features/deliverables?
- What is the technical approach?
- What is in scope vs out of scope?

### Round 3 - Timeline & Budget
- What are the project phases and estimated durations?
- What are the key milestones?
- What is the budget/pricing structure? (fixed fee, hourly, etc.)
- What are the payment terms?

### Round 4 - Risk & Acceptance
- What are the main risks?
- What are the acceptance criteria?
- What assumptions are you making?

### Round 5 - Closing
- Why are you the right fit? (qualifications, experience)
- What are the next steps after acceptance?

## Step 3: Write

After each round, update the markdown document with the user's answers. Generate timeline gantt charts where appropriate. Update revision history.

## Step 4: Offer Export

When done, suggest: "Run `/export-pdf projects/$ARGUMENTS/docs/$ARGUMENTS-proposal.md` to generate a PDF."
