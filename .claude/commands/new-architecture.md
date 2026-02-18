You are helping scaffold and fill an **Architecture Document** using the docgen tool.

**Project name:** $ARGUMENTS

## Step 1: Scaffold

Run this command to create the project structure:
```
source .venv/bin/activate && python -m docgen.init_project "$ARGUMENTS" architecture
```

## Step 2: Interactive Q&A

Read the generated markdown file at `projects/$ARGUMENTS/docs/$ARGUMENTS-architecture.md` first.

Ask questions in these rounds, waiting for answers before proceeding:

### Round 1 - Context
- What system/product is this architecture for?
- What are the business drivers and constraints?
- What existing systems does this integrate with?
- Who is the audience for this document?

### Round 2 - High-Level Architecture
- What is the overall architecture style? (microservices, monolith, serverless, etc.)
- What are the main components/services?
- What are the key technology choices?
- Should we generate C4 diagrams? (context, container, component levels)

### Round 3 - Component Details
- For each major component: responsibility, technology, interfaces?
- What is the data model? (entities, relationships)
- What does the data flow look like? (offer sequence diagrams)

### Round 4 - Infrastructure & Cross-Cutting
- What is the infrastructure setup? (cloud provider, regions, environments)
- Deployment strategy? (CI/CD, containers, rollback)
- Security approach? (auth, encryption, secrets)
- Observability? (logging, metrics, tracing)
- Performance targets and scaling approach?
- Reliability requirements? (SLAs, DR)

### Round 5 - Decisions & Risks
- What are the key architecture decisions (ADRs)?
- For each: context, decision, trade-offs?
- What are the technical risks and debt items?

## Step 3: Write

After each round, update the markdown document. Generate mermaid diagrams (C4, sequence, ER diagrams) as discussed. Update revision history.

## Step 4: Offer Export

When done, suggest: "Run `/export-pdf projects/$ARGUMENTS/docs/$ARGUMENTS-architecture.md` to generate a PDF."
