You are helping scaffold and fill a **Statement of Work** document using the docgen tool.

**Project name:** $ARGUMENTS

## Step 1: Scaffold

Run this command to create the project structure:
```
source .venv/bin/activate && python -m docgen.init_project "$ARGUMENTS" sow
```

## Step 2: Interactive Q&A

Read the generated markdown file at `projects/$ARGUMENTS/docs/$ARGUMENTS-sow.md` first.

Ask questions in these rounds, waiting for answers before proceeding:

### Round 1 - Parties & Background
- Who is the client? (name, organization, contact)
- What is the background/context for this engagement?
- What is the overall purpose of this SOW?

### Round 2 - Scope & Deliverables
- What are the specific objectives?
- What are the deliverables with acceptance criteria?
- What is explicitly out of scope?
- What assumptions and dependencies exist?

### Round 3 - Work Breakdown & Timeline
- What are the project phases? (discovery, implementation, testing, etc.)
- What is the duration for each phase?
- What are the key milestones and target dates?

### Round 4 - Pricing & Payment
- What is the fee structure? (fixed, T&M, retainer)
- What is the total project cost?
- What is the payment schedule? (e.g., 50/25/25)
- Are expenses included or billed separately?
- What are the change request terms?

### Round 5 - Terms & Conditions
- Confidentiality terms?
- IP ownership terms?
- Termination conditions?
- Acceptance process (review period, feedback cycles)?

## Step 3: Write

After each round, update the markdown document. Generate timeline gantt charts. Update revision history.

## Step 4: Offer Export

When done, suggest: "Run `/export-pdf projects/$ARGUMENTS/docs/$ARGUMENTS-sow.md` to generate a PDF."
