You are helping scaffold and fill a **Technical Specification** document using the docgen tool.

**Project name:** $ARGUMENTS

## Step 1: Scaffold

Run this command to create the project structure:
```
source .venv/bin/activate && python -m docgen.init_project "$ARGUMENTS" tech-spec
```

## Step 2: Interactive Q&A

Now guide the user through filling the document section by section. Read the generated markdown file at `projects/$ARGUMENTS/docs/$ARGUMENTS-tech-spec.md` first.

Ask questions in these rounds, waiting for answers before proceeding:

### Round 1 - Context
- What problem does this solve? What is the current situation?
- Who is the audience for this spec?
- What is the scope (in scope / out of scope)?

### Round 2 - Goals & Design
- What are the primary goals? (numbered list)
- What are the explicit non-goals?
- What is the high-level technical approach?
- Are there key design decisions to document?

### Round 3 - Technical Details
- What are the main components/services involved?
- What APIs or data models need to be defined?
- Are there architecture diagrams needed? (offer to generate mermaid diagrams)
- What are the dependencies?

### Round 4 - Implementation
- What are the implementation phases?
- What is the timeline?
- What are the risks and mitigations?
- What are the acceptance criteria?

### Round 5 - Finalization
- Testing strategy?
- Rollout plan?
- Monitoring & observability needs?

## Step 3: Write

After each round, update the markdown document with the user's answers. Generate mermaid diagrams where appropriate. Update the revision history.

## Step 4: Offer Export

When done, suggest: "Run `/export-pdf projects/$ARGUMENTS/docs/$ARGUMENTS-tech-spec.md` to generate a PDF."
