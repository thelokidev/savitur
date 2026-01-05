# Fix the corrupted drik.py file by applying the warnings.warn fix

import os

drik_path = "o:/savitur/PyJHora/src/jhora/panchanga/drik.py"
backup_path = "o:/savitur/PyJHora/src/jhora/panchanga/drik_backup.py"

# Read the file
with open(drik_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the problematic warnings.warn line
old_warn = 'warnings.warn("Unsupported Ayanamsa mode:", ayanamsa_mode,const._DEFAULT_AYANAMSA_MODE+" Assumed")'
new_warn = 'warnings.warn(f"Unsupported Ayanamsa mode: {ayanamsa_mode}. {const._DEFAULT_AYANAMSA_MODE} Assumed")'

if old_warn in content:
    content = content.replace(old_warn, new_warn)
    print(f"Fixed warnings.warn call")
    with open(drik_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("File saved successfully")
else:
    print("Pattern not found - file might already be corrupted")
    print("Attempting to restore from backup if exists...")
    
    # Check if we can copy from drik1.py the correct implementation
    print("Please manually restore the file from git or backup")
