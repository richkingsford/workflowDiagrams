#!/usr/bin/env python3
"""
Workflow Diagram Generator

This script reads a JSON workflow definition and generates a visual workflow diagram
using Graphviz. It creates a flowchart showing the steps, decisions, and flow paths.
"""

import json
import os
from graphviz import Digraph


def load_workflow_json(file_path):
    """Load workflow data from JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)


def create_workflow_diagram(workflow_data, output_format='png'):
    """
    Create a workflow diagram from JSON data using Graphviz.
    
    Args:
        workflow_data: Dictionary containing workflow information
        output_format: Output format (png, svg, pdf, etc.)
    
    Returns:
        Graphviz Digraph object
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
                    # Continue to next step (handled above)
                    pass
                elif 'loop back' in success_action.lower():
                    # Extract step number to loop back to
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
                
                # Add retry arrow back to current step
                dot.edge(failure_node_id, node_id, 
                        label='Retry', color='orange', style='dashed')
    
    # Add end node for the last step
    last_step_id = f'step_{steps[-1]["step_id"]}'
    dot.node('end', 'END', shape='ellipse', fillcolor='lightcoral')
    
    # Only add end connection if the last step doesn't loop back
    last_step = steps[-1]
    if 'decision' in last_step and 'loop back' not in last_step['decision'].get('success', '').lower():
        dot.edge(last_step_id, 'end', label='Complete')
    
    return dot


def generate_diagram(json_file, output_dir='output', output_format='png'):
    """
    Generate workflow diagram from JSON file.
    
    Args:
        json_file: Path to JSON workflow file
        output_dir: Directory to save output files
        output_format: Output format (png, svg, pdf, etc.)
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load workflow data
    workflow_data = load_workflow_json(json_file)
    
    # Create diagram
    dot = create_workflow_diagram(workflow_data, output_format)
    
    # Generate output filename
    workflow_name = workflow_data['workflow'].get('title', 'workflow')
    output_file = os.path.join(output_dir, f'{workflow_name.lower()}_workflow')
    
    # Render the diagram
    dot.render(output_file, format=output_format, cleanup=True)
    
    print(f"Workflow diagram generated: {output_file}.{output_format}")
    
    # Also save the DOT source for reference
    with open(f"{output_file}.dot", 'w') as f:
        f.write(dot.source)
    
    return f"{output_file}.{output_format}"


if __name__ == "__main__":
    # Generate diagram from the requirements workflow JSON
    json_file = "requirements_workflow.json"
    
    if os.path.exists(json_file):
        output_file = generate_diagram(json_file)
        print(f"\nWorkflow diagram created successfully!")
        print(f"Output file: {output_file}")
        
        # Also generate SVG for web viewing
        svg_file = generate_diagram(json_file, output_format='svg')
        print(f"SVG version: {svg_file}")
    else:
        print(f"Error: {json_file} not found!")