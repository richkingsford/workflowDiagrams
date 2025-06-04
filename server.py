#!/usr/bin/env python3
"""
Simple web server to view workflow diagrams
"""

import http.server
import socketserver
import os
import webbrowser
from urllib.parse import unquote

class WorkflowHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="/workspace/workflowDiagrams", **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        # Allow iframe embedding
        self.send_header('X-Frame-Options', 'ALLOWALL')
        super().end_headers()

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Workflow Diagrams</title>
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
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .workflow-section {
            margin: 40px 0;
            padding: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
        }
        .diagram-container {
            text-align: center;
            margin: 20px 0;
        }
        .diagram-container img {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .download-links {
            text-align: center;
            margin: 20px 0;
        }
        .download-links a {
            display: inline-block;
            margin: 0 10px;
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 4px;
        }
        .download-links a:hover {
            background-color: #0056b3;
        }
        .json-container {
            margin: 20px 0;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 4px;
            border-left: 4px solid #007bff;
        }
        pre {
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
            max-height: 400px;
            overflow-y: auto;
        }
        .nav-links {
            text-align: center;
            margin: 20px 0;
        }
        .nav-links a {
            display: inline-block;
            margin: 0 15px;
            padding: 8px 16px;
            background-color: #28a745;
            color: white;
            text-decoration: none;
            border-radius: 4px;
        }
        .nav-links a:hover {
            background-color: #218838;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Workflow Diagrams</h1>
        
        <div class="nav-links">
            <a href="#requirements">Requirements Workflow</a>
            <a href="#product-management">Product Management Process</a>
        </div>
        
        <div class="workflow-section" id="requirements">
            <h2>Requirements Workflow</h2>
            <h3>Wall-Crawling Concrete Smoothing Robot</h3>
            
            <div class="diagram-container">
                <img src="/output/requirements_workflow.png" alt="Requirements Workflow Diagram">
            </div>
            
            <div class="download-links">
                <a href="/output/requirements_workflow.png" download>Download PNG</a>
                <a href="/output/requirements_workflow.svg" download>Download SVG</a>
                <a href="/output/requirements_workflow.dot" download>Download DOT Source</a>
                <a href="/requirements_workflow.json" download>Download JSON</a>
            </div>
            
            <div class="json-container">
                <h4>Source JSON Data</h4>
                <pre id="requirements-json-content">Loading...</pre>
            </div>
        </div>
        
        <div class="workflow-section" id="product-management">
            <h2>Product Management Process</h2>
            <h3>Request to Sprint Ready Workflow</h3>
            
            <div class="diagram-container">
                <img src="/output/product_management_process_workflow.png" alt="Product Management Process Workflow Diagram">
            </div>
            
            <div class="download-links">
                <a href="/output/product_management_process_workflow.png" download>Download PNG</a>
                <a href="/output/product_management_process_workflow.svg" download>Download SVG</a>
                <a href="/output/product_management_process_workflow.dot" download>Download DOT Source</a>
                <a href="/product_management_workflow.json" download>Download JSON</a>
            </div>
            
            <div class="json-container">
                <h4>Source JSON Data</h4>
                <pre id="product-json-content">Loading...</pre>
            </div>
        </div>
    </div>
    
    <script>
        // Load and display Requirements JSON content
        fetch('/requirements_workflow.json')
            .then(response => response.json())
            .then(data => {
                document.getElementById('requirements-json-content').textContent = JSON.stringify(data, null, 2);
            })
            .catch(error => {
                document.getElementById('requirements-json-content').textContent = 'Error loading JSON: ' + error;
            });
        
        // Load and display Product Management JSON content
        fetch('/product_management_workflow.json')
            .then(response => response.json())
            .then(data => {
                document.getElementById('product-json-content').textContent = JSON.stringify(data, null, 2);
            })
            .catch(error => {
                document.getElementById('product-json-content').textContent = 'Error loading JSON: ' + error;
            });
    </script>
</body>
</html>
            """
            self.wfile.write(html_content.encode())
        else:
            super().do_GET()

if __name__ == "__main__":
    PORT = 12000
    
    with socketserver.TCPServer(("0.0.0.0", PORT), WorkflowHandler) as httpd:
        print(f"Server running at http://0.0.0.0:{PORT}")
        print(f"Access the workflow diagram at: https://work-1-yihgbsbvzvzksljb.prod-runtime.all-hands.dev")
        print("Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")