
import re

def replace_text_preserving_urls_and_noblocks(text):
    """
    Replace 'Dantherm' with 'Pluggit' and 'dantherm' with 'pluggit',
    except inside:
      - URLs (e.g. https://...)
      - no-replace blocks marked with <!-- START:no-dantherm-replace --> ... <!-- END:no-dantherm-replace -->
    """
    # Temporarily protect URLs
    url_pattern = re.compile(r'https?://[^\s\)]+')
    urls = url_pattern.findall(text)
    for i, url in enumerate(urls):
        text = text.replace(url, f"__URL_PLACEHOLDER_{i}__")

    # Temporarily protect no-dantherm-replace blocks
    noblock_pattern = re.compile(r'<!-- START:no-dantherm-replace -->(.*?)<!-- END:no-dantherm-replace -->', re.DOTALL)
    noblocks = noblock_pattern.findall(text)
    for i, block in enumerate(noblocks):
        text = text.replace(block, f"__BLOCK_PLACEHOLDER_{i}__")

    # Perform replacements outside protected areas
    text = text.replace("Dantherm", "Pluggit").replace("dantherm", "pluggit")

    # Restore no-replace blocks
    for i, block in enumerate(noblocks):
        text = text.replace(f"__BLOCK_PLACEHOLDER_{i}__", block)

    # Restore URLs
    for i, url in enumerate(urls):
        text = text.replace(f"__URL_PLACEHOLDER_{i}__", url)

    return text

# Read source README from Dantherm repo
with open("dantherm/README.md", "r", encoding="utf-8") as f:
    source = f.read()

# Extract all shared-section blocks
pattern = re.compile(r'<!-- START:shared-section -->(.*?)<!-- END:shared-section -->', re.DOTALL)
sections = pattern.findall(source)

if not sections:
    print("❌ No shared-section blocks found in Dantherm README.md")
    exit(1)

# Process each shared-section block with replacements
processed_sections = [replace_text_preserving_urls_and_noblocks(s) for s in sections]

# Read target README (Pluggit)
with open("README.md", "r", encoding="utf-8") as f:
    target = f.read()

# Replace all shared-section blocks in target README
def replace_sections(content, new_sections):
    parts = []
    last_end = 0
    matches = list(pattern.finditer(content))
    if len(matches) != len(new_sections):
        print(f"❌ Mismatch: {len(new_sections)} source vs {len(matches)} target sections")
        exit(1)
    for i, match in enumerate(matches):
        parts.append(content[last_end:match.start(1)])
        parts.append(new_sections[i])
        last_end = match.end(1)
    parts.append(content[last_end:])
    return ''.join(parts)

# Write updated README back to file
new_target = replace_sections(target, processed_sections)
with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_target)

print(f"✅ Inserted {len(sections)} shared sections into pluggit-test/README.md")
