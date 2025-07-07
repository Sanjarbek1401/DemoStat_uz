import json
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.conf import settings
from dashboard_app.models import Region, StatisticsData


class Command(BaseCommand):
    help = 'Import demographic data from JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='dashboard_app/data/regions_data.json',
            help='Path to JSON data file'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before import'
        )
        parser.add_argument(
            '--validate-only',
            action='store_true',
            help='Only validate data without importing'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise CommandError(f'File not found: {file_path}')

        # Load JSON data
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise CommandError(f'Invalid JSON file: {e}')

        # Validate data structure
        self.validate_data(data)
        
        if options['validate_only']:
            self.stdout.write(
                self.style.SUCCESS('✅ Data validation passed!')
            )
            return

        # Clear existing data if requested
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            StatisticsData.objects.all().delete()

        # Import data
        self.import_data(data)
        
        self.stdout.write(
            self.style.SUCCESS('✅ Data import completed successfully!')
        )

    def validate_data(self, data):
        """Validate JSON data structure"""
        required_keys = ['metadata', 'regions']
        for key in required_keys:
            if key not in data:
                raise CommandError(f'Missing required key: {key}')

        metadata = data['metadata']
        required_metadata = ['years', 'age_groups', 'genders']
        for key in required_metadata:
            if key not in metadata:
                raise CommandError(f'Missing metadata key: {key}')

        # Validate regions data
        for region_name, region_data in data['regions'].items():
            if 'svg_id' not in region_data:
                raise CommandError(f'Missing svg_id for region: {region_name}')
            
            if 'data' not in region_data:
                raise CommandError(f'Missing data for region: {region_name}')

            # Validate age groups sum to total
            for gender, years_data in region_data['data'].items():
                for year, populations in years_data.items():
                    if 'total' in populations:
                        total = populations['total']
                        individual_sum = sum(
                            pop for age, pop in populations.items() 
                            if age != 'total'
                        )
                        if abs(total - individual_sum) > 1:  # Allow for rounding errors
                            self.stdout.write(
                                self.style.WARNING(
                                    f'⚠️  {region_name} {gender} {year}: Total ({total:,}) != Sum ({individual_sum:,})'
                                )
                            )

        self.stdout.write('✅ Data structure validation passed')

    def import_data(self, data):
        """Import data into database"""
        imported_count = 0
        
        with transaction.atomic():
            for region_name, region_data in data['regions'].items():
                # Get or create region
                region, created = Region.objects.get_or_create(
                    name=region_name,
                    defaults={'svg_id': region_data['svg_id']}
                )
                
                if created:
                    self.stdout.write(f'Created region: {region_name}')

                # Import demographic data
                for gender, years_data in region_data['data'].items():
                    for year, populations in years_data.items():
                        year = int(year)
                        
                        for age_group, population in populations.items():
                            if age_group == 'total':
                                age_min, age_max = 0, None
                            elif age_group == '85+':
                                age_min, age_max = 85, None
                            elif '-' in age_group:
                                age_parts = age_group.split('-')
                                age_min, age_max = int(age_parts[0]), int(age_parts[1])
                            else:
                                continue  # Skip invalid age groups

                            # Create or update record
                            record, created = StatisticsData.objects.update_or_create(
                                region=region,
                                year=year,
                                age_min=age_min,
                                age_max=age_max,
                                gender=gender,
                                defaults={'population': population}
                            )
                            
                            if created:
                                imported_count += 1

        self.stdout.write(f'Imported {imported_count} new records')

    def get_age_range(self, age_str):
        """Convert age string to min/max values"""
        if age_str == 'total':
            return 0, None
        elif age_str == '85+':
            return 85, None
        elif '-' in age_str:
            parts = age_str.split('-')
            return int(parts[0]), int(parts[1])
        else:
            raise ValueError(f'Invalid age range: {age_str}') 