#!/usr/bin/env python3
"""
Enhanced Workflow Diagram Generator

This script reads JSON workflow definitions in multiple formats and generates 
visual workflow diagrams using Graphviz.
"""

import json
import os
from graphviz import Digraph


def load_workflow_json(file_path):
    """Load workflow data from JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)


def detect_workflow_format(workflow_data):
    """Detect the format of the workflow JSON."""
    if 'workflow' in workflow_data:
        if isinstance(workflow_data['workflow'], list):
            return 'array_format'  # New format with array of steps
        elif isinstance(workflow_data['workflow'], dict) and 'steps' in workflow_data['workflow']:
            return 'steps_format'  # Original format with steps array
    return 'unknown'


def create_workflow_diagram_array_format(workflow_data, title="Workflow", output_format='png'):
    """
    Create a workflow diagram from array format JSON data.
    
    Args:
        workflow_data: Dictionary containing workflow array
        title: Title for the diagram
        output_format: Output format (png, svg, pdf, etc.)
    
    Returns:
        Graphviz Digraph object
    """
    workflow_steps = workflow_data['workflow']
    
    # Create a new directed graph
    dot = Digraph(comment=title)
    dot.attr(rankdir='TB', size='12,16')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial')
    dot.attr('edge', fontname='Arial')
    
    # Add title
    dot.node('title', title, shape='plaintext', fontsize='16', fontweight='bold')
    
    # Create a lookup dictionary for steps
    steps_dict = {step['id']: step for step in workflow_steps}
    
    # Process each step
    for step in workflow_steps:
        step_id = str(step['id'])
        step_type = step['type']
        step_text = step['text']
        
        # Determine node properties based on type
        if step_type == 'start':
            fillcolor = 'lightgreen'
            shape = 'ellipse'
        elif step_type == 'end':
            fillcolor = 'lightcoral'
            shape = 'ellipse'
        elif step_type == 'decision':
            fillcolor = 'lightblue'
            shape = 'diamond'
        elif step_type == 'process':
            fillcolor = 'lightyellow'
            shape = 'box'
        else:
            fillcolor = 'lightgray'
            shape = 'box'
        
        # Add the node
        dot.node(step_id, step_text, shape=shape, fillcolor=fillcolor)
        
        # Connect title to start node
        if step_type == 'start':
            dot.edge('title', step_id, style='invis')
        
        # Add edges based on next connections
        if 'next' in step and step['next']:
            if step_type == 'decision':
                # Handle decision nodes with conditions
                for next_item in step['next']:
                    if isinstance(next_item, dict) and 'condition' in next_item:
                        condition = next_item['condition']
                        next_id = str(next_item['to'])
                        
                        # Color code the edges
                        if condition.lower() == 'yes':
                            color = 'green'
                        elif condition.lower() == 'no':
                            color = 'red'
                        else:
                            color = 'black'
                        
                        dot.edge(step_id, next_id, label=condition, color=color)
                    else:
                        # Simple numeric next reference
                        next_id = str(next_item)
                        dot.edge(step_id, next_id)
            else:
                # Handle regular process nodes
                for next_id in step['next']:
                    next_id_str = str(next_id)
                    
                    # Check if this creates a loop back
                    if int(next_id) < step['id']:
                        dot.edge(step_id, next_id_str, 
                               label='Loop back', 
                               color='orange', style='dashed')
                    else:
                        dot.edge(step_id, next_id_str)
    
    return dot


def create_workflow_diagram_steps_format(workflow_data, output_format='png'):
    """
    Create a workflow diagram from steps format JSON data (original format).
    """
    workflow = workflow_data['workflow']
    title = workflow.get('title', 'Workflow')
    name = workflow['name']
    steps = workflow['steps']
    
    # Create a new directed graph
    dot = Digraph(comment=f'{title}: {name}')
    dot.attr(rankdir='TB', size='12,16')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial')
    dot.attr('edge', fontname='Arial')
    
    # Add title
    dot.node('title', f'{title}\n{name}', 
             shape='plaintext', fontsize='16', fontweight='bold')
    
    # Add start node
    dot.node('start', 'START', shape='ellipse', fillcolor='lightgreen')
    
    # Connect title to start
    dot.edge('title', 'start', style='invis')
    
    # Process each step
    for i, step in enumerate(steps):
        step_id = step['step_id']
        step_name = step['name']
        
        # Create main step node
        node_id = f'step_{step_id}'
        
        # Different colors for different types of steps
        if 'decision' in step_name.lower() or '?' in step_name:
            fillcolor = 'lightblue'
            shape = 'diamond'
        else:
            fillcolor = 'lightyellow'
            shape = 'box'
        
        # Add action text if present
        label = step_name
        if 'action' in step:
            label += f'\n\n{step["action"]}'
        
        dot.node(node_id, label, shape=shape, fillcolor=fillcolor)
        
        # Connect from start or previous step
        if i == 0:
            dot.edge('start', node_id)
        else:
            prev_step_id = f'step_{steps[i-1]["step_id"]}'
            dot.edge(prev_step_id, node_id, label='Success')
        
        # Handle decisions
        if 'decision' in step:
            decision = step['decision']
            
            # Success path
            if 'success' in decision:
                success_action = decision['success']
                if 'next step' in success_action.lower():
                    pass
                elif 'loop back' in success_action.lower():
                    import re
                    match = re.search(r'step (\d+)', success_action.lower())
                    if match:
                        loop_step = int(match.group(1))
                        loop_node_id = f'step_{loop_step}'
                        dot.edge(node_id, loop_node_id, 
                               label='Success\n(Loop back)', 
                               color='green', style='dashed')
            
            # Failure path
            if 'failure' in decision:
                failure_action = decision['failure']
                failure_node_id = f'failure_{step_id}'
                
                dot.node(failure_node_id, failure_action, 
                        shape='box', fillcolor='lightcoral')
                dot.edge(node_id, failure_node_id, 
                        label='Failure', color='red')
                
                dot.edge(failure_node_id, node_id, 
                        label='Retry', color='orange', style='dashed')
    
    # Add end node for the last step
    last_step_id = f'step_{steps[-1]["step_id"]}'
    dot.node('end', 'END', shape='ellipse', fillcolor='lightcoral')
    
    last_step = steps[-1]
    if 'decision' in last_step and 'loop back' not in last_step['decision'].get('success', '').lower():
        dot.edge(last_step_id, 'end', label='Complete')
    
    return dot


def generate_diagram(json_file, output_dir='output', output_format='png', title=None):
    """
    Generate workflow diagram from JSON file.
    
    Args:
        json_file: Path to JSON workflow file
        output_dir: Directory to save output files
        output_format: Output format (png, svg, pdf, etc.)
        title: Optional title override
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load workflow data
    workflow_data = load_workflow_json(json_file)
    
    # Detect format and create appropriate diagram
    format_type = detect_workflow_format(workflow_data)
    
    if format_type == 'array_format':
        if title is None:
            title = os.path.splitext(os.path.basename(json_file))[0].replace('_', ' ').title()
        dot = create_workflow_diagram_array_format(workflow_data, title, output_format)
        workflow_name = title.lower().replace(' ', '_')
    elif format_type == 'steps_format':
        dot = create_workflow_diagram_steps_format(workflow_data, output_format)
        workflow_name = workflow_data['workflow'].get('title', 'workflow').lower()
    else:
        raise ValueError(f"Unknown workflow format in {json_file}")
    
    # Generate output filename
    output_file = os.path.join(output_dir, f'{workflow_name}_workflow')
    
    # Render the diagram
    dot.render(output_file, format=output_format, cleanup=True)
    
    print(f"Workflow diagram generated: {output_file}.{output_format}")
    
    # Also save the DOT source for reference
    with open(f"{output_file}.dot", 'w') as f:
        f.write(dot.source)
    
    return f"{output_file}.{output_format}"


if __name__ == "__main__":
    # Generate diagrams for all JSON files
    json_files = [
        ("requirements_workflow.json", "Requirements"),
        ("product_management_workflow.json", "Product Management Process")
    ]
    
    for json_file, title in json_files:
        if os.path.exists(json_file):
            print(f"\nGenerating diagram for {json_file}...")
            
            # Generate PNG
            png_file = generate_diagram(json_file, title=title, output_format='png')
            print(f"PNG: {png_file}")
            
            # Generate SVG
            svg_file = generate_diagram(json_file, title=title, output_format='svg')
            print(f"SVG: {svg_file}")
        else:
            print(f"Warning: {json_file} not found!")