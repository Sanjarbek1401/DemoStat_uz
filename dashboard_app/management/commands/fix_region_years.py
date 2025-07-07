from django.core.management.base import BaseCommand
from dashboard_app.models import Region, StatisticsData
from django.db import transaction

class Command(BaseCommand):
    help = "Shift year by +1 for specific regions' statistics (Samarqand, Surxondaryo, Sirdaryo, Toshkent) without affecting other data."

    TARGET_REGIONS = [
        'Samarqand',
        'Surxondaryo',
        'Sirdaryo',
        'Toshkent',
    ]

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Shifting years by +1 for regions: %s' % ', '.join(self.TARGET_REGIONS)))
        regions = Region.objects.filter(name__in=self.TARGET_REGIONS)
        count = 0
        for region in regions:
            stats = StatisticsData.objects.filter(region=region)
            for stat in stats:
                old_year = stat.year
                stat.year = old_year - 1
                stat.save(update_fields=['year'])
                count += 1
                self.stdout.write(f"{region.name}: {old_year} -> {stat.year}")
        self.stdout.write(self.style.SUCCESS(f"Done. Shifted {count} records.")) 