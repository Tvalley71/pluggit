import re

# 🔁 Define replacements
REPLACEMENTS = [
    ("DANTHERM", "PLUGGIT"),
    ("Dantherm", "Pluggit"),
    ("dantherm", "pluggit"),
]

# 📄 Read source README from dantherm
with open("dantherm/README.md", "r", encoding="utf-8") as f:
    source = f.read()

# 📄 Read target README
with open("README.md", "r", encoding="utf-8") as f:
    target = f.read()

# 🧠 Section types
section_types = {
    "shared-section": False,       # partial replace (not in URLs)
    "replace-section": True,       # full replace (incl. URLs)
    "no-replace-section": None     # no replace
}

# 🔄 Replace, skipping URLs if full=False
def apply_replacements(text, full):
    if full is None:
        return text

    if full:
        for old, new in REPLACEMENTS:
            text = text.replace(old, new)
        return text

    # partial replace: avoid changing inside URLs
    def replacer(match):
        url = match.group(0)
        return url  # leave URL untouched

    # Find all URLs to protect
    url_pattern = re.compile(r'https?://[^\s)>\]]+')
    protected_urls = list(url_pattern.finditer(text))

    protected_ranges = [(m.start(), m.end()) for m in protected_urls]

    def in_protected(pos):
        return any(start <= pos < end for start, end in protected_ranges)

    result = []
    i = 0
    while i < len(text):
        if in_protected(i):
            # Copy URL verbatim
            for start, end in protected_ranges:
                if start == i:
                    result.append(text[start:end])
                    i = end
                    break
        else:
            replaced = False
            for old, new in REPLACEMENTS:
                if text.startswith(old, i):
                    result.append(new)
                    i += len(old)
                    replaced = True
                    break
            if not replaced:
                result.append(text[i])
                i += 1

    return ''.join(result)

# 🔁 Replace sections
def replace_sections(section_type, full_replace_flag):
    pattern = re.compile(
        rf'<!-- START:{section_type} -->(.*?)<!-- END:{section_type} -->',
        re.DOTALL
    )
    source_sections = pattern.findall(source)
    target_matches = list(pattern.finditer(target))

    if len(source_sections) != len(target_matches):
        print(f"❌ Mismatch in {section_type}: {len(source_sections)} source vs {len(target_matches)} target sections")
        exit(1)

    processed = [apply_replacements(s, full_replace_flag) for s in source_sections]

    parts = []
    last_end = 0
    for i, match in enumerate(target_matches):
        parts.append(target[last_end:match.start(1)])
        parts.append(processed[i])
        last_end = match.end(1)
    parts.append(target[last_end:])
    return ''.join(parts)

# 🔁 Run all section replacements
for section, flag in section_types.items():
    target = replace_sections(section, flag)

# 💾 Save
with open("README.md", "w", encoding="utf-8") as f:
    f.write(target)

print("✅ README updated successfully with all section types.")
