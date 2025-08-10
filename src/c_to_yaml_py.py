#!/usr/bin/env python3
"""
C Header to YAML Converter (Python Implementation)

This is a Python implementation of the C-to-YAML converter to demonstrate
the complete workflow without requiring a C compiler.
"""

import re
import sys

def parse_c_header_to_yaml(header_file, output_file=None):
    """Parse C header file and convert back to YAML format."""
    
    try:
        with open(header_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{header_file}' not found.")
        return False
    
    # Initialize instruction data
    inst_data = {}
    
    # Extract string fields using regex
    string_fields = {
        'schema': r'\.schema = "([^"]*)"',
        'kind': r'\.kind = "([^"]*)"', 
        'name': r'\.name = "([^"]*)"',
        'long_name': r'\.long_name = "([^"]*)"',
        'description': r'\.description = "([^"]*)"',
        'defined_by': r'\.defined_by = "([^"]*)"',
        'assembly': r'\.assembly = "([^"]*)"',
        'encoding_match': r'\.encoding_match = "([^"]*)"',
        'operation': r'\.operation = "([^"]*)"',
        'sail_operation': r'\.sail_operation = "([^"]*)"'
    }
    
    for field, pattern in string_fields.items():
        match = re.search(pattern, content)
        if match:
            # Unescape C string
            value = match.group(1)
            value = value.replace('\\n', '\n').replace('\\t', '\t')
            value = value.replace('\\"', '"').replace('\\\\', '\\')
            inst_data[field] = value
    
    # Extract access modes
    access_fields = {
        's': r'\.s = "([^"]*)"',
        'u': r'\.u = "([^"]*)"', 
        'vs': r'\.vs = "([^"]*)"',
        'vu': r'\.vu = "([^"]*)"'
    }
    
    access_data = {}
    for field, pattern in access_fields.items():
        match = re.search(pattern, content)
        if match:
            access_data[field] = match.group(1)
    
    # Extract data_independent_timing
    timing_match = re.search(r'\.data_independent_timing = (\d+)', content)
    timing = timing_match.group(1) == '1' if timing_match else False
    
    # Extract encoding variables
    variables = []
    var_pattern = r'\{ "([^"]*)", "([^"]*)" \}'
    for match in re.finditer(var_pattern, content):
        if match.group(1) != "NULL":  # Skip sentinel
            variables.append({
                'name': match.group(1),
                'location': match.group(2)
            })
    
    # Generate YAML content
    yaml_content = ""
    
    if 'schema' in inst_data and inst_data['schema']:
        yaml_content += f"$schema: \"{inst_data['schema']}\"\n"
    if 'kind' in inst_data and inst_data['kind']:
        yaml_content += f"kind: {inst_data['kind']}\n"
    if 'name' in inst_data and inst_data['name']:
        yaml_content += f"name: {inst_data['name']}\n"
    if 'long_name' in inst_data and inst_data['long_name']:
        yaml_content += f"long_name: {inst_data['long_name']}\n"
    
    if 'description' in inst_data and inst_data['description']:
        yaml_content += "description: |\n"
        for line in inst_data['description'].split('\n'):
            yaml_content += f"  {line}\n"
    
    if 'defined_by' in inst_data and inst_data['defined_by']:
        yaml_content += f"definedBy: {inst_data['defined_by']}\n"
    if 'assembly' in inst_data and inst_data['assembly']:
        yaml_content += f"assembly: {inst_data['assembly']}\n"
    
    # Encoding section
    yaml_content += "encoding:\n"
    if 'encoding_match' in inst_data and inst_data['encoding_match']:
        yaml_content += f"  match: {inst_data['encoding_match']}\n"
    
    if variables:
        yaml_content += "  variables:\n"
        for var in variables:
            yaml_content += f"    - name: {var['name']}\n"
            yaml_content += f"      location: {var['location']}\n"
    
    # Access section
    if access_data:
        yaml_content += "access:\n"
        for mode, value in access_data.items():
            if value:
                yaml_content += f"  {mode}: {value}\n"
    
    # Timing
    yaml_content += f"data_independent_timing: {'true' if timing else 'false'}\n"
    
    # Operations
    if 'operation' in inst_data and inst_data['operation']:
        yaml_content += "operation(): |\n"
        for line in inst_data['operation'].split('\n'):
            yaml_content += f"  {line}\n"
    
    if 'sail_operation' in inst_data and inst_data['sail_operation']:
        yaml_content += "sail(): |\n"
        for line in inst_data['sail_operation'].split('\n'):
            yaml_content += f"  {line}\n"
    
    # Write output
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(yaml_content)
            print(f"YAML output written to: {output_file}")
        except IOError as e:
            print(f"Error writing YAML file: {e}")
            return False
    else:
        print(yaml_content)
    
    return True

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python c_to_yaml_py.py <header_file> [output_yaml_file]")
        sys.exit(1)
    
    header_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) == 3 else None
    
    if not parse_c_header_to_yaml(header_file, output_file):
        sys.exit(1)

if __name__ == "__main__":
    main()
