import re
import random
import os

def shuffle_gallery(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    grid_start_tag = '<div class="row g-4 mt-2 portfolio-grid">'
    start_index = content.find(grid_start_tag)
    if start_index == -1:
        print(f"Portfolio grid not found in {filepath}")
        return

    item_regex = r'(<div class="[^"]*port-item"[^>]*>.*?</div>\s*</div>\s*</div>)'
    items = re.findall(item_regex, content, re.DOTALL)
    
    if not items:
        print(f"No items found in {filepath}")
        return

    print(f"Found {len(items)} items in {filepath}")
    
    # Shuffle the items
    random.shuffle(items)
    
    # Reset delays for smooth animation (0, 0.1, 0.2 per row of 3)
    shuffled_items = []
    for i, item in enumerate(items):
        delay = (i % 3) * 0.1
        # Replace data-delay="X" with new delay
        new_item = re.sub(r'data-delay="[^"]*"', f'data-delay="{delay:.1f}"', item)
        # Also handle data-gsap-delay if it exists
        new_item = re.sub(r'data-gsap-delay="[^"]*"', f'data-gsap-delay="{delay:.1f}"', new_item)
        shuffled_items.append(new_item)
    
    # Find positions
    all_items_match = list(re.finditer(item_regex, content, re.DOTALL))
    if not all_items_match:
        return
        
    first_item_start = all_items_match[0].start()
    last_item_end = all_items_match[-1].end()
    
    # Construct the new content
    new_items_block = "\n        ".join(shuffled_items)
    
    new_content = content[:first_item_start] + new_items_block + content[last_item_end:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully shuffled and normalized delays in {filepath}")

# Paths
base_path = r'c:\Users\MSI\OneDrive\Desktop\Salon\cunnet-clone'
shuffle_gallery(os.path.join(base_path, 'index.html'))
shuffle_gallery(os.path.join(base_path, 'gallery.html'))
