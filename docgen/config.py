"""Configuration loader and path constants for docgen."""

import json
from pathlib import Path

# Path constants
ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / "docgen.config.json"
TEMPLATES_DIR = ROOT_DIR / "templates"
PARTIALS_DIR = TEMPLATES_DIR / "partials"
STYLES_DIR = ROOT_DIR / "styles"
PROJECTS_DIR = ROOT_DIR / "projects"

PROJECT_CONFIG_NAME = "docgen.config.json"


def load_global_config() -> dict:
    """Load the root-level global configuration."""
    with open(CONFIG_PATH) as f:
        return json.load(f)


def load_project_config(project_name: str) -> dict:
    """Load project-level config if it exists, otherwise empty dict."""
    project_config_path = PROJECTS_DIR / project_name / PROJECT_CONFIG_NAME
    if project_config_path.exists():
        with open(project_config_path) as f:
            return json.load(f)
    return {}


def load_config(project_name: str | None = None) -> dict:
    """Load merged configuration: global defaults overlaid with project overrides.

    If project_name is provided and the project has a docgen.config.json,
    its values take precedence over the global config.
    """
    config = load_global_config()
    if project_name:
        project_config = load_project_config(project_name)
        config.update(project_config)
    return config


def get_project_dir(project_name: str) -> Path:
    """Return the project directory path for a given project name."""
    return PROJECTS_DIR / project_name


def get_project_paths(project_name: str) -> dict[str, Path]:
    """Return all standard paths for a project."""
    base = get_project_dir(project_name)
    return {
        "root": base,
        "docs": base / "docs",
        "diagrams": base / "diagrams",
        "diagram_exports": base / "diagrams" / "exports",
        "output": base / "output",
        "assets": base / "assets",
    }
