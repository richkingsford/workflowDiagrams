# Workflow Diagrams

This project converts JSON workflow definitions into visual workflow diagrams using Python and Graphviz.

## Features

- **JSON-based workflow definition**: Define workflows in a structured JSON format
- **Visual diagram generation**: Automatically generate flowcharts from JSON data
- **Multiple output formats**: PNG, SVG, and DOT source files
- **Web interface**: Simple web server to view and download diagrams
- **Decision handling**: Support for success/failure paths and loops

## Files

- `requirements_workflow.json` - JSON definition of the "Requirements" workflow
- `workflow_generator.py` - Python script to generate diagrams from JSON
- `server.py` - Web server to view diagrams in browser
- `output/` - Directory containing generated diagram files

## Requirements

- Python 3.6+
- Graphviz library (`pip install graphviz`)
- Graphviz system package (`apt-get install graphviz` on Ubuntu/Debian)

## Usage

### Generate Diagram

```bash
python workflow_generator.py
```

This will read `requirements_workflow.json` and generate:
- `output/requirements_workflow.png` - PNG image
- `output/requirements_workflow.svg` - SVG vector image  
- `output/requirements_workflow.dot` - Graphviz DOT source

### View in Browser

```bash
python server.py
```

Then open your browser to view the interactive diagram with download links.

## JSON Workflow Format

```json
{
  "workflow": {
    "name": "Workflow Name",
    "title": "Category Title", 
    "steps": [
      {
        "step_id": 1,
        "name": "Step Name",
        "action": "Optional action description",
        "decision": {
          "success": "What happens on success",
          "failure": "What happens on failure"
        }
      }
    ]
  }
}
```

## Current Workflow: Wall-Crawling Concrete Smoothing Robot

The included workflow demonstrates a robotic process with:

1. **Epic Validation** - Decision point for project viability
2. **Grip Dry Concrete** - Robot positioning and grip activation
3. **Position Near Wet Concrete** - Movement to work area
4. **Smooth Concrete** - Primary work operation
5. **Advance Forward** - Movement with loop back to step 2

Each step includes success/failure paths with appropriate retry mechanisms and error handling.

## Extending

To create additional workflows:

1. Create a new JSON file following the format
2. Modify `workflow_generator.py` to point to your JSON file
3. Run the generator to create new diagrams

The system supports:
- Linear workflows
- Decision branches
- Loop-back mechanisms  
- Error handling paths
- Custom styling and colors