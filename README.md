# Based HTTP Server (Python)

A minimalist HTTP/1.1 server written from scratch in Python using raw TCP sockets — built as part of the Codecrafters challenge.

## Features
- Accepts TCP connections on port 4221
- Parses raw HTTP GET requests
- Handles `/`, `/echo/<msg>`, and `/user-agent`
- Returns appropriate HTTP response codes
- Supports concurrent connections using threads

## Learning Highlights
- Low-level socket programming
- Manual HTTP parsing
- Working with raw bytes and string decoding
- Implementing concurrency with Python's threading module
