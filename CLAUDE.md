# Docgen - Project Conventions

## Overview
Personal document generation tool. Scaffolds tech specs, proposals, SOWs, and architecture docs from Jinja2 templates, then exports to PDF via Pandoc + WeasyPrint.

## Project Structure
- `docgen/` — Python package (config, export pipeline, diagrams, scaffolding)
- `templates/` — Jinja2 markdown templates and partials
- `styles/` — CSS for WeasyPrint PDF rendering
- `projects/` — Generated per-project document folders

## Key Commands
- Scaffold: `python -m docgen.init_project "<project-name>" <doc-type>`
- Export PDF: `python -m docgen.export "<path-to-markdown>"`
- Export diagrams: `python -m docgen.diagrams "<path-to-markdown>"`

## Conventions
- All config comes from `docgen.config.json` at project root
- Documents use YAML frontmatter for metadata and section flags
- Templates use Jinja2 with `{{ variable }}` and `{% if sections.flag %}` guards
- CSS uses `@page` rules for print layout (WeasyPrint CSS Paged Media)
- Mermaid blocks are pre-processed to PNG before Pandoc runs
- Python venv at `.venv/` — activate before running

## Doc Types
- `tech-spec` — Technical specification
- `proposal` — Project proposal
- `sow` — Statement of work
- `architecture` — Architecture/solution document

## Dependencies
- System: pandoc, drawio (cask), mermaid-cli (npm global)
- Python: Jinja2, PyYAML, python-frontmatter, WeasyPrint, Pygments
