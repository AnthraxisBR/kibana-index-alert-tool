import re


def clear_html_tags(string: str):
    clean = re.compile('<.*?>')
    cleaned = re.sub(clean, '', string)
    cleaned = cleaned.replace('\n\n', '')
    return cleaned
