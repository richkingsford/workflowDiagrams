#!/usr/bin/env python3
"""
Simple Web Viewer for Workflow Diagram
Run this to view your generated diagram in a web browser
"""

import http.server
import socketserver
import webbrowser
import os
import threading
import time

def create_html():
    """Create a simple HTML page to display the diagram"""
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Product Management Workflow</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .diagram {
            text-align: center;
            margin: 20px 0;
        }
        .diagram img {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .downloads {
            text-align: center;
            margin: 20px 0;
        }
        .downloads a {
            display: inline-block;
            margin: 5px 10px;
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        .downloads a:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Product Management Process Workflow</h1>
        
        <div class="diagram">
            <img src="output/product_management_workflow.png" alt="Product Management Workflow Diagram">
        </div>
        
        <div class="downloads">
            <a href="output/product_management_workflow.png" download>Download PNG</a>
            <a href="output/product_management_workflow.svg" download>Download SVG</a>
            <a href="output/product_management_workflow.dot" download>Download DOT</a>
            <a href="product_management_workflow.json" download>Download JSON</a>
        </div>
    </div>
</body>
</html>
"""
    with open('index.html', 'w') as f:
        f.write(html_content)

def start_server():
    """Start a simple HTTP server"""
    PORT = 12000
    
    class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', '*')
            super().end_headers()
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🌐 Server running at: https://work-1-yihgbsbvzvzksljb.prod-runtime.all-hands.dev")
        print(f"📱 Local server: http://localhost:{PORT}")
        print("🔄 Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped")

if __name__ == "__main__":
    # Check if diagram exists
    if not os.path.exists('output/product_management_workflow.png'):
        print("❌ No diagram found! Run workflow_generator.py first.")
        exit(1)
    
    # Create HTML file
    create_html()
    print("📄 Created index.html")
    
    # Start server
    start_server()