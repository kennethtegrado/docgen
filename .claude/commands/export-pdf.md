You are exporting a markdown document to PDF using the docgen export pipeline.

**Document path:** $ARGUMENTS

## Steps

1. Verify the document exists at the given path. If a project name is given instead of a full path, look in `projects/<name>/docs/` for the markdown file.

2. Run the export:
```
source .venv/bin/activate && python -m docgen.export "$ARGUMENTS"
```

3. Report the output PDF location and file size.

4. If there are errors:
   - **Mermaid errors**: Check that `mmdc` is installed (`npm list -g @mermaid-js/mermaid-cli`)
   - **WeasyPrint errors**: Check that WeasyPrint is installed in the venv
   - **Pandoc errors**: Check that pandoc is installed (`pandoc --version`)
   - **CSS errors**: Verify `styles/print.css` exists

5. Suggest opening the PDF: `open <output-path>`
