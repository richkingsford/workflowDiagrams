# Product Management Workflow Diagram Generator

A simple tool to generate visual workflow diagrams from JSON data.

## Quick Start

1. **Generate the diagram:**
   ```bash
   python workflow_generator.py
   ```

2. **View the diagram:**
   ```bash
   python view_diagram.py
   ```

3. **Open your browser** to see the visual diagram!

## Files

- `product_management_workflow.json` - The workflow data
- `workflow_generator.py` - Generates PNG, SVG, and DOT files
- `view_diagram.py` - Simple web viewer for the diagram
- `output/` - Generated diagram files

## What You Get

- **PNG image** - For presentations and documents
- **SVG image** - Scalable vector graphics
- **DOT source** - Graphviz source code
- **Web viewer** - Interactive browser view

## The Workflow

This diagram shows a complete Product Management process from initial request to sprint-ready user stories, including decision points and feedback loops.

## Requirements

- Python 3.6+
- graphviz package (`pip install graphviz`)
- Graphviz system package (usually pre-installed)