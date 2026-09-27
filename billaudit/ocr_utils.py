# billaudit/ocr_utils.py
import re
import easyocr

reader = easyocr.Reader(['en'], gpu=False)  # set gpu=True if you want to use your RTX 3050


def extract_text_from_image(image_path):
    """Run OCR on the bill image, return raw text as one string."""
    results = reader.readtext(image_path, detail=0)  # detail=0 -> just text, no bounding boxes
    return "\n".join(results)


def parse_line_items(raw_text):
    """
    Very basic parser: looks for lines like
    'Consultation Fee 500' or 'X-Ray - Rs. 1200'
    Returns list of dicts: [{'item': str, 'amount': float}, ...]
    """
    line_items = []
    # matches a line ending in a number (with optional decimals, commas, Rs/₹ symbols)
    pattern = re.compile(r'^(.*?)[\s\-:.]*[₹Rs]*\.?\s*([\d,]+\.?\d*)\s*$', re.IGNORECASE)

    for line in raw_text.split('\n'):
        line = line.strip()
        if not line:
            continue
        match = pattern.match(line)
        if match:
            item_name = match.group(1).strip()
            amount_str = match.group(2).replace(',', '')
            try:
                amount = float(amount_str)
                if item_name and amount > 0:
                    line_items.append({'item': item_name, 'amount': amount})
            except ValueError:
                continue
    return line_items


def check_bill(line_items, stated_total=None):
    """
    Run basic checks on parsed line items.
    Returns a dict of findings.
    """
    findings = {
        'duplicates': [],
        'high_value_flags': [],
        'sum_mismatch': None,
        'computed_total': 0
    }

    seen = {}
    for item in line_items:
        key = item['item'].lower()
        if key in seen:
            findings['duplicates'].append(item['item'])
        else:
            seen[key] = item['amount']
        findings['computed_total'] += item['amount']

        # flag if a single item is unusually expensive - tune threshold as needed
        if item['amount'] > 10000:
            findings['high_value_flags'].append(item)

    if stated_total is not None:
        diff = abs(findings['computed_total'] - stated_total)
        if diff > 1:  # allow ₹1 rounding tolerance
            findings['sum_mismatch'] = {
                'stated_total': stated_total,
                'computed_total': findings['computed_total'],
                'difference': diff
            }

    return findings