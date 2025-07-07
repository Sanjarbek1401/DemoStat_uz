from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum, Q
from django.views.decorators.http import require_GET
from django.core.cache import cache

from .models import Region, StatisticsData, PdfResource, RepublicStatistics

def dashboard(request):
    """Main dashboard view"""
    context = {
        'regions': Region.objects.all(),
        'current_page': 'home'
    }
    return render(request, 'dashboard/index.html', context)
    
def about(request):
    """About page view"""
    context = {
        'current_page': 'about'
    }
    return render(request, 'dashboard/about.html', context)

def resources(request):
    """Resources page view"""
    pdfs = PdfResource.objects.order_by('-uploaded_at')
    context = {
        'pdfs': pdfs,
        'current_page': 'resources'
    }
    return render(request, 'dashboard/resources.html', context)

def pdf_detail(request, pk):
    pdf = get_object_or_404(PdfResource, pk=pk)
    return render(request, 'dashboard/pdf_detail.html', {'pdf': pdf})

@require_GET
def get_regions(request):
    """Get all regions data for the map"""
    # Cache regions data for 1 hour
    cache_key = 'regions_data'
    regions = cache.get(cache_key)
    
    if regions is None:
        regions = list(Region.objects.values('id', 'name', 'svg_id'))
        cache.set(cache_key, regions, 3600)  # 1 hour
    
    return JsonResponse({'regions': regions})

@require_GET
def get_statistics(request):
    """Get statistics data based on filters - OPTIMIZED VERSION"""
    
    # Parse parameters with proper defaults
    params = parse_request_parameters(request)
    
    # Build base query
    base_query = StatisticsData.objects.filter(
        year=params['year'],
        gender=params['gender']
    )
    
    # Add region filter if specified
    if params['region_id']:
        base_query = base_query.filter(region__svg_id=params['region_id'])
    
    # Get age-filtered data
    age_filtered_data = get_age_filtered_statistics(
        base_query, 
        params['min_age'], 
        params['max_age']
    )
    
    # Get region-specific data
    region_data = get_region_statistics(
        params['year'], 
        params['gender'], 
        params['min_age'], 
        params['max_age']
    )
    
    # Build response
    response_data = {
        'total_population': age_filtered_data['total_population'],
        'youth_population': age_filtered_data['youth_population'],
        'children_population': age_filtered_data['children_population'],
        'age_groups': age_filtered_data['age_groups'],
        'regions': region_data,
        'year': params['year'],
        'gender': params['gender_display'],
        'min_age': params['min_age'],
        'max_age': params['max_age']
    }
    
    return JsonResponse(response_data)

def parse_request_parameters(request):
    """Parse and validate request parameters"""
    # Get date parameters with defaults
    start_date = request.GET.get('start_date', '2025-01-01')
    gender = request.GET.get('gender', 'both')
    
    # Extract year from start_date
    try:
        year = int(start_date.split('-')[0])
    except (ValueError, IndexError):
        year = 2025
    
    # Handle region filter
    region_id = request.GET.get('region_id') or request.GET.get('region')
    
    # Handle age range filter
    try:
        min_age = int(request.GET.get('min_age', 0))
        max_age = int(request.GET.get('max_age', 85))
    except (TypeError, ValueError):
        min_age = 0
        max_age = 85
    
    # Convert gender parameter to database value
    gender_map = {
        'male': 'erkak',
        'female': 'ayol',
        'both': 'jami',
        'jami': 'jami'
    }
    db_gender = gender_map.get(gender, 'jami')
    
    return {
        'year': year,
        'gender': db_gender,
        'gender_display': gender,
        'region_id': region_id,
        'min_age': min_age,
        'max_age': max_age
    }

