import json
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from dashboard_app.models import Region, StatisticsData


class Command(BaseCommand):
    help = 'Rebuild database with optimized JSON data and fix all validation issues'

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            default='dashboard_app/data/complete_demographics.json',
            help='Source JSON file to import'
        )
        parser.add_argument(
            '--backup',
            action='store_true',
            help='Create backup before rebuilding'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force rebuild without confirmation'
        )
        parser.add_argument(
            '--fix-totals',
            action='store_true',
            help='Auto-fix total vs sum discrepancies'
        )

    def handle(self, *args, **options):
        source_file = options['source']
        backup = options.get('backup', False)
        force = options.get('force', False)
        fix_totals = options.get('fix_totals', False)
        
        if not os.path.exists(source_file):
            self.stdout.write(
                self.style.ERROR(f'❌ Source file not found: {source_file}')
            )
            return

        # Show current state
        current_count = StatisticsData.objects.count()
        self.stdout.write(f'📊 Current records: {current_count:,}')
        
        if not force:
            confirm = input(f'\n🚨 This will DELETE all {current_count:,} statistics records and rebuild from JSON.\nContinue? (yes/no): ')
            if confirm.lower() != 'yes':
                self.stdout.write('❌ Operation cancelled')
                return

        # Create backup if requested
        if backup:
            self.create_backup()

        # Load and validate JSON
        self.stdout.write('📥 Loading JSON data...')
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Failed to load JSON: {e}'))
            return

        # Validate JSON structure
        if not self.validate_json_structure(data):
            return

        # Rebuild database
        self.rebuild_database(data, fix_totals)

    def create_backup(self):
        """Create backup of current data"""
        backup_file = f'statistics_backup_{int(__import__("time").time())}.json'
        self.stdout.write(f'💾 Creating backup: {backup_file}')
        
        from .export_demographics import Command as ExportCommand
        export_cmd = ExportCommand()
        export_cmd.stdout = self.stdout
        
        # Export current data
        os.system(f'python manage.py export_demographics --format json --output {backup_file}')
        self.stdout.write(self.style.SUCCESS(f'✅ Backup created: {backup_file}'))

    def validate_json_structure(self, data):
        """Validate JSON structure"""
        required_keys = ['metadata', 'regions']
        for key in required_keys:
            if key not in data:
                self.stdout.write(self.style.ERROR(f'❌ Missing key: {key}'))
                return False

        regions_count = len(data['regions'])
        years_count = len(data['metadata']['years'])
        
        self.stdout.write(f'📊 JSON contains:')
        self.stdout.write(f'   - {regions_count} regions')
        self.stdout.write(f'   - {years_count} years ({min(data["metadata"]["years"])}-{max(data["metadata"]["years"])})')
        self.stdout.write(f'   - {len(data["metadata"]["age_groups"])} age groups')
        
        return True

    @transaction.atomic
    def rebuild_database(self, data, fix_totals):
        """Rebuild database with transaction safety"""
        self.stdout.write('🗑️  Clearing existing statistics data...')
        
        # Delete all statistics data
        deleted_count = StatisticsData.objects.count()
        StatisticsData.objects.all().delete()
        self.stdout.write(f'✅ Deleted {deleted_count:,} records')

        # Import new data
        self.stdout.write('📥 Importing optimized data...')
        
        imported_count = 0
        validation_errors = []
        
        for region_name, region_info in data['regions'].items():
            self.stdout.write(f'   Processing: {region_name}')
            
            # Get or create region
            try:
                region = Region.objects.get(name=region_name)
            except Region.DoesNotExist:
                self.stdout.write(f'⚠️  Region not found: {region_name}, skipping...')
                continue

            # Process each gender
            for gender, gender_data in region_info['data'].items():
                # Process each year
                for year_str, year_data in gender_data.items():
                    year = int(year_str)
                    
                    # Process age groups
                    total_from_sum = 0
                    total_record_value = year_data.get('total', 0)
                    
                    for age_str, population in year_data.items():
                        if age_str == 'total':
                            # Handle total record
                            age_min, age_max = 0, None
                        elif age_str.endswith('+'):
                            # Handle 85+ record
                            age_min = int(age_str[:-1])
                            age_max = None
                            total_from_sum += population
                        elif '-' in age_str:
                            # Handle regular age range
                            parts = age_str.split('-')
                            age_min, age_max = int(parts[0]), int(parts[1])
                            total_from_sum += population
                        else:
                            continue
                        
                        # Fix total if requested and there's a discrepancy
                        if age_str == 'total' and fix_totals and total_record_value != total_from_sum:
                            old_value = population
                            population = total_from_sum
                            validation_errors.append(
                                f'Fixed {region_name} {year} {gender} total: {old_value} → {population}'
                            )

                        # Create record
                        StatisticsData.objects.create(
                            region=region,
                            year=year,
                            age_min=age_min,
                            age_max=age_max,
                            gender=gender,
                            population=population
                        )
                        imported_count += 1
                    
                    # Check for validation errors
                    if not fix_totals and total_record_value != total_from_sum:
                        validation_errors.append(
                            f'{region_name} {year} {gender}: Total ({total_record_value:,}) != Sum ({total_from_sum:,}), Diff: {total_record_value - total_from_sum:,}'
                        )

        # Show results
        self.stdout.write(
            self.style.SUCCESS(f'✅ Imported {imported_count:,} records')
        )
        
        if validation_errors:
            self.stdout.write(f'\n⚠️  Validation issues found: {len(validation_errors)}')
            if fix_totals:
                self.stdout.write('✅ Fixed automatically:')
            else:
                self.stdout.write('❌ Issues detected:')
            
            for error in validation_errors[:10]:  # Show first 10
                self.stdout.write(f'   • {error}')
            
            if len(validation_errors) > 10:
                self.stdout.write(f'   ... and {len(validation_errors) - 10} more')
        else:
            self.stdout.write('✅ No validation errors found!')

        # Final verification
        final_count = StatisticsData.objects.count()
        self.stdout.write(f'\n📊 Final database state:')
        self.stdout.write(f'   - Total records: {final_count:,}')
        self.stdout.write(f'   - Years: {StatisticsData.objects.values("year").distinct().count()}')
        self.stdout.write(f'   - Regions: {StatisticsData.objects.values("region").distinct().count()}')
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Database rebuild completed successfully!')) 