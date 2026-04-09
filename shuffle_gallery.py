import re
import random

def shuffle_gallery(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match the port-item div and its THREE nested closing tags
    item_regex = r'(<div class="[^"]*port-item"[^>]*>.*?</div>\s+</div>\s+</div>)'
    items = re.findall(item_regex, content, re.DOTALL)
    
    if not items:
        print(f"No items found in {filepath}")
        return

    # Filter out forbidden images
    forbidden = [
        'gallery-haircut.jpg.webp',
        'Hero_section-1.jpg.webp',
        'Hero_section-2.webp',
        'our work.jpg.webp'
    ]
    
    filtered_items = []
    for item in items:
        skip = False
        for f in forbidden:
            if f in item:
                skip = True
                break
        if not skip:
            filtered_items.append(item)
    
    # Shuffle
    random.shuffle(filtered_items)
    
    # Replace the gallery block inside portfolio-grid
    container_pattern = r'(<div class="row g-4 mt-2 portfolio-grid">)(.*?)(</div>\s+</div>\s+</section>)'
    
    # For safety, let's find the grid specifically
    grid_match = re.search(container_pattern, content, re.DOTALL)
    if not grid_match:
        # Try alternate pattern for gallery.html which might have different structure
        container_pattern = r'(<div class="row g-4 mt-2 portfolio-grid">)(.*?)(</div>\s+</div>\s+</div>\s+</section>|</div>\s+</div>\s+</section>)'
        grid_match = re.search(container_pattern, content, re.DOTALL)

    if grid_match:
        header = grid_match.group(1)
        # We need to be careful with the footer match because of nested divs
        # I'll just replace the content between the start of the first item and the end of the last item in the group
        
        inner_content = grid_match.group(2)
        new_inner = "\n        " + "\n        ".join(filtered_items) + "\n      "
        new_content = content[:grid_match.start(2)] + new_inner + content[grid_match.end(2):]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully shuffled {len(filtered_items)} items in {filepath}")
    else:
        print(f"Could not find portfolio-grid container in {filepath}")

shuffle_gallery(r'c:\Users\MSI\OneDrive\Desktop\Salon\cunnet-clone\index.html')
shuffle_gallery(r'c:\Users\MSI\OneDrive\Desktop\Salon\cunnet-clone\gallery.html')
