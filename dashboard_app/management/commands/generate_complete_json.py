import json
import os
from collections import defaultdict, OrderedDict
from django.core.management.base import BaseCommand
from dashboard_app.models import Region, StatisticsData


class Command(BaseCommand):
    help = 'Generate complete JSON with all years and regions from current database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='dashboard_app/data/complete_demographics.json',
            help='Output JSON file path'
        )
        parser.add_argument(
            '--years',
            type=str,
            help='Comma-separated years to include (default: all years)'
        )
        parser.add_argument(
            '--compact',
            action='store_true',
            help='Generate compact JSON without indentation'
        )

    def handle(self, *args, **options):
        output_path = options['output']
        years_filter = options.get('years')
        compact = options.get('compact', False)
        
        # Parse years filter
        if years_filter:
            years = [int(y.strip()) for y in years_filter.split(',')]
        else:
            years = sorted(list(set(StatisticsData.objects.values_list('year', flat=True))))

        self.stdout.write(f'Generating JSON for {len(years)} years: {min(years)}-{max(years)}')

        # Generate complete data structure
        data = self.generate_complete_data(years)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write to file
        indent = None if compact else 2
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)

        file_size = os.path.getsize(output_path) / 1024  # KB
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Generated complete JSON: {output_path} ({file_size:.1f} KB)'
            )
        )
        
        # Print statistics
        total_regions = len(data['regions'])
        total_data_points = sum(
            len(region_data['data']) for region_data in data['regions'].values()
        )
        self.stdout.write(f'📊 Regions: {total_regions}')
        self.stdout.write(f'📊 Years: {len(years)}')
        self.stdout.write(f'📊 Data points: {total_data_points:,}')

    def generate_complete_data(self, years):
        """Generate complete data structure with all years"""
        
        # Get all age groups from database
        age_groups_raw = StatisticsData.objects.values_list('age_min', 'age_max').distinct()
        age_groups = []
        
        # Sort age groups properly, handling None values
        sorted_age_groups = sorted(age_groups_raw, key=lambda x: (x[0] or 0, x[1] or 999))
        
        for age_min, age_max in sorted_age_groups:
            if age_max is None:
                if age_min == 0:
                    continue  # Skip total records for age groups list
                else:
                    age_groups.append(f"{age_min}+")
            else:
                age_groups.append(f"{age_min}-{age_max}")
        
        # Build metadata
        data = {
            "metadata": {
                "version": "2.0",
                "generated_at": "2024-01-15",
                "description": "Complete demographic data for all regions and years",
                "years": years,
                "age_groups": age_groups,
                "genders": ["jami", "erkak", "ayol"],
                "total_years": len(years),
                "data_source": "stats-dashboard database export"
            },
            "regions": OrderedDict()
        }

        # Get all regions sorted by name
        regions = Region.objects.all().order_by('name')
        
        for region in regions:
            if not region.name:  # Skip empty region names
                continue
                
            self.stdout.write(f'Processing: {region.name}')
            
            region_data = {
                "svg_id": region.svg_id,
                "data": OrderedDict()
            }

            # Get all statistics for this region
            stats_query = StatisticsData.objects.filter(
                region=region,
                year__in=years
            ).order_by('gender', 'year', 'age_min')

            # Group by gender
            for gender in ['jami', 'erkak', 'ayol']:
                gender_stats = stats_query.filter(gender=gender)
                
                if not gender_stats.exists():
                    continue
                
                region_data["data"][gender] = OrderedDict()
                
                # Group by year
                for year in years:
                    year_stats = gender_stats.filter(year=year)
                    
                    if not year_stats.exists():
                        continue
                    
                    year_data = OrderedDict()
                    
                    # Add data in logical order: total first, then age groups
                    for stat in year_stats:
                        if stat.age_max is None and stat.age_min == 0:
                            # Total record
                            year_data["total"] = stat.population
                        elif stat.age_max is None:
                            # 85+ record
                            year_data[f"{stat.age_min}+"] = stat.population
                        else:
                            # Regular age range
                            year_data[f"{stat.age_min}-{stat.age_max}"] = stat.population
                    
                    if year_data:  # Only add if we have data
                        region_data["data"][gender][str(year)] = year_data

            # Only add region if it has data
            if region_data["data"]:
                data["regions"][region.name] = region_data
        
        return data 