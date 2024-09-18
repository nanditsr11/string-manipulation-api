from http.server import BaseHTTPRequestHandler, HTTPServer  # Import the HTTP modules
import json  # For sending JSON responses
from urllib.parse import urlparse, parse_qs  # For parsing query parameters

class StringManipulationAPI(BaseHTTPRequestHandler):

    def do_GET(self):
        # Parse query parameters from the URL
        query_components = parse_qs(urlparse(self.path).query)
        text = query_components.get("text", [""])[0]  # Get the 'text' parameter, default is empty
        operation = query_components.get("operation", [""])[0]  # Get the 'operation' parameter

        # Perform the requested string operation
        if operation == "reverse":
            result = text[::-1]  # Reverse the string
        elif operation == "uppercase":
            result = text.upper()  # Convert string to uppercase
        elif operation == "palindrome":
            result = str(text == text[::-1])  # Check if the string is a palindrome
        else:
            result = "Invalid operation."  # Handle invalid operations

        # Send HTTP headers
        self.send_response(200)  # HTTP 200 OK
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Prepare and send the JSON response
        response_data = {"text": text, "operation": operation, "result": result}
        self.wfile.write(json.dumps(response_data).encode('utf-8'))  # Send response as JSON

# Function to run the server
def run(server_class=HTTPServer, handler_class=StringManipulationAPI, port=8080):
    server_address = ('', port)  # Set up the server to listen on all interfaces
    httpd = server_class(server_address, handler_class)  # Instantiate the HTTP server
    print(f'Starting String Manipulation API on port {port}...')
    httpd.serve_forever()  # Keep the server running indefinitely

# Entry point for the script
if __name__ == "__main__":
    run()  # Run the server
