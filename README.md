# WebsiteScreenshotter
## Description
The Website Screenshotter is a Python application designed to screenshot web pages. It reads a list of hostnames and ports from a JSON and uses Selenium WebDriver to take screenshots. 
This is helpful in large pentests to look through hundreds or thousands of hostnames and ports that for example nmap had found previously. The screenshots help to find vulnerable targets more easily.

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
    "hostname": "example.com",
    "ports": {
      "80": "http",
      "443": "https"
    }
  },
  "192.168.1.2": {
    "hostname": "anotherexample.com",
    "ports": {
      "8080": "http",
      "8443": "https"
    }
  }
}

# Test
