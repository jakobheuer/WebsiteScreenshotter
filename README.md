# WebsiteScreenshotter
## Description
A multithreaded website screenshotter. Reads a list of hostnames and ports from a JSON and takes screenshots. 
Helps in finding vulnerable looking targets in pentests with large amounts of webpages previously found by nmap or other tools.

## Requirements
- Python 3.6 or higher
- Selenium WebDriver
- ChromeDriver
- Tkinter

Ensure that ChromeDriver (or the driver for your chosen browser) is installed and its path is correctly set up in your system's PATH environment variable.

## JSON Structure

The program expects a JSON file named `scan.json` with the following structure:

```json
{
  "192.168.1.1": {
    "hostname": "jakobheuer.com",
    "ports": {
      "80": "http",
      "443": "https"
    }
  },
  "192.168.1.2": {
    "hostname": "example.com",
    "ports": {
      "8080": "http",
      "8443": "https"
    }
  }
}
```

# How to Run
1. Place your 'scan.json' in the same directory as the script.
2. Run the script:
```
python3 Screenshot.py
```
# What it looks like
![Screenshotter](https://github.com/jakobheuer/WebsiteScreenshotter/assets/45359957/07d62636-52fc-4ce9-bb3d-e097891525d3)

