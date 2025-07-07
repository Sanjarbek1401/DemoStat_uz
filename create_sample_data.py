import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from dashboard_app.models import Region, StatisticsData

# Age ranges to generate data for
AGE_RANGES = [
    (0, 4), (5, 9), (10, 14), (15, 19), (20, 24), 
    (25, 29), (30, 34), (35, 39), (40, 44), (45, 49),
    (50, 54), (55, 59), (60, 64), (65, 69), (70, 74),
    (75, 79), (80, 84), (85, None)
]

# Genders to generate data for
GENDERS = ['jami', 'erkak', 'ayol']

# Base populations by region (roughly based on Uzbekistan demographics)
BASE_POPULATIONS = {
    'Toshkent': 2500000,
    'Toshkent viloyati': 2900000,
    'Andijon': 3000000,
    'Buxoro': 1900000,
    'Farg\'ona': 3600000,
    'Jizzax': 1300000,
    'Namangan': 2700000,
    'Navoiy': 1000000,
    'Qashqadaryo': 3100000,
    'Samarqand': 3800000,
    'Sirdaryo': 800000,
    'Surxondaryo': 2500000,
    'Xorazm': 1800000,
    'Qoraqalpog\'iston Respublikasi': 1900000,
}

def create_sample_data(years=(2025,)):
    """Create sample statistics data for the given years"""
    # Get all regions
    regions = Region.objects.all()
    
    if not regions:
        print("No regions found. Please run initialize_regions.py first.")
        return
    
    for year in years:
        print(f"Generating data for year {year}...")
        
        for region in regions:
            # Get base population for this region
            base_pop = BASE_POPULATIONS.get(region.name, 1000000)
            
            # Create total ("jami") data based on age ranges
            for age_min, age_max in AGE_RANGES:
                # Calculate a population for this age range
                if age_max:
                    age_factor = 0.8 - (age_min / 100)  # Younger ages have more people
                    pop_range = int(base_pop * age_factor * 0.05)  # 5% of population per range
                else:
                    # 85+ has fewer people
                    pop_range = int(base_pop * 0.01)
                
                # Add some randomness
                pop_range = max(1000, int(pop_range * random.uniform(0.8, 1.2)))
                
                # Create record for total population (jami)
                StatisticsData.objects.create(
                    region=region,
                    year=year,
                    age_min=age_min,
                    age_max=age_max,
                    gender='jami',
                    population=pop_range
                )
                
                # Create gender-specific records (roughly 50/50 split)
                male_pop = int(pop_range * random.uniform(0.48, 0.52))
                female_pop = pop_range - male_pop
                
                StatisticsData.objects.create(
                    region=region,
                    year=year,
                    age_min=age_min,
                    age_max=age_max,
                    gender='erkak',
                    population=male_pop
                )
                
                StatisticsData.objects.create(
                    region=region,
                    year=year,
                    age_min=age_min,
                    age_max=age_max,
                    gender='ayol',
                    population=female_pop
                )
                
        print(f"Data generation complete for year {year}")

if __name__ == "__main__":
    # Check if data already exists
    if StatisticsData.objects.exists():
        # Automatically delete existing data
        StatisticsData.objects.all().delete()
        print("Existing data deleted.")
    
    # Generate data for years -2050 in 5-year increments
    create_sample_data(years=[, 2030, 2035, 2040, 2045, 2050])
    print(f"Total records created: {StatisticsData.objects.count()}")
