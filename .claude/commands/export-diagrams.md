You are exporting all diagrams from a markdown document using the docgen diagram pipeline.

**Document path:** $ARGUMENTS

## Steps

1. Verify the document exists at the given path. If a project name is given instead of a full path, look in `projects/<name>/docs/` for the markdown file.

2. Run the diagram export:
```
source .venv/bin/activate && python -m docgen.diagrams "$ARGUMENTS"
```

3. List all exported diagram files in the project's `diagrams/exports/` directory.

4. Report what was generated (mermaid diagrams, draw.io exports) and their locations.

5. If there are errors:
   - **Mermaid errors**: Check that `mmdc` is installed (`npm list -g @mermaid-js/mermaid-cli`)
   - **Draw.io errors**: Check that draw.io is installed (`ls /Applications/draw.io.app`)
   - Suggest installing missing dependencies
