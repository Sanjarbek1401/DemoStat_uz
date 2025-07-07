from django.core.management.base import BaseCommand
from django.db.models import Sum, Count
from django.db import models
from dashboard_app.models import Region, StatisticsData


class Command(BaseCommand):
    help = 'Validate demographic data consistency'

    def add_arguments(self, parser):
        parser.add_argument(
            '--year',
            type=int,
            help='Validate specific year only'
        )
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Attempt to fix validation errors'
        )

    def handle(self, *args, **options):
        year_filter = options.get('year')
        fix_errors = options.get('fix', False)
        
        total_errors = 0
        
        self.stdout.write('🔍 Validating demographic data...\n')

        # Check 1: Missing age groups
        total_errors += self.check_missing_age_groups(year_filter)
        
        # Check 2: Total vs individual age groups consistency
        total_errors += self.check_total_consistency(year_filter, fix_errors)
        
        # Check 3: Duplicate records
        total_errors += self.check_duplicates(fix_errors)
        
        # Check 4: Invalid age ranges
        total_errors += self.check_invalid_ages()

        # Summary
        if total_errors == 0:
            self.stdout.write(
                self.style.SUCCESS('✅ All validation checks passed!')
            )
        else:
            self.stdout.write(
                self.style.ERROR(f'❌ Found {total_errors} validation errors')
            )

    def check_missing_age_groups(self, year_filter=None):
        """Check for missing age groups in each region/year/gender combination"""
        errors = 0
        expected_age_groups = 18  # 17 individual + 1 total
        
        query = StatisticsData.objects.values('region', 'year', 'gender').distinct()
        if year_filter:
            query = query.filter(year=year_filter)

        for combo in query:
            count = StatisticsData.objects.filter(**combo).count()
            if count < expected_age_groups:
                errors += 1
                region_name = Region.objects.get(id=combo['region']).name
                self.stdout.write(
                    self.style.WARNING(
                        f'⚠️  {region_name} {combo["year"]} {combo["gender"]}: '
                        f'Only {count}/{expected_age_groups} age groups'
                    )
                )
        
        return errors

    def check_total_consistency(self, year_filter=None, fix_errors=False):
        """Check if total records match sum of individual age groups"""
        errors = 0
        
        query = StatisticsData.objects.values('region', 'year', 'gender').distinct()
        if year_filter:
            query = query.filter(year=year_filter)

        for combo in query:
            # Get total record
            total_record = StatisticsData.objects.filter(
                **combo, age_min=0, age_max__isnull=True
            ).first()
            
            if not total_record:
                continue
                
            # Sum individual age groups
            individual_sum = StatisticsData.objects.filter(
                **combo, age_max__isnull=False
            ).aggregate(total=Sum('population'))['total'] or 0
            
            difference = abs(total_record.population - individual_sum)
            if difference > 1:  # Allow for rounding errors
                errors += 1
                region_name = Region.objects.get(id=combo['region']).name
                self.stdout.write(
                    self.style.ERROR(
                        f'❌ {region_name} {combo["year"]} {combo["gender"]}: '
                        f'Total ({total_record.population:,}) != Sum ({individual_sum:,}), '
                        f'Difference: {difference:,}'
                    )
                )
                
                if fix_errors:
                    # Update total to match individual sum
                    total_record.population = individual_sum
                    total_record.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✅ Fixed: Updated total to {individual_sum:,}')
                    )
        
        return errors

    def check_duplicates(self, fix_errors=False):
        """Check for duplicate records"""
        errors = 0
        
        # Find duplicates
        duplicates = StatisticsData.objects.values(
            'region', 'year', 'age_min', 'age_max', 'gender'
        ).annotate(
            count=Count('id')
        ).filter(count__gt=1)
        
        for dup in duplicates:
            errors += 1
            region_name = Region.objects.get(id=dup['region']).name
            age_range = f"{dup['age_min']}-{dup['age_max']}" if dup['age_max'] else f"{dup['age_min']}+"
            
            self.stdout.write(
                self.style.ERROR(
                    f'❌ Duplicate: {region_name} {dup["year"]} {age_range} {dup["gender"]} '
                    f'({dup["count"]} records)'
                )
            )
            
            if fix_errors:
                # Keep the first record, delete others
                records = StatisticsData.objects.filter(
                    region_id=dup['region'],
                    year=dup['year'],
                    age_min=dup['age_min'],
                    age_max=dup['age_max'],
                    gender=dup['gender']
                )
                first_record = records.first()
                records.exclude(id=first_record.id).delete()
                self.stdout.write(
                    self.style.SUCCESS(f'  ✅ Fixed: Removed {dup["count"]-1} duplicate(s)')
                )
        
        return errors

    def check_invalid_ages(self):
        """Check for invalid age ranges"""
        errors = 0
        
        # Check for invalid age ranges
        invalid_ages = StatisticsData.objects.filter(
            age_min__lt=0
        ) | StatisticsData.objects.filter(
            age_max__lt=0
        ) | StatisticsData.objects.filter(
            age_min__gt=150
        ) | StatisticsData.objects.filter(
            age_max__gt=150
        )
        
        for record in invalid_ages:
            errors += 1
            self.stdout.write(
                self.style.ERROR(
                    f'❌ Invalid age range: {record.region.name} {record.year} '
                    f'{record.age_min}-{record.age_max} {record.gender}'
                )
            )
        
        return errors 