import re
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup, Tag

def extract_dom_selector(tag: Tag) -> str:
    """Generates a clean, identifiable CSS selector for a BeautifulSoup tag."""
    parts = []
    curr = tag
    while curr and curr.name and curr.name != '[document]':
        tag_name = curr.name
        if curr.get('id'):
            parts.insert(0, f"#{curr['id']}")
            break
        elif curr.get('class'):
            classes = curr['class']
            if isinstance(classes, list) and classes:
                first_class = classes[0]
                if not any(char in first_class for char in [':', '/', '\\', '$', '@']):
                    parts.insert(0, f"{tag_name}.{first_class}")
                else:
                    parts.insert(0, tag_name)
            else:
                parts.insert(0, tag_name)
        else:
            parts.insert(0, tag_name)
        
        curr = curr.parent
        if len(parts) >= 3:
            break
            
    return " > ".join(parts) if parts else tag.name or ".ec-element"

def extract_structured_page_content(html_content: str, base_url: str = "") -> Dict[str, Any]:
    """
    Parses HTML content into structured e-commerce elements with exact DOM selectors.
    Preserves element hierarchy and boundaries so text snippets are clean and accurate.
    """
    if not html_content or not html_content.strip():
        return {
            "title": "",
            "meta_description": "",
            "elements": [],
            "combined_text": "",
            "prechecked_inputs": [],
            "promotional_banners": [],
            "pricing_elements": [],
            "action_buttons": [],
            "modals": [],
            "is_empty": True
        }

    soup = BeautifulSoup(html_content, "html.parser")

    # 1. Metadata
    title_tag = soup.find('title')
    page_title = title_tag.get_text(strip=True) if title_tag else ""
    
    meta_desc_tag = soup.find('meta', attrs={'name': re.compile(r'description', re.I)})
    meta_desc = meta_desc_tag.get('content', '').strip() if meta_desc_tag else ""
    if not meta_desc:
        og_desc = soup.find('meta', attrs={'property': 'og:description'})
        meta_desc = og_desc.get('content', '').strip() if og_desc else ""

    # 2. Decompose purely unrenderable/noise tags
    for noise in soup(["script", "style", "noscript", "svg", "canvas", "iframe"]):
        noise.decompose()

    elements: List[Dict[str, Any]] = []
    prechecked_inputs: List[Dict[str, Any]] = []
    promotional_banners: List[Dict[str, Any]] = []
    pricing_elements: List[Dict[str, Any]] = []
    action_buttons: List[Dict[str, Any]] = []
    modals: List[Dict[str, Any]] = []

    # 3. Check for pre-selected checkboxes (Critical for Basket Sneaking & Interface Interference)
    for checkbox in soup.find_all('input', attrs={'type': 'checkbox'}):
        is_checked = checkbox.has_attr('checked') or checkbox.get('checked') in ('checked', 'true', '')
        # Get parent or adjacent label text
        parent_text = ""
        if checkbox.parent:
            parent_text = checkbox.parent.get_text(separator=" ", strip=True)
        label_id = checkbox.get('id')
        if label_id:
            label_tag = soup.find('label', attrs={'for': label_id})
            if label_tag:
                parent_text = f"{parent_text} {label_tag.get_text(strip=True)}".strip()

        selector = extract_dom_selector(checkbox)
        if is_checked:
            item_data = {
                "tag": "input[type='checkbox']",
                "selector": selector,
                "text": parent_text or "Pre-checked optional checkbox",
                "is_checked": True,
                "context_type": "prechecked_input"
            }
            prechecked_inputs.append(item_data)
            elements.append(item_data)

    # 4. Check for Promotional Banners & Announcement Bars
    banner_selectors = re.compile(r'banner|promo|announcement|alert|marquee|countdown|urgency|deal|offer|ticker', re.I)
    for b_tag in soup.find_all(attrs={'class': banner_selectors}) + soup.find_all(attrs={'id': banner_selectors}):
        b_text = b_tag.get_text(separator=" ", strip=True)
        if 5 <= len(b_text) <= 500:
            selector = extract_dom_selector(b_tag)
            item = {
                "tag": b_tag.name,
                "selector": selector,
                "text": b_text,
                "context_type": "promotional_banner"
            }
            promotional_banners.append(item)
            elements.append(item)

    # 5. Buttons and Call-to-Actions
    for btn in soup.find_all(['button', 'input'], attrs={'type': re.compile(r'submit|button', re.I)}) + soup.find_all('a', attrs={'role': 'button'}):
        btn_text = btn.get_text(separator=" ", strip=True)
        if not btn_text and btn.get('value'):
            btn_text = str(btn.get('value')).strip()
        if 2 <= len(btn_text) <= 150:
            selector = extract_dom_selector(btn)
            item = {
                "tag": btn.name,
                "selector": selector,
                "text": btn_text,
                "context_type": "action_button"
            }
            action_buttons.append(item)
            elements.append(item)

    # 6. Pricing, Fees & Charges
    price_selectors = re.compile(r'price|fee|charge|handling|platform|convenience|tax|total|shipping|cost', re.I)
    for p_tag in soup.find_all(attrs={'class': price_selectors}) + soup.find_all(attrs={'id': price_selectors}):
        p_text = p_tag.get_text(separator=" ", strip=True)
        if 3 <= len(p_text) <= 250:
            selector = extract_dom_selector(p_tag)
            item = {
                "tag": p_tag.name,
                "selector": selector,
                "text": p_text,
                "context_type": "pricing_element"
            }
            pricing_elements.append(item)
            elements.append(item)

    # 7. Modals and Dialogs
    modal_tags = soup.find_all(['dialog', 'aside']) + soup.find_all(attrs={'role': 'dialog'}) + soup.find_all(attrs={'class': re.compile(r'modal|popup|overlay|drawer|dialog', re.I)})
    for m_tag in modal_tags:
        m_text = m_tag.get_text(separator=" ", strip=True)
        if 5 <= len(m_text) <= 600:
            selector = extract_dom_selector(m_tag)
            item = {
                "tag": m_tag.name,
                "selector": selector,
                "text": m_text,
                "context_type": "modal"
            }
            modals.append(item)
            elements.append(item)

    # 8. General Headings, Paragraphs, Lists, Spans, Labels, and terminal Containers
    text_container_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'span', 'strong', 'em', 'b', 'div', 'section', 'article', 'small', 'label', 'td', 'th', 'dd', 'dt']
    for text_tag in soup.find_all(text_container_tags):
        # Skip if container has child block elements that will be separately extracted
        if text_tag.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'table']):
            continue
        # Also avoid nested divs that contain another div
        if text_tag.name in ('div', 'section', 'article') and text_tag.find(['div', 'section', 'article']):
            continue

        t_text = text_tag.get_text(separator=" ", strip=True)
        if 4 <= len(t_text) <= 500:
            if not any(e["text"] == t_text for e in elements):
                elements.append({
                    "tag": text_tag.name,
                    "selector": extract_dom_selector(text_tag),
                    "text": t_text,
                    "context_type": "content_element"
                })

    # 9. Clean Full Text (separated by clean newlines to preserve sentence/block boundaries)
    clean_lines = []
    if page_title:
        clean_lines.append(page_title)
    if meta_desc:
        clean_lines.append(meta_desc)

    for el in elements:
        t = el["text"].strip()
        if t and t not in clean_lines:
            clean_lines.append(t)

    # Fallback to make sure no visible text string from the body was omitted
    if soup.body:
        for s in soup.body.stripped_strings:
            s_clean = s.strip()
            if len(s_clean) >= 6 and not any(s_clean in line for line in clean_lines):
                clean_lines.append(s_clean)
                elements.append({
                    "tag": "text",
                    "selector": "body",
                    "text": s_clean,
                    "context_type": "body_text"
                })

    combined_text = "\n".join(clean_lines)

    return {
        "title": page_title,
        "meta_description": meta_desc,
        "elements": elements,
        "combined_text": combined_text,
        "prechecked_inputs": prechecked_inputs,
        "promotional_banners": promotional_banners,
        "pricing_elements": pricing_elements,
        "action_buttons": action_buttons,
        "modals": modals,
        "is_empty": len(combined_text.strip()) < 20
    }
