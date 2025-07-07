#!/usr/bin/env python
import os
import importlib.util
import sys
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def run_fixture_file(file_path):
    """Import and run a fixture file"""
    file_name = os.path.basename(file_path)
    if file_name.startswith('__') or not file_name.endswith('.py'):
        return False
    
    print(f"Running fixture: {file_name}")
    
    # Import the module dynamically
    spec = importlib.util.spec_from_file_location("module.name", file_path)
    fixture_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixture_module)
    
    return True

def main():
    fixtures_dir = os.path.join('dashboard_app', 'fixtures')
    fixtures_path = os.path.abspath(fixtures_dir)
    
    print(f"Looking for fixture files in: {fixtures_path}")
    
    success_count = 0
    total_files = 0
    
    for filename in os.listdir(fixtures_path):
        file_path = os.path.join(fixtures_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.py') and not filename.startswith('__'):
            total_files += 1
            if run_fixture_file(file_path):
                success_count += 1
    
    print(f"\nCompleted running {success_count} out of {total_files} fixture files.")

if __name__ == "__main__":
    main()
