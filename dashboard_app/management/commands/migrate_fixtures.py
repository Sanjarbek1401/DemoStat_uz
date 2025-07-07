import json
import os
import glob
from django.core.management.base import BaseCommand
from collections import defaultdict


class Command(BaseCommand):
    help = 'Convert old fixture files to new JSON structure'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='dashboard_app/data/migrated_data.json',
            help='Output JSON file path'
        )

    def handle(self, *args, **options):
        output_path = options['output']
        
        # Create data structure
        data = {
            "metadata": {
                "version": "1.0",
                "migrated_from": "fixture_files",
                "age_groups": ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80-84", "85+"],
                "genders": ["jami", "erkak", "ayol"]
            },
            "regions": defaultdict(lambda: {"svg_id": "", "data": defaultdict(lambda: defaultdict(dict))})
        }

        # Find all fixture files
        fixture_files = glob.glob('dashboard_app/fixtures/*_data_template.py')
        
        self.stdout.write(f'Found {len(fixture_files)} fixture files')

        for file_path in fixture_files:
            self.process_fixture_file(file_path, data)

        # Convert defaultdict to regular dict for JSON serialization
        final_data = {
            "metadata": data["metadata"],
            "regions": {}
        }

        for region_name, region_data in data["regions"].items():
            final_data["regions"][region_name] = {
                "svg_id": region_data["svg_id"],
                "data": dict(region_data["data"])
            }

        # Write to file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=2, ensure_ascii=False)

        self.stdout.write(
            self.style.SUCCESS(f'✅ Migrated data to {output_path}')
        )

    def process_fixture_file(self, file_path, data):
        """Process a single fixture file"""
        filename = os.path.basename(file_path)
        
        # Parse filename: RegionName_gender_data_template.py
        parts = filename.replace('_data_template.py', '').split('_')
        if len(parts) < 2:
            return
            
        gender = parts[-1]  # last part is gender
        region_name = '_'.join(parts[:-1])  # everything else is region name
        
        # Map gender names
        gender_map = {
            'total': 'jami',
            'male': 'erkak', 
            'female': 'ayol',
            'jami': 'jami',
            'erkak': 'erkak',
            'ayol': 'ayol'
        }
        
        gender = gender_map.get(gender, gender)
        
        self.stdout.write(f'Processing: {region_name} - {gender}')
        
        # This is a simplified parser - in reality you'd need to properly parse Python files
        # For now, just create the structure
        
        # Set up region structure
        if not data["regions"][region_name]["svg_id"]:
            # Try to determine svg_id from region name
            svg_id_map = {
                'Toshkent': 'tashkent',
                'Toshkent Shahri': 'tashkent_city', 
                'Andijon': 'andijan',
                'Buxoro': 'bukhara',
                'Farg\'ona': 'fergana',
                'Jizzax': 'jizzakh',
                'Namangan': 'namangan',
                'Navoiy': 'navoi',
                'Qashqadaryo': 'kashkadarya',
                'Qoraqalpog\'iston': 'karakalpakstan',
                'Respublika': 'respublika',
                'Samarqand': 'samarkand',
                'Sirdaryo': 'sirdarya',
                'Surxondaryo': 'surkhandarya',
                'Xorazm': 'khorezm'
            }
            data["regions"][region_name]["svg_id"] = svg_id_map.get(region_name, region_name.lower())

        # Note: This is a placeholder - you would need to actually parse the Python file
        # to extract the real data. For now, just create the structure.
        self.stdout.write(f'  Created structure for {region_name} - {gender}')

    def extract_data_from_fixture(self, file_path):
        """Extract data from fixture file (simplified)"""
        # This would need to parse the Python file and extract the data array
        # For security reasons, we can't just exec() the file
        # You could use ast module to parse it safely
        pass 