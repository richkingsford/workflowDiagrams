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
- `product_management_workflow.json` - JSON definition of the "Product Management Process" workflow
- `workflow_generator.py` - Original Python script to generate diagrams from JSON
- `enhanced_workflow_generator.py` - Enhanced script supporting multiple JSON formats
- `server.py` - Web server to view diagrams in browser
- `output/` - Directory containing generated diagram files

## Requirements

- Python 3.6+
- Graphviz library (`pip install graphviz`)
- Graphviz system package (`apt-get install graphviz` on Ubuntu/Debian)

## Usage

### Generate Diagrams

For the original Requirements workflow:
```bash
python workflow_generator.py
```

For both workflows (recommended):
```bash
python enhanced_workflow_generator.py
```

This will generate for each workflow:
- PNG image files
- SVG vector image files
- Graphviz DOT source files

### View in Browser

```bash
python server.py
```

Then open your browser to view the interactive diagram with download links.

## JSON Workflow Formats

The tool supports two JSON formats:

### Format 1: Steps-based (Requirements workflow)
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

### Format 2: Array-based (Product Management workflow)
```json
{
  "workflow": [
    {
      "id": 1,
      "type": "start|process|decision|end",
      "text": "Step description",
      "next": [2] // or for decisions: [{"condition": "Yes", "to": 3}, {"condition": "No", "to": 4}]
    }
  ]
}
```

## Included Workflows

### 1. Requirements Workflow: Wall-Crawling Concrete Smoothing Robot
This workflow demonstrates a robotic process with:

1. **Epic Validation** - Decision point for project viability
2. **Grip Dry Concrete** - Robot positioning and grip activation
3. **Position Near Wet Concrete** - Movement to work area
4. **Smooth Concrete** - Primary work operation
5. **Advance Forward** - Movement with loop back to step 2

Each step includes success/failure paths with appropriate retry mechanisms and error handling.

### 2. Product Management Process Workflow
This workflow demonstrates a software development process from request to sprint:

1. **Request Made** - Starting point
2. **Request to Product Manager?** - Decision point for routing
3. **Create Epic** or **Redirect to Product Manager** - Based on decision
4. **Epic clear and viable?** - Validation decision with refinement loop
5. **Product Managers Refine and Prioritize Epics** - Backlog management
6. **Engineering Creates Linked User Stories** - Development preparation
7. **User Stories Go into Upcoming Sprints** - Sprint planning
8. **Sprint Ready** - End state

## Extending

To create additional workflows:

1. Create a new JSON file following either format
2. Add the file to `enhanced_workflow_generator.py` in the `json_files` list
3. Run the enhanced generator to create new diagrams

The system supports:
- Linear workflows
- Decision branches with Yes/No conditions
- Loop-back mechanisms  
- Error handling paths
- Multiple workflow types (start, process, decision, end)
- Custom styling and colors