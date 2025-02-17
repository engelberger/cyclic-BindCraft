#!/usr/bin/env python3
import os
import argparse
import json

def generate_commands(settings_path, filters_path, advanced_path, n_jobs):
    """Generate commands file for BindCraft array jobs"""
    
    # Get the absolute path of the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # First, update the PDB path in the settings file
    with open(settings_path, 'r') as f:
        settings = json.load(f)
    
    # Update the PDB path to use the proteins directory
    pdb_filename = os.path.basename(settings['starting_pdb'])
    settings['starting_pdb'] = os.path.join(script_dir, 'proteins', pdb_filename)
    
    # Add     "target_hotspot_residues": "40,41,50", residue 44,117,118 to the existing target_hotspot_residues
    existing_residues = settings.get('target_hotspot_residues', '')
    new_residues = f"{existing_residues},44,117,118"
    settings['target_hotspot_residues'] = new_residues
    
    # Create a temporary settings file with the updated path
    temp_settings_path = settings_path.replace('.json', '_temp.json')
    with open(temp_settings_path, 'w') as f:
        json.dump(settings, f, indent=2)
    
    # Create base command using the temporary settings file
    base_cmd = f"python -u bindcraft.py --settings {temp_settings_path}"
    
    if filters_path:
        base_cmd += f" --filters {filters_path}"
    if advanced_path:
        base_cmd += f" --advanced {advanced_path}"
    
    print(f"Generating {n_jobs} commands with base command: {base_cmd}")
    
    # Write commands to file using absolute path
    settings_target_dir = os.path.join(script_dir, 'settings_target')
    output_file = os.path.join(settings_target_dir, f"commands_bindcraft_{os.path.basename(settings_path).split('_')[0]}")
    print(f"Writing to file: {output_file}")
    
    # Create directory if it doesn't exist
    os.makedirs(settings_target_dir, exist_ok=True)
    
    with open(output_file, 'w') as f:
        for i in range(n_jobs):
            f.write(f"{base_cmd}\n")
            print(f"Wrote command {i+1}")

def main():
    parser = argparse.ArgumentParser(description='Generate BindCraft commands file')
    parser.add_argument('--settings', '-s', required=True, help='Path to settings JSON file')
    parser.add_argument('--filters', '-f', default=None, help='Path to filters JSON file')
    parser.add_argument('--advanced', '-a', default=None, help='Path to advanced settings JSON file')
    parser.add_argument('--n_jobs', '-n', type=int, required=True, help='Number of array jobs to generate')
    
    args = parser.parse_args()
    print(f"Arguments received: {args}")
    generate_commands(args.settings, args.filters, args.advanced, args.n_jobs)

if __name__ == '__main__':
    main()