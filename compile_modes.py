import os
import json

# Define constants
modes_dir = 'modes'
output_file = 'custom_modes.json' # Note the underscore as per plan

# Initialize list to hold mode data
all_modes = []

# Scan the modes directory
if os.path.isdir(modes_dir):
    for slug in os.listdir(modes_dir):
        if slug in ["architect", "code", "ask", "debug"]:
            print(f"Skipping mode '{slug}' as it is not a custom mode.")
            continue
        
        mode_path = os.path.join(modes_dir, slug)

        # Check if it's a directory
        if os.path.isdir(mode_path):
            metadata_path = os.path.join(mode_path, 'metadata.json')
            roledef_path = os.path.join(mode_path, 'roledefinition.md')
            instructions_path = os.path.join(mode_path, 'custominstructions.md')

            # Ensure all required files exist
            if os.path.exists(metadata_path) and os.path.exists(roledef_path) and os.path.exists(instructions_path):
                try:
                    # Read metadata.json
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        mode_data = json.load(f)

                    # Read roledefinition.md
                    with open(roledef_path, 'r', encoding='utf-8') as f:
                        role_definition = f.read()

                    # Read custominstructions.md
                    with open(instructions_path, 'r', encoding='utf-8') as f:
                        custom_instructions = f.read()

                    # Combine data
                    mode_data['roleDefinition'] = role_definition
                    mode_data['customInstructions'] = custom_instructions

                    # Append to the list
                    all_modes.append(mode_data)
                except Exception as e:
                    print(f"Error processing mode '{slug}': {e}")
            else:
                print(f"Warning: Skipping mode '{slug}' due to missing files.")

else:
    print(f"Error: Modes directory '{modes_dir}' not found.")

# Prepare final output structure
output_data = {"customModes": all_modes}

# Write the output file
try:
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    print(f"Successfully compiled modes to '{output_file}'")
except Exception as e:
    print(f"Error writing output file '{output_file}': {e}")


# Replace the file on disk at /Users/williameaston/Library/Application Support/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/custom_modes.json

local_settings_path = '/Users/williameaston/Library/Application Support/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/custom_modes.json'
with open(local_settings_path, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)
