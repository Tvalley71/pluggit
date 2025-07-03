import re

# 🔁 Define replacements
REPLACEMENTS = [
    ("DANTHERM", "PLUGGIT"),
    ("Dantherm", "Pluggit"),
    ("dantherm", "pluggit"),
]

def sync_readme(source_file, target_file):

    # 🔄 Replace, skipping URLs if mode allows replacements
    def apply_replacements(text, mode):
        if mode == "no-replace":
            return text

        if mode == "replace-all":
            # Replace everything, including URLs
            for old, new in REPLACEMENTS:
                text = text.replace(old, new)
            return text

        if mode:
            raise Exception(f"❌ Invalid replacement mode {mode}")

        # Default mode (None): partial replace - avoid changing inside URLs
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

    # Function to read until a specific pattern, returning the content and match object
    def read_until(text, pattern, start_pos=0):
        """Searches for a regex pattern in text starting from start_pos. Returns the content up to and including the match."""
        if start_pos >= len(text):
            return '', None
        
        search_text = text[start_pos:]
        match = re.search(pattern, search_text)
        
        if match:
            # Return content from start_pos up to and including the match
            end_pos = start_pos + match.end()
            return text[start_pos:end_pos], match
        else:
            # No match found, return remaining text
            return text[start_pos:], None

    # Function to read until the next shared section, returning content, prefix, mode, and new position
    def read_until_shared_section(text, start_pos=0):
        """Reads the content until next shared-section from the given position."""

        content, match = read_until(text, r'<!-- (START|END):shared-section(?:\s+([\w-]+))? -->', start_pos)
        if not match:
            return content, None, None, len(text)  # No match found, return end position

        prefix = match.group(1)
        
        try:
            mode = match.group(2)
        except IndexError:
            mode = None  # group doesn't exist

        # Calculate the new position after the match
        new_pos = start_pos + match.end()
        
        return content, prefix, mode, new_pos

    with open(source_file, 'r', encoding='utf-8') as f:
        source = f.read()   
        
    with open(target_file, 'r', encoding='utf-8') as f:
        target = f.read()

    target_pos = 0
    source_pos = 0

    output = ''
    mode_stack = []  # Stack to track nested modes

    while True:
        # Write the target section until next shared section
        text, target_prefix, _, target_pos = read_until_shared_section(target, target_pos)
        if text:
            output += text
        if not target_prefix:
            # No more shared sections in target, break the loop
            break

        if target_prefix != 'START':
            raise Exception(f"❌ Expected 'START' prefix, but found '{target_prefix}' in target file.")

        # Skip in source to the next shared section
        _, source_prefix, source_mode, source_pos = read_until_shared_section(source, source_pos)
        if not source_prefix:
            raise Exception("❌ Source file ran out of shared sections.")
        elif source_prefix != 'START':
            raise Exception(f"❌ Expected 'START' prefix, but found '{source_prefix}' in source file.")

        # Push the initial mode onto the stack
        mode_stack.append(source_mode)
        nesting = 1

        while True:
            # Use the current mode from the top of the stack
            current_mode = mode_stack[-1] if mode_stack else None
            
            # Write the source section until next shared section
            text, source_prefix, next_mode, source_pos = read_until_shared_section(source, source_pos)
            text = apply_replacements(text, current_mode)
            output += text

            # Skip in target to the next shared section
            _, target_prefix, _, target_pos = read_until_shared_section(target, target_pos)

            if source_prefix != target_prefix:
                raise Exception(f"❌ Tag mismatch: source '{source_prefix}' vs target '{target_prefix}'")

            if source_prefix == 'START':
                # Push new mode onto stack for nested section
                mode_stack.append(next_mode)
                nesting += 1
            elif source_prefix == 'END':
                # Pop mode from stack when section ends
                if mode_stack:
                    mode_stack.pop()
                nesting -= 1
                if nesting < 0:
                    raise Exception("❌ Unmatched 'END' tag in source file.")
                elif nesting == 0:
                    # If we reached the end of the nested shared section, break to write the next target section
                    break
            
    with open(target_file, 'w', encoding='utf-8') as out:
        out.write(output)

    print("✅ Sync completed. Output written to target file")

sync_readme('dantherm/README.md', 'README.md')
