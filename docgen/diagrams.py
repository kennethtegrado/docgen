"""Mermaid and draw.io diagram rendering for docgen."""

import platform
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from docgen.config import load_config


def _find_drawio_cmd() -> str:
    """Locate the draw.io CLI executable across platforms."""
    # Check PATH first (works if user has `drawio` symlinked or in PATH)
    drawio = shutil.which("drawio") or shutil.which("draw.io")
    if drawio:
        return drawio

    system = platform.system()
    if system == "Darwin":
        mac_path = "/Applications/draw.io.app/Contents/MacOS/draw.io"
        if Path(mac_path).exists():
            return mac_path
    elif system == "Linux":
        for p in ["/usr/bin/drawio", "/snap/bin/drawio", "/usr/local/bin/drawio"]:
            if Path(p).exists():
                return p
    elif system == "Windows":
        prog = Path.home() / "AppData" / "Local" / "draw.io" / "draw.io.exe"
        if prog.exists():
            return str(prog)

    raise FileNotFoundError(
        "draw.io CLI not found. Install it: https://github.com/jgraph/drawio-desktop/releases"
    )


def render_mermaid(mermaid_code: str, output_path: Path, fmt: str = "png",
                   theme: str = "default") -> Path:
    """Render a mermaid diagram to PNG or SVG using mmdc."""
    output_path = output_path.with_suffix(f".{fmt}")

    with tempfile.NamedTemporaryFile(mode="w", suffix=".mmd", delete=False) as f:
        f.write(mermaid_code)
        input_path = f.name

    cmd = [
        "mmdc",
        "-i", input_path,
        "-o", str(output_path),
        "-t", theme,
        "-b", "transparent",
    ]
    if fmt == "svg":
        cmd.extend(["-f", "svg"])

    subprocess.run(cmd, check=True, capture_output=True, text=True)
    Path(input_path).unlink(missing_ok=True)
    return output_path


def render_drawio(drawio_path: Path, output_path: Path, fmt: str = "png") -> Path:
    """Render a draw.io file to PNG or SVG using draw.io CLI."""
    output_path = output_path.with_suffix(f".{fmt}")

    cmd = [
        _find_drawio_cmd(),
        "--export",
        "--format", fmt,
        "--output", str(output_path),
        str(drawio_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    return output_path


def extract_and_render_mermaid(md_content: str, export_dir: Path,
                                theme: str = "default",
                                fmt: str = "png") -> str:
    """Find all mermaid code blocks in markdown, render them, replace with image refs."""
    export_dir.mkdir(parents=True, exist_ok=True)
    pattern = re.compile(r"```mermaid\n(.*?)```", re.DOTALL)
    counter = 0

    def replacer(match):
        nonlocal counter
        counter += 1
        mermaid_code = match.group(1)
        output_name = f"diagram-{counter}"
        output_path = export_dir / output_name
        rendered = render_mermaid(mermaid_code, output_path, fmt=fmt, theme=theme)
        return f"![Diagram {counter}]({rendered})"

    return pattern.sub(replacer, md_content)


def render_drawio_files(drawio_files: list[str], project_dir: Path,
                        export_dir: Path, fmt: str = "png") -> dict[str, Path]:
    """Render all draw.io files listed in frontmatter."""
    export_dir.mkdir(parents=True, exist_ok=True)
    results = {}

    for drawio_file in drawio_files:
        drawio_path = project_dir / "diagrams" / drawio_file
        if not drawio_path.exists():
            print(f"Warning: draw.io file not found: {drawio_path}")
            continue
        output_name = drawio_path.stem
        output_path = export_dir / output_name
        rendered = render_drawio(drawio_path, output_path, fmt=fmt)
        results[drawio_file] = rendered

    return results


def process_diagrams(md_content: str, frontmatter: dict,
                     project_dir: Path,
                     project_name: str | None = None) -> str:
    """Process all diagrams in a document: mermaid blocks + draw.io files."""
    config = load_config(project_name)
    diagrams_config = frontmatter.get("diagrams", {})
    theme = diagrams_config.get("mermaid_theme", config.get("mermaid_theme", "default"))
    fmt = diagrams_config.get("export_format", config.get("default_export_format", "png"))
    export_dir = project_dir / "diagrams" / "exports"

    # Render mermaid blocks inline
    md_content = extract_and_render_mermaid(md_content, export_dir, theme=theme, fmt=fmt)

    # Render draw.io files
    drawio_files = diagrams_config.get("drawio_files", [])
    if drawio_files:
        render_drawio_files(drawio_files, project_dir, export_dir, fmt=fmt)

    return md_content


if __name__ == "__main__":
    import sys
    import frontmatter as fm

    if len(sys.argv) < 2:
        print("Usage: python -m docgen.diagrams <path-to-markdown>")
        sys.exit(1)

    doc_path = Path(sys.argv[1]).resolve()
    post = fm.load(str(doc_path))
    project_dir = doc_path.parent.parent  # docs/ -> project root
    project_name = post.metadata.get("project") or project_dir.name

    processed = process_diagrams(post.content, post.metadata, project_dir, project_name)
    print(f"Diagrams exported to: {project_dir / 'diagrams' / 'exports'}")
