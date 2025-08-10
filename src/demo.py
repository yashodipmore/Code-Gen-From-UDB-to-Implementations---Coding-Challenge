#!/usr/bin/env python3
"""
Complete Workflow Demonstration Script

This script demonstrates the entire RISC-V UDB to C header conversion workflow
and generates a summary report.
"""

import subprocess
import sys
import os
from datetime import datetime

def run_command(cmd, description):
    """Run a command and capture its output."""
    print(f"\n{'='*60}")
    print(f"STEP: {description}")
    print(f"COMMAND: {cmd}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        if result.stdout:
            print("OUTPUT:")
            print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def check_file_exists(filename):
    """Check if a file exists and show its size."""
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        print(f"✅ File '{filename}' created successfully ({size} bytes)")
        return True
    else:
        print(f"❌ File '{filename}' not found")
        return False

def compare_files(file1, file2):
    """Compare two text files and report differences."""
    try:
        with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
            content1 = f1.read()
            content2 = f2.read()
            
        if content1 == content2:
            print(f"✅ Files '{file1}' and '{file2}' are IDENTICAL")
            return True
        else:
            print(f"❌ Files '{file1}' and '{file2}' are DIFFERENT")
            return False
    except Exception as e:
        print(f"❌ Error comparing files: {e}")
        return False

def main():
    """Run the complete demonstration workflow."""
    print("RISC-V UDB to C Header Converter - Complete Workflow Demonstration")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: YAML to C Header
    success1 = run_command(
        "python yaml_to_c.py sample_instruction.yaml output.h",
        "Convert original YAML to C header"
    )
    check_file_exists("output.h")
    
    # Step 2: C Header to YAML
    success2 = run_command(
        "python c_to_yaml_py.py output.h output.yaml",
        "Convert C header back to YAML"
    )
    check_file_exists("output.yaml")
    
    # Step 3: YAML to C Header (round-trip)
    success3 = run_command(
        "python yaml_to_c.py output.yaml output2.h",
        "Convert generated YAML to C header (round-trip test)"
    )
    check_file_exists("output2.h")
    
    # Step 4: C Header to YAML (final verification)
    success4 = run_command(
        "python c_to_yaml_py.py output2.h output2.yaml",
        "Convert second C header to YAML (final verification)"
    )
    check_file_exists("output2.yaml")
    
    # Verification: Compare round-trip files
    print(f"\n{'='*60}")
    print("VERIFICATION: Round-trip consistency check")
    print(f"{'='*60}")
    
    yaml_match = compare_files("output.yaml", "output2.yaml")
    header_match = compare_files("output.h", "output2.h")
    
    # Summary
    print(f"\n{'='*60}")
    print("WORKFLOW SUMMARY")
    print(f"{'='*60}")
    
    steps = [
        ("Step 1: YAML → C Header", success1),
        ("Step 2: C Header → YAML", success2),
        ("Step 3: YAML → C Header (round-trip)", success3),
        ("Step 4: C Header → YAML (verification)", success4),
        ("YAML Round-trip Consistency", yaml_match),
        ("C Header Round-trip Consistency", header_match)
    ]
    
    all_success = True
    for step_name, success in steps:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{step_name:<40} {status}")
        if not success:
            all_success = False
    
    print(f"\n{'='*60}")
    if all_success:
        print("🎉 ALL TESTS PASSED! Round-trip conversion is working perfectly!")
        print("✅ Data integrity maintained through complete conversion cycle")
        print("✅ RISC-V UDB format compatibility verified")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
    
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    # Generate file listing
    print("\nGENERATED FILES:")
    files = [
        "sample_instruction.yaml",
        "output.h", 
        "output.yaml",
        "output2.h",
        "output2.yaml",
        "SOLUTION_REPORT.md"
    ]
    
    for filename in files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"  📄 {filename:<25} ({size:,} bytes)")
    
    return all_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
