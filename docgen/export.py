"""Export pipeline: Markdown → preprocess diagrams → Pandoc → WeasyPrint → PDF."""

import subprocess
import sys
import tempfile
from pathlib import Path

import frontmatter as fm

from docgen.config import STYLES_DIR, load_config
from docgen.diagrams import process_diagrams


def export_pdf(doc_path: Path, output_path: Path | None = None) -> Path:
    """Export a markdown document to PDF via Pandoc + WeasyPrint."""
    doc_path = doc_path.resolve()
    post = fm.load(str(doc_path))
    metadata = post.metadata

    # Determine project directory (docs/ -> project root)
    project_dir = doc_path.parent.parent
    project_name = metadata.get("project") or project_dir.name
    config = load_config(project_name)

    # Determine output path
    if output_path is None:
        output_dir = project_dir / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{doc_path.stem}.pdf"

    # Process diagrams (mermaid + draw.io)
    processed_content = process_diagrams(
        post.content, metadata, project_dir, project_name,
        doc_dir=doc_path.parent,
    )

    # Rebuild the full markdown with frontmatter
    processed_doc = f"---\n"
    for key, value in metadata.items():
        if isinstance(value, str):
            processed_doc += f'{key}: "{value}"\n'
        elif isinstance(value, bool):
            processed_doc += f"{key}: {'true' if value else 'false'}\n"
        else:
            processed_doc += f"{key}: {value}\n"
    processed_doc += f"---\n\n{processed_content}"

    # Write processed markdown to temp file in the same dir as the source doc
    # so that relative image paths (e.g., ../diagrams/exports/) resolve correctly
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, dir=str(doc_path.parent)
    ) as f:
        f.write(processed_doc)
        temp_md = Path(f.name)

    # Build Pandoc command
    export_config = metadata.get("export", {})
    sections = metadata.get("sections", {})
    css_path = STYLES_DIR / "print.css"

    pandoc_cmd = [
        "pandoc",
        str(temp_md),
        "-o", str(output_path),
        "--pdf-engine=weasyprint",
        f"--css={css_path}",
        "--standalone",
        "--self-contained",
        f"--metadata=title:{metadata.get('title', 'Document')}",
    ]

    # Add TOC if enabled
    if sections.get("toc", True):
        pandoc_cmd.append("--toc")
        pandoc_cmd.append("--toc-depth=3")

    # Add syntax highlighting
    pandoc_cmd.extend(["--highlight-style", "pygments"])

    try:
        result = subprocess.run(
            pandoc_cmd,
            check=True,
            capture_output=True,
            text=True,
            cwd=str(project_dir),
        )
        print(f"PDF exported: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Pandoc error: {e.stderr}", file=sys.stderr)
        raise
    finally:
        temp_md.unlink(missing_ok=True)

    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m docgen.export <path-to-markdown> [output-path]")
        sys.exit(1)

    doc_path = Path(sys.argv[1]).resolve()
    output_path = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None

    export_pdf(doc_path, output_path)
