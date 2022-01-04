# Urlscan Report Generator

This simple Python 3.10 CLI project was created in order to simulate an automated process of scanning sites for malicious content using the [UrlScan.io](http://www.urlscan.io) API.

This project was created with the "free" version of the API, which is generously offered to the public, but as such it does not take advantage of features available to "pro" users.

## Requirements

`Urlscan Report Generator` requires that Python 3.10 (or greater) be installed, as well as a [UrlScan.io](http://www.urlscanio) API Key.

## Installation

Clone the `UrlScan Report Generator` project.

Using Python 3.10 or greater, create a local virtual environment in the source folder by typing:
`python -m venv .venv`

Install required packages using:
`pip install -r requirements.txt`

In the `env.py` file, make sure to set the `API_KEY` value to your UrlScan.io API Key. If you do not have one head over to the [UrlScan.io](http://urlscan.io) website, and register to get your personal API key.

## Usage/Examples

Run the program from your favorite CLI.

```
 python3.10 urlscan-report-generator
```

Upon running the program you will be prompted for two inputs.
The first of which is the url to be scanned, the second of which is the desired visibility level. See [the API documentation here](https://urlscan.io/docs/api/), for more information.

NOTE: By default, the visibility value is set to `unlisted`, and will override the value set in your personal API settings.

Reports are generated in the `/reports/` folder according to uuid. Similarly, screenshots are saved in the `/screenshots/` folder according to uuid.
Previous scans of the same websites are overwritten by newer ones, so if you want to keep the report/screenshot - you will want to make a copy of the files before repeating the scan.
