# ViceProbe

ViceProbe is a comprehensive reconnaissance tool designed for pentesters to automate and integrate various techniques for discovering subdomains, web directories, technologies in use, parameters, and Google Dorks. This tool aims to enhance the efficiency and accuracy of security assessments by centralizing the results and providing detailed reports.

## Features

- **Subdomain Enumeration**: Identify subdomains associated with a target domain.
- **Active Subdomain Enumeration**: Validate and find live subdomains.
- **Web Directory Enumeration**: Discover web directories and files on the target server.
- **Href Scraping**: Collect URLs from a web page, including those within scope and miscellaneous.
- **Parameter Enumeration**: Identify URL parameters that may be vulnerable.
- **Technology Enumeration**: Detect technologies and platforms used by the target domain.
- **Google Dork Enumeration**: Perform Google Dork queries to find sensitive information.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/hackervice/viceprobe.git
    cd viceprobe
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the application**:
    ```bash
    python viceprobe.py
    ```

2. **Access the web interface**:
    Open a web browser and navigate to `http://localhost:5000`.

3. **Perform reconnaissance**:
    - Enter the target domain.
    - Select the desired enumeration tools.
    - Click the "Run" button to start the reconnaissance.

4. **View results**:
    - The results will be displayed on the web interface.
    - Export the results to PDF or CSV for detailed reporting.

## Project Structure

