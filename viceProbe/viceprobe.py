import os
from flask import Flask, render_template, request, redirect, url_for, send_file
import subdomain_enum
import active_enum
import webfolder_enum
import href_scraper
import parameter_enum
import tech_enum
import gd_enum  # Import the gd_enum module
import pandas as pd
import shutil
import atexit
from io import BytesIO
from weasyprint import HTML

app = Flask(__name__)

def clear_temp_folder():
    temp_folder = 'temp'
    for filename in os.listdir(temp_folder):
        file_path = os.path.join(temp_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove arquivos e links simbólicos
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove diretórios
        except Exception as e:
            print(f'Falha ao apagar {file_path}. Razão: {e}')

# Registrar a função clear_temp_folder para ser executada ao sair
atexit.register(clear_temp_folder)

@app.route('/')
def index():
    subdomain_results = ''
    if os.path.exists('temp/assetfinder_results.txt'):
        with open('temp/assetfinder_results.txt', 'r') as file:
            subdomain_results = file.read()

    active_subdomain_results = ''
    if os.path.exists('temp/active_subdomains_clean.txt'):
        with open('temp/active_subdomains_clean.txt', 'r') as file:
            active_subdomain_results = file.read()

    webfolder_results = ''
    if os.path.exists('temp/webfolder_results.txt'):
        with open('temp/webfolder_results.txt', 'r') as file:
            webfolder_results = file.read()

    href_inside_scope_results = ''
    if os.path.exists('temp/href_inside_scope_results.txt'):
        with open('temp/href_inside_scope_results.txt', 'r') as file:
            href_inside_scope_results = file.read()

    href_miscellaneous_results = ''
    if os.path.exists('temp/href_miscellaneous_results.txt'):
        with open('temp/href_miscellaneous_results.txt', 'r') as file:
            href_miscellaneous_results = file.read()

    parameter_results = ''
    if os.path.exists('temp/parameter_enum_results.txt'):
        with open('temp/parameter_enum_results.txt', 'r') as file:
            parameter_results = file.read()

    tech_results = ''
    if os.path.exists('temp/tech_enum_results.txt'):
        with open('temp/tech_enum_results.txt', 'r') as file:
            tech_results = file.read()

    gd_results = ''
    if os.path.exists('temp/gd_enum_results.txt'):
        with open('temp/gd_enum_results.txt', 'r') as file:
            gd_results = file.read()

    return render_template('index.html',
                           subdomain_results=subdomain_results,
                           active_subdomain_results=active_subdomain_results,
                           webfolder_results=webfolder_results,
                           href_inside_scope_results=href_inside_scope_results,
                           href_miscellaneous_results=href_miscellaneous_results,
                           parameter_results=parameter_results,
                           tech_results=tech_results,
                           gd_results=gd_results)  # Add gd_results to the template

@app.route('/run_enum', methods=['POST'])
def run_enum():
    domain = request.form['domain']
    selected_tools = request.form.getlist('tools')

    if domain:
        if 'subdomain_enum' in selected_tools:
            subdomain_enum.assetfinder_subdomains(domain)
        if 'active_subdomain_enum' in selected_tools:
            active_enum.active_subdomain_enum(domain)
        if 'webfolder_enum' in selected_tools:
            webfolder_enum.webfolder_enum(domain)
        if 'href_enum' in selected_tools:
            href_scraper.scrape_hrefs(domain)
        if 'parameter_enum' in selected_tools:
            parameter_enum.parameter_enum(domain)
        if 'tech_enum' in selected_tools:
            tech_enum.enumerate_tech(domain)
        if 'gd_enum' in selected_tools:  # Add Google Dork enumeration
            gd_enum.enumerate_gd(domain)

        return redirect(url_for('index'))

    return redirect(url_for('index'))

@app.route('/export/pdf')
def export_pdf():
    # Data to export
    data = {
        'Subdomain Enumeration Results': '',
        'Active Subdomain Enumeration Results': '',
        'Web Folder Enumeration Results': '',
        'URLs Inside Scope Results': '',
        'Miscellaneous URLs Results': '',
        'Parameter Enumeration Results': '',
        'Technology Enumeration Results': '',
        'Google Dork Enumeration Results': ''
    }

    # Read data from files
    file_paths = {
        'Subdomain Enumeration Results': 'temp/assetfinder_results.txt',
        'Active Subdomain Enumeration Results': 'temp/active_subdomains_clean.txt',
        'Web Folder Enumeration Results': 'temp/webfolder_results.txt',
        'URLs Inside Scope Results': 'temp/href_inside_scope_results.txt',
        'Miscellaneous URLs Results': 'temp/href_miscellaneous_results.txt',
        'Parameter Enumeration Results': 'temp/parameter_enum_results.txt',
        'Technology Enumeration Results': 'temp/tech_enum_results.txt',
        'Google Dork Enumeration Results': 'temp/gd_enum_results.txt'
    }

    for title, path in file_paths.items():
        if os.path.exists(path):
            with open(path, 'r') as file:
                data[title] = file.read()

    # Generate HTML
    html_content = render_template('pdf_template.html', data=data)

    # Convert HTML to PDF
    pdf = HTML(string=html_content).write_pdf()

    return send_file(BytesIO(pdf), download_name='reconnaissance_results.pdf', as_attachment=True)

@app.route('/export/csv')
def export_csv():
    # Data to export
    data = {
        'Subdomain Enumeration Results': [],
        'Active Subdomain Enumeration Results': [],
        'Web Folder Enumeration Results': [],
        'URLs Inside Scope Results': [],
        'Miscellaneous URLs Results': [],
        'Parameter Enumeration Results': [],
        'Technology Enumeration Results': [],
        'Google Dork Enumeration Results': []
    }

    # Read data from files
    file_paths = {
        'Subdomain Enumeration Results': 'temp/assetfinder_results.txt',
        'Active Subdomain Enumeration Results': 'temp/active_subdomains_clean.txt',
        'Web Folder Enumeration Results': 'temp/webfolder_results.txt',
        'URLs Inside Scope Results': 'temp/href_inside_scope_results.txt',
        'Miscellaneous URLs Results': 'temp/href_miscellaneous_results.txt',
        'Parameter Enumeration Results': 'temp/parameter_enum_results.txt',
        'Technology Enumeration Results': 'temp/tech_enum_results.txt',
        'Google Dork Enumeration Results': 'temp/gd_enum_results.txt'
    }

    for title, path in file_paths.items():
        if os.path.exists(path):
            with open(path, 'r') as file:
                data[title] = file.readlines()

    # Convert to DataFrame
    df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data.items()]))

    # Save to CSV in memory
    csv = df.to_csv(index=False)
    return send_file(BytesIO(csv.encode()), download_name='reconnaissance_results.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
