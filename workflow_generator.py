#!/usr/bin/env python3
"""
Simple Workflow Diagram Generator
Generates visual diagrams from product_management_workflow.json
"""

import json
import graphviz
import os

def generate_workflow_diagram():
    """Generate workflow diagram from product_management_workflow.json"""
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dir, 'product_management_workflow.json')
    
    # Load the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    workflow = data['workflow']
    
    # Create a new directed graph
    dot = graphviz.Digraph(comment='Product Management Process')
    dot.attr(rankdir='TB', size='12,16')
    dot.attr('node', fontname='Arial', fontsize='10')
    dot.attr('edge', fontname='Arial', fontsize='9')
    
    # Add nodes with different styles based on type
    for step in workflow:
        step_id = str(step['id'])
        text = step['text']
        step_type = step['type']
        
        if step_type == 'start':
            dot.node(step_id, text, shape='ellipse', style='filled', fillcolor='lightgreen')
        elif step_type == 'end':
            dot.node(step_id, text, shape='ellipse', style='filled', fillcolor='lightcoral')
        elif step_type == 'decision':
            dot.node(step_id, text, shape='diamond', style='filled', fillcolor='lightyellow')
        else:  # process
            dot.node(step_id, text, shape='box', style='filled', fillcolor='lightblue')
    
    # Add edges
    for step in workflow:
        step_id = str(step['id'])
        
        if step['next']:
            if step['type'] == 'decision':
                # Handle decision nodes with conditions
                for next_item in step['next']:
                    if isinstance(next_item, dict):
                        condition = next_item['condition']
                        to_id = str(next_item['to'])
                        dot.edge(step_id, to_id, label=condition)
                    else:
                        # Simple next without condition
                        dot.edge(step_id, str(next_item))
            else:
                # Handle regular process nodes
                for next_id in step['next']:
                    dot.edge(step_id, str(next_id))
    
    # Create output directory relative to script location
    output_dir = os.path.join(script_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate the diagram
    output_file = os.path.join(output_dir, 'product_management_workflow')
    
    # Render as PNG
    dot.render(output_file, format='png', cleanup=True)
    print(f"✅ PNG diagram generated: {output_file}.png")
    
    # Render as SVG
    dot.render(output_file, format='svg', cleanup=True)
    print(f"✅ SVG diagram generated: {output_file}.svg")
    
    # Save DOT source
    with open(f"{output_file}.dot", 'w') as f:
        f.write(dot.source)
    print(f"✅ DOT source saved: {output_file}.dot")
    
    return f"{output_file}.png"

if __name__ == "__main__":
    try:
        png_file = generate_workflow_diagram()
        print(f"\n🎉 Workflow diagram successfully generated!")
        print(f"📁 Check the 'output' folder for your files")
        print(f"🖼️  Main diagram: {png_file}")
        
    except FileNotFoundError:
        print("❌ Error: product_management_workflow.json not found!")
        print("Make sure the JSON file is in the same directory as this script.")
    except Exception as e:
        print(f"❌ Error generating diagram: {e}")