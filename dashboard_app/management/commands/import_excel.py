import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from dashboard_app.models import Region, StatisticsData


class Command(BaseCommand):
    help = 'Import demographic data from Excel file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            required=True,
            help='Path to Excel file'
        )
        parser.add_argument(
            '--sheet',
            type=str,
            default='Sheet1',
            help='Excel sheet name'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before import'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        sheet_name = options['sheet']
        
        try:
            # Read Excel file
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Validate required columns
            required_columns = ['region', 'year', 'gender', 'age_group', 'population']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise CommandError(f'Missing columns: {missing_columns}')

            if options['clear']:
                self.stdout.write('Clearing existing data...')
                StatisticsData.objects.all().delete()

            self.import_data(df)
            
        except FileNotFoundError:
            raise CommandError(f'File not found: {file_path}')
        except Exception as e:
            raise CommandError(f'Error processing Excel file: {e}')

    def import_data(self, df):
        """Import data from DataFrame"""
        imported_count = 0
        
        with transaction.atomic():
            for _, row in df.iterrows():
                # Get or create region
                region, created = Region.objects.get_or_create(
                    name=row['region'],
                    defaults={'svg_id': self.get_svg_id(row['region'])}
                )
                
                # Parse age group
                age_min, age_max = self.parse_age_group(row['age_group'])
                
                # Create or update record
                record, created = StatisticsData.objects.update_or_create(
                    region=region,
                    year=int(row['year']),
                    age_min=age_min,
                    age_max=age_max,
                    gender=row['gender'],
                    defaults={'population': int(row['population'])}
                )
                
                if created:
                    imported_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'✅ Imported {imported_count} records')
        )

    def parse_age_group(self, age_group_str):
        """Parse age group string to min/max values"""
        age_group = str(age_group_str).strip()
        
        if age_group.lower() in ['total', 'all']:
            return 0, None
        elif age_group.endswith('+'):
            return int(age_group[:-1]), None
        elif '-' in age_group:
            parts = age_group.split('-')
            return int(parts[0]), int(parts[1])
        else:
            # Single age
            return int(age_group), int(age_group)

    def get_svg_id(self, region_name):
        """Get SVG ID for region"""
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
        return svg_id_map.get(region_name, region_name.lower().replace(' ', '_')) 