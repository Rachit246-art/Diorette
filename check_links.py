import os
import re

def check_links():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    broken_links = []
    
    # Get all project files for case-sensitive matching
    all_files = {}
    for root, dirs, files in os.walk('.'):
        for f in files:
            full_path = os.path.join(root, f).replace('\\', '/')
            # Remove leading ./
            if full_path.startswith('./'):
                full_path = full_path[2:]
            all_files[full_path.lower()] = full_path

    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Find src and href
            links = re.findall(r'(?:src|href)="([^"#?]+)"', content)
            for link in links:
                if link.startswith(('http', 'mailto', 'tel', 'javascript')):
                    continue
                
                # Check if it's a valid local file
                link_clean = link.replace('\\', '/')
                if link_clean.lower() in all_files:
                    actual_path = all_files[link_clean.lower()]
                    if actual_path != link_clean:
                        broken_links.append(f"CASE MISMATCH in {html_file}: Linked '{link_clean}', actual file '{actual_path}'")
                elif not os.path.exists(link_clean):
                    broken_links.append(f"NOT FOUND in {html_file}: {link_clean}")

    return broken_links

results = check_links()
for r in results:
    print(r)
