import json
import csv
import os
from collections import defaultdict
from django.core.management.base import BaseCommand
from dashboard_app.models import Region, StatisticsData


class Command(BaseCommand):
    help = 'Export demographic data to various formats'

    def add_arguments(self, parser):
        parser.add_argument(
            '--format',
            type=str,
            choices=['json', 'csv', 'excel'],
            default='json',
            help='Export format'
        )
        parser.add_argument(
            '--output',
            type=str,
            help='Output file path'
        )
        parser.add_argument(
            '--year',
            type=int,
            help='Export specific year only'
        )

    def handle(self, *args, **options):
        format_type = options['format']
        output_path = options['output']
        year_filter = options.get('year')

        if format_type == 'json':
            self.export_json(output_path, year_filter)
        elif format_type == 'csv':
            self.export_csv(output_path, year_filter)
        elif format_type == 'excel':
            self.export_excel(output_path, year_filter)

    def export_json(self, output_path=None, year_filter=None):
        """Export data to JSON format"""
        if not output_path:
            output_path = 'exported_demographics.json'

        # Build data structure
        data = {
            "metadata": {
                "version": "1.0",
                "exported_at": "2024-01-15",
                "age_groups": ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80-84", "85+"],
                "genders": ["jami", "erkak", "ayol"]
            },
            "regions": {}
        }

        # Get all regions
        for region in Region.objects.all():
            region_data = {
                "svg_id": region.svg_id,
                "data": defaultdict(lambda: defaultdict(dict))
            }

            # Get statistics data
            stats_query = StatisticsData.objects.filter(region=region)
            if year_filter:
                stats_query = stats_query.filter(year=year_filter)

            for stat in stats_query:
                # Determine age group
                if stat.age_max is None and stat.age_min == 0:
                    age_group = "total"
                elif stat.age_max is None:
                    age_group = f"{stat.age_min}+"
                else:
                    age_group = f"{stat.age_min}-{stat.age_max}"

                region_data["data"][stat.gender][str(stat.year)][age_group] = stat.population

            data["regions"][region.name] = {
                "svg_id": region.svg_id,
                "data": dict(region_data["data"])
            }

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        self.stdout.write(
            self.style.SUCCESS(f'✅ Exported to {output_path}')
        )

    def export_csv(self, output_path=None, year_filter=None):
        """Export data to CSV format"""
        if not output_path:
            output_path = 'exported_demographics.csv'

        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['region', 'svg_id', 'year', 'gender', 'age_min', 'age_max', 'age_group', 'population']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # Get all statistics data
            stats_query = StatisticsData.objects.select_related('region')
            if year_filter:
                stats_query = stats_query.filter(year=year_filter)

            for stat in stats_query:
                # Determine age group
                if stat.age_max is None and stat.age_min == 0:
                    age_group = "total"
                elif stat.age_max is None:
                    age_group = f"{stat.age_min}+"
                else:
                    age_group = f"{stat.age_min}-{stat.age_max}"

                writer.writerow({
                    'region': stat.region.name,
                    'svg_id': stat.region.svg_id,
                    'year': stat.year,
                    'gender': stat.gender,
                    'age_min': stat.age_min,
                    'age_max': stat.age_max or '',
                    'age_group': age_group,
                    'population': stat.population
                })

        self.stdout.write(
            self.style.SUCCESS(f'✅ Exported to {output_path}')
        ) 