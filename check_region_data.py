#!/usr/bin/env python
import os
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from dashboard_app.models import Region, StatisticsData

# List of regions to check
regions = ['Toshkent', 'Sirdaryo', 'Surxondaryo', 'Samarqand']

print("Checking data for regions:")
print("--------------------------")

for r_name in regions:
    try:
        r = Region.objects.get(name=r_name)
        count = StatisticsData.objects.filter(region=r).count()
        print(f"{r_name}: {count} data points, svg_id={r.svg_id}")
    except Region.DoesNotExist:
        print(f"{r_name}: Region not found in database")
