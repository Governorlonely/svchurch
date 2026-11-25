"""Build the same offline-ready site for the root preview and existing links."""
import base64
import re
from pathlib import Path

site = Path(__file__).resolve().parent
workspace = site.parent
html = (site / 'shell.html').read_text(encoding='utf-8')
css = (site / 'style.css').read_text(encoding='utf-8')
js = (site / 'app.js').read_text(encoding='utf-8')
html, styles_found = re.subn(r'<link rel="stylesheet" href="style\.css\?v=[^"]*">', lambda _: '<style>' + css + '</style>', html)
html, script_found = re.subn(r'<script src="app\.js\?v=[^"]*"></script>', lambda _: '<script>' + js + '</script>', html)
if (styles_found, script_found) != (1, 1):
    raise ValueError('Expected one stylesheet and one app script in shell.html')
assets = [
    ('logo.png', 'image/png'),
    ('pastors.png', 'image/png'),
    ('fonts/ActayWide-Bold.otf', 'font/otf'),
    ('fonts/helvetica_boldcyrusbyme.otf', 'font/otf'),
]
for name, mime in assets:
    data = (site / 'assets' / name).read_bytes()
    data_url = 'data:' + mime + ';base64,' + base64.b64encode(data).decode('ascii')
    html = html.replace('assets/' + name, data_url)

# One current standalone deliverable.
output = site / 'index.html'
output.write_text(html, encoding='utf-8')
print(f'Built {output.name} ({len(html):,} characters).')
