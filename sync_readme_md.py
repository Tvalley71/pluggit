
import re

# Read source README from Dantherm
with open("dantherm/README.md", "r", encoding="utf-8") as f:
    source = f.read()

# Find all shared-section blocks
shared_pattern = re.compile(r"<!-- START:shared-section -->(.*?)<!-- END:shared-section -->", re.DOTALL)
shared_sections = shared_pattern.findall(source)

if not shared_sections:
    print("❌ No shared-section blocks found in Dantherm README.md")
    exit(1)

processed_sections = []

# Regex for no-replace blocks
no_replace_pattern = re.compile(
    r"<!-- START:no-dantherm-replace -->(.*?)<!-- END:no-dantherm-replace -->",
    re.DOTALL,
)

# Regex for URLs
url_pattern = re.compile(r"https?://[^\s)]+", re.DOTALL)

for section in shared_sections:
    placeholders = {}

    # Protect no-dantherm-replace blocks
    def protect_no_replace(match):
        key = f"__PLACEHOLDER_NO_REPLACE_{len(placeholders)}__"
        placeholders[key] = match.group(0)
        return key

    protected = no_replace_pattern.sub(protect_no_replace, section)

    # Protect URLs
    def protect_url(match):
        key = f"__PLACEHOLDER_URL_{len(placeholders)}__"
        placeholders[key] = match.group(0)
        return key

    protected = url_pattern.sub(protect_url, protected)

    # Perform replacements
    replaced = (
        protected.replace("DANTHERM", "PLUGGIT")
                 .replace("Dantherm", "Pluggit")
                 .replace("dantherm", "pluggit")
    )

    # Restore placeholders
    for key, value in placeholders.items():
        replaced = replaced.replace(key, value)

    processed_sections.append(replaced)

# Read target README (Pluggit)
with open("README.md", "r", encoding="utf-8") as f:
    target = f.read()

# Replace the shared-section blocks
matches = list(shared_pattern.finditer(target))
if len(matches) != len(processed_sections):
    print(f"❌ Mismatch: {len(processed_sections)} source vs {len(matches)} target sections")
    exit(1)

# Replace contents block by block
def replace_sections(content, new_sections):
    parts = []
    last_end = 0
    for i, match in enumerate(shared_pattern.finditer(content)):
        parts.append(content[last_end:match.start(1)])
        parts.append(new_sections[i])
        last_end = match.end(1)
    parts.append(content[last_end:])
    return ''.join(parts)

new_target = replace_sections(target, processed_sections)

# Save updated README
with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_target)

print(f"✅ Updated {len(processed_sections)} shared sections in Pluggit README.md")