def get_age_filtered_statistics(base_query, min_age, max_age):
    """Get statistics filtered by age range - UNIVERSAL LOGIC"""
    age_ranges = [
        (0, 4), (5, 9), (10, 14), (15, 19), (20, 24), (25, 29),
        (30, 34), (35, 39), (40, 44), (45, 49), (50, 54), (55, 59),
        (60, 64), (65, 69), (70, 74), (75, 79), (80, 84), (85, None)
    ]
    relevant_ranges = []
    for age_min, age_max_range in age_ranges:
        if age_max_range is None:
            if max_age >= 85 and min_age <= 85:
                relevant_ranges.append((age_min, age_max_range))
        elif age_min <= max_age and age_max_range >= min_age:
            relevant_ranges.append((age_min, age_max_range))

    total_population = 0
    age_groups = []
    for age_min, age_max_range in relevant_ranges:
        if age_max_range is None:
            age_query = base_query.filter(age_min=age_min, age_max__isnull=True)
            range_label = f"{age_min}+"
        else:
            age_query = base_query.filter(age_min=age_min, age_max=age_max_range)
            range_label = f"{age_min}-{age_max_range}"
        population = age_query.aggregate(total=Sum('population'))['total'] or 0
        age_groups.append({'range': range_label, 'population': population})
        total_population += population

    youth_population = base_query.filter(
        age_min=20, age_max=24
    ).aggregate(total=Sum('population'))['total'] or 0

    children_population = base_query.filter(
        age_min__gte=0, age_max__lte=14
    ).aggregate(total=Sum('population'))['total'] or 0

    return {
        'total_population': total_population,
        'youth_population': youth_population,
        'children_population': children_population,
        'age_groups': age_groups
    }

def get_region_statistics(year, gender, min_age, max_age):
    """Get statistics by region - UNIVERSAL LOGIC"""
    cache_key = f'region_stats_{year}_{gender}_{min_age}_{max_age}'
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return cached_data

    age_ranges = [
        (0, 4), (5, 9), (10, 14), (15, 19), (20, 24), (25, 29),
        (30, 34), (35, 39), (40, 44), (45, 49), (50, 54), (55, 59),
        (60, 64), (65, 69), (70, 74), (75, 79), (80, 84), (85, None)
    ]
    relevant_ranges = []
    for age_min, age_max_range in age_ranges:
        if age_max_range is None:
            if max_age >= 85 and min_age <= 85:
                relevant_ranges.append((age_min, age_max_range))
        elif age_min <= max_age and age_max_range >= min_age:
            relevant_ranges.append((age_min, age_max_range))

    region_data = []
    for region in Region.objects.all():
        # Base query for the specific region and year
        base_query = StatisticsData.objects.filter(
            region=region,
            year=year
        )

        # Apply age range filters
        age_filter = Q()
        for age_min_val, age_max_val in relevant_ranges:
            if age_max_val is None:
                age_filter |= Q(age_min=age_min_val, age_max__isnull=True)
            else:
                age_filter |= Q(age_min=age_min_val, age_max=age_max_val)
        
        filtered_query = base_query.filter(age_filter)
        
        # Calculate populations
        total_population = 0
        male_population = 0
        female_population = 0

        if gender == 'jami':
            total_population = filtered_query.filter(gender='jami').aggregate(total=Sum('population'))['total'] or 0
            male_population = filtered_query.filter(gender='erkak').aggregate(total=Sum('population'))['total'] or 0
            female_population = filtered_query.filter(gender='ayol').aggregate(total=Sum('population'))['total'] or 0
        else:
            total_population = filtered_query.filter(gender=gender).aggregate(total=Sum('population'))['total'] or 0

        youth_query = base_query.filter(age_min=20, age_max=24)
        children_query = base_query.filter(age_min__gte=0, age_max__lte=14)
        
        youth_population = (youth_query.filter(gender=gender).aggregate(total=Sum('population'))['total'] or 0)
        children_population = (children_query.filter(gender=gender).aggregate(total=Sum('population'))['total'] or 0)

        density_category = get_density_category(total_population)

        region_data.append({
            'id': region.id,
            'name': region.name,
            'svg_id': region.svg_id,
            'population': total_population,
            'male_population': male_population,
            'female_population': female_population,
            'youth_population': youth_population,
            'children_population': children_population,
            'density_category': density_category
        })
    cache.set(cache_key, region_data, 1800)
    return region_data

def get_density_category(population):
    """Calculate density category based on population"""
    if population == 0:
        return 0  # No data
    elif population < 1000000:
        return 1  # Low density
    elif population < 2000000:
        return 2  # Medium density
    elif population < 3000000:
        return 3  # High density
    else:
        return 4  # Very high density

def republic_stats_api(request):
    year = int(request.GET.get('year', 2026))
    age_min = int(request.GET.get('min_age', 0))
    age_max = int(request.GET.get('max_age', 85))
    try:
        stats = RepublicStatistics.objects.get(year=year, age_min=age_min, age_max=age_max)
        data = {
            'republic_total_population': stats.total_population,
            'republic_age_population': stats.age_population,
            'age_range': f'{age_min}-{age_max}',
        }
    except RepublicStatistics.DoesNotExist:
        data = {
            'republic_total_population': 0,
            'republic_age_population': 0,
            'age_range': f'{age_min}-{age_max}',
        }
    return JsonResponse(data)
