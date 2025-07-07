from django.core.management.base import BaseCommand
from dashboard_app.models import Region, StatisticsData, RepublicStatistics
from django.db.models import Sum

class Command(BaseCommand):
    help = 'Copy Respublika statistics from StatisticsData to RepublicStatistics.'

    def handle(self, *args, **options):
        try:
            republic_region = Region.objects.get(svg_id='respublika')
        except Region.DoesNotExist:
            self.stderr.write(self.style.ERROR("Respublika regioni topilmadi (svg_id='respublika')."))
            return

        years = StatisticsData.objects.filter(region=republic_region).values_list('year', flat=True).distinct()
        total_created = 0
        for year in years:
            total_population = StatisticsData.objects.filter(
                region=republic_region, year=year, gender='jami'
            ).aggregate(total=Sum('population'))['total'] or 0

            stats = StatisticsData.objects.filter(region=republic_region, year=year, gender='jami')
            for stat in stats:
                age_min = stat.age_min
                age_max = stat.age_max if stat.age_max is not None else 85
                age_population = stat.population
                obj, created = RepublicStatistics.objects.update_or_create(
                    year=year,
                    age_min=age_min,
                    age_max=age_max,
                    defaults={
                        'total_population': total_population,
                        'age_population': age_population
                    }
                )
                total_created += int(created)
                self.stdout.write(f"{year} {age_min}-{age_max}: {age_population} (Jami: {total_population})")
        self.stdout.write(self.style.SUCCESS(f"Ko'chirish tugadi! Yangi yoki yangilangan yozuvlar: {total_created}")) 