"""Project scaffolding: creates project folders and initial markdown from templates."""

import sys
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from docgen.config import (
    TEMPLATES_DIR,
    load_config,
    get_project_paths,
)

DOC_TYPES = {
    "tech-spec": "tech-spec.md.j2",
    "proposal": "proposal.md.j2",
    "sow": "sow.md.j2",
    "architecture": "architecture.md.j2",
}

# Section defaults per doc type (controls which Jinja2 conditionals render)
SECTION_DEFAULTS = {
    "tech-spec": {
        "toc": True, "cover_page": True, "page_numbers": True, "headers": True,
        "executive_summary": True, "revision_history": True, "appendix": True,
        "glossary": True, "references": True, "risk_assessment": True,
        "timeline": True, "budget": False, "acceptance_criteria": True,
        "architecture_diagrams": True,
    },
    "proposal": {
        "toc": True, "cover_page": True, "page_numbers": True, "headers": True,
        "executive_summary": True, "revision_history": True, "appendix": True,
        "glossary": False, "references": True, "risk_assessment": True,
        "timeline": True, "budget": True, "acceptance_criteria": True,
        "architecture_diagrams": False,
    },
    "sow": {
        "toc": True, "cover_page": True, "page_numbers": True, "headers": True,
        "executive_summary": False, "revision_history": True, "appendix": True,
        "glossary": False, "references": True, "risk_assessment": True,
        "timeline": True, "budget": True, "acceptance_criteria": True,
        "architecture_diagrams": False,
    },
    "architecture": {
        "toc": True, "cover_page": True, "page_numbers": True, "headers": True,
        "executive_summary": True, "revision_history": True, "appendix": True,
        "glossary": True, "references": True, "risk_assessment": True,
        "timeline": False, "budget": False, "acceptance_criteria": False,
        "architecture_diagrams": True,
    },
}


def scaffold_project(project_name: str, doc_type: str, title: str = "") -> Path:
    """Create a new project folder structure and render the initial document."""
    if doc_type not in DOC_TYPES:
        raise ValueError(f"Unknown doc type '{doc_type}'. Must be one of: {list(DOC_TYPES.keys())}")

    paths = get_project_paths(project_name)

    # Create all directories
    for p in paths.values():
        p.mkdir(parents=True, exist_ok=True)

    # Load config (global, merged with project overrides if project config exists)
    config = load_config(project_name)

    # Build template context
    if not title:
        title = project_name.replace("-", " ").title()

    context = {
        "title": title,
        "author": config["author"],
        "date": date.today().isoformat(),
        "client": "",
        "project": project_name,
        "company": config.get("company", ""),
        "email": config.get("email", ""),
        "mermaid_theme": config.get("mermaid_theme", "default"),
        "export_format": config.get("default_export_format", "png"),
        "paper_size": config.get("default_paper_size", "A4"),
        "margin": config.get("default_margin", "2cm"),
        "accent_color": config.get("accent_color", "#2563eb"),
        "sections": SECTION_DEFAULTS.get(doc_type, {}),
    }

    # Render template
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template(DOC_TYPES[doc_type])
    rendered = template.render(**context)

    # Write the document
    doc_filename = f"{project_name}-{doc_type}.md"
    doc_path = paths["docs"] / doc_filename
    doc_path.write_text(rendered)

    print(f"Project scaffolded: {paths['root']}")
    print(f"  Document: {doc_path}")
    print(f"  Diagrams: {paths['diagrams']}")
    print(f"  Output:   {paths['output']}")
    print(f"  Assets:   {paths['assets']}")

    return doc_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python -m docgen.init_project <project-name> <doc-type> [title]")
        print(f"Doc types: {list(DOC_TYPES.keys())}")
        sys.exit(1)

    project_name = sys.argv[1]
    doc_type = sys.argv[2]
    title = sys.argv[3] if len(sys.argv) > 3 else ""

    scaffold_project(project_name, doc_type, title)
