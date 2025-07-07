/**
 * Uzbekistan Statistics Dashboard
 * Main application script handling API calls and visualization
 */

$(document).ready(function() {
    // State variables
    let selectedYear = 2026;
    let selectedGender = 'jami';
    let selectedRegion = 'respublika';
    let minAge = 0;
    let maxAge = 85;
    
    // Initialize map
    const uzMap = new UzbekistanMap('map', mapRegionClickHandler);
    uzMap.init();
    
    // Initialize controls
    initializeControls();
    
    // Initial data load
    refreshData();
    
    // Note: 'respublika' represents country-level data, not a specific region on the map
    // We don't visually select it since there's no corresponding SVG element
    
    /**
     * Initialize all interactive controls
     */
    function initializeControls() {
        // Year slider
        $('#year-slider').on('input', function() {
            let year = parseInt($(this).val());
            selectedYear = year;
            $('.current-year').text(selectedYear);
            refreshData();
            updateRepublicOverlayFromAPI(year, minAge, maxAge);
        });
        
        // Gender buttons
        $('.gender-btn').on('click', function() {
            $('.gender-btn').removeClass('active');
            $(this).addClass('active');
            selectedGender = $(this).data('gender');
            refreshData();
        });
        
        const ageBrackets = {
            0: 4, 5: 9, 10: 14, 15: 19, 20: 24, 25: 29, 30: 34,
            35: 39, 40: 44, 45: 49, 50: 54, 55: 59, 60: 64, 65: 69,
            70: 74, 75: 79, 80: 84, 85: 85
        };

        // Age range sliders with "snap" functionality
        $('#age-min-slider').on('input', function() {
            minAge = parseInt($(this).val());
            
            // Snap max-age to the corresponding bracket end
            if (ageBrackets[minAge] !== undefined) {
                maxAge = ageBrackets[minAge];
                $('#age-max-slider').val(maxAge);
            } else {
                // If minAge is not a bracket start, ensure max is at least min
                if (minAge > maxAge) {
                    maxAge = minAge;
                    $('#age-max-slider').val(maxAge);
                }
            }
            
            updateAgeRangeLabel();
            refreshData();
            updateRepublicOverlayFromAPI(selectedYear, minAge, maxAge);
        });
        
        $('#age-max-slider').on('input', function() {
            maxAge = parseInt($(this).val());
            
            // Ensure max is not less than min
            if (maxAge < minAge) {
                $('#age-min-slider').val(maxAge);
                minAge = maxAge;
            }
            
            updateAgeRangeLabel();
            refreshData();
            updateRepublicOverlayFromAPI(selectedYear, minAge, maxAge);
        });
    }
    
    /**
     * Update the age range label
     */
    function updateAgeRangeLabel() {
        let rangeText = `${minAge}-${maxAge === 85 ? '85+' : maxAge}`;
        $('.current-age-range').text(rangeText);
    }
    
    /**
     * Refresh data from API based on selected filters
     */
    function refreshData() {
        // Build API URL with parameters using start_date and end_date instead of year
        // Using January 1st of the selected year as start_date and December 31st as end_date
        const startDate = `${selectedYear}-01-01`;
        const endDate = `${selectedYear}-12-31`;
        
        let url = `/api/statistics?start_date=${startDate}&end_date=${endDate}&gender=${selectedGender}`;
        
        // Add region filter if a region is selected
        if (selectedRegion) {
            url += `&region=${selectedRegion}`;
        }
        
        // Add age range parameters
        url += `&min_age=${minAge}&max_age=${maxAge}`;
        
        // Fetch statistics based on selected filters
        fetch(url)
            .then(response => response.json())
            .then(data => {
                updateMapColors(data);
                updateCountryStats(data);
                updateRepublicInfoOverlay(data);
                
                // Always update republic overlay with proper total population (0-85)
                updateRepublicOverlayFromAPI(selectedYear, minAge, maxAge);
                
                if (selectedRegion) {
                    showRegionInfo(data);
                } else {
                    hideRegionInfo();
                }
            })
            .catch(error => console.error('Error fetching data:', error));
    }
    
    /**
     * Region click handler
     */
    function mapRegionClickHandler(regionId) {
        if (selectedRegion === regionId) {
            // Deselect if clicking the same region again
            selectedRegion = null;
            hideRegionInfo();
        } else {
            selectedRegion = regionId;
            uzMap.selectRegion(regionId);
            // Don't show info here, wait for data refresh
        }
        refreshData();
    }
    
    /**
     * Update map colors based on population data
     */
    function updateMapColors(data) {
        // Update map region colors based on population density categories
        for (const region of data.regions) {
            // Skip regions with invalid or empty svg_id
            if (!region.svg_id || region.svg_id === '') {
                console.warn(`Region '${region.name}' has no SVG ID, skipping map update`);
                continue;
            }
            
            // Update region data for tooltips
            uzMap.updateRegionData(region.svg_id, {
                name: region.name,
                population: region.population,
                youth_population: region.youth_population,
                children_population: region.children_population
            });
            
            // Set region density (affects color opacity)
            uzMap.setRegionDensity(region.svg_id, region.density_category);
        }
    }
    
    /**
     * Update country-wide statistics
     */
    function updateCountryStats(data) {
        $('.country-total-population').text(data.total_population.toLocaleString());
        $('.country-youth-population').text(data.youth_population.toLocaleString());
        $('.country-children-population').text(data.children_population ? data.children_population.toLocaleString() : 'N/A');
    }
    
    /**
     * Show region information overlay
     */
    function showRegionInfo(data) {
        // Find the selected region's data
        const region = data.regions.find(r => r.svg_id === selectedRegion);
        if (region && region.svg_id !== 'respublika') {
            $('.region-header').text(region.name);
            
            // Fetch total population (0-85) for this region separately
            fetchRegionTotalPopulation(selectedRegion);
            
            // Update age range label for region overlay
            let ageLabel = `${minAge}-${maxAge === 85 ? '85+' : maxAge}`;
            $('.region-age-range').text(ageLabel + ' yoshlilar');
            
            // For "Shundan", show the filtered age range population
            $('.region-youth').text(region.population ? region.population.toLocaleString() : 'N/A');
            // Show/hide gender-specific stats
            if (selectedGender === 'jami' && region.male_population && region.female_population) {
                $('.region-male').text(region.male_population.toLocaleString());
                $('.region-female').text(region.female_population.toLocaleString());
                $('.gender-stats').show();
            } else {
                $('.gender-stats').hide();
            }
            $('.region-info-overlay').show();
            // If this is the respublika (country-wide) region, don't highlight any specific region on the map
            if (selectedRegion === 'respublika') {
                uzMap.clearSelection();
            }
        } else {
            // Agar respublika tanlansa yoki region topilmasa, overlayni yashiramiz
            hideRegionInfo();
        }
    }
    
    /**
     * Fetch total population (0-85) for a specific region
     */
    function fetchRegionTotalPopulation(regionId) {
        const startDate = `${selectedYear}-01-01`;
        const endDate = `${selectedYear}-12-31`;
        const url = `/api/statistics?start_date=${startDate}&end_date=${endDate}&gender=${selectedGender}&region=${regionId}&min_age=0&max_age=85`;
        
        fetch(url)
            .then(response => response.json())
            .then(data => {
                const region = data.regions.find(r => r.svg_id === regionId);
                if (region) {
                    $('.region-total').text(region.population.toLocaleString());
                }
            })
            .catch(error => {
                console.error('Error fetching region total population:', error);
                $('.region-total').text('Error');
            });
    }
    
    /**
     * Hide region information overlay
     */
    function hideRegionInfo() {
        $('.region-info-overlay').hide();
    }
    
    // Handle window resize
    $(window).resize(function() {
        // Redraw map if needed
        uzMap.resize();
    });

    // Faqat Respublika info overlay-ni yangilash uchun funksiya
    function updateRepublicInfoOverlay(data) {
        if (!data || !data.regions) return;
        // Respublika ma'lumotini topamiz
        const republic = data.regions.find(r => r.svg_id === 'respublika');
        if (republic) {
            // Don't update republic_total_population here - it should always show 0-85 total
            // This will be handled by updateRepublicOverlayFromAPI()
            
            // Yosh oralig'i va qiymatini filterga moslab chiqarish
            let ageLabel = `${minAge}-${maxAge === 85 ? '85+' : maxAge}`;
            $('.republic-age-range').text(ageLabel + ' yoshlilar');
            
            // For "Shundan", show the filtered age range population
            $('.republic-youth').text(republic.population ? republic.population.toLocaleString() : 'N/A');
        }
    }

    // Cache for total population data to avoid redundant API calls
    let totalPopulationCache = {
        year: null,
        gender: null,
        data: null
    };
    
    function updateRepublicOverlayFromAPI(year, minAge, maxAge) {
        const startDate = `${year}-01-01`;
        const endDate = `${year}-12-31`;
        
        // Check if we already have cached total population data for this year and gender
        const cacheIsValid = totalPopulationCache.year === year && 
                             totalPopulationCache.gender === selectedGender && 
                             totalPopulationCache.data !== null;
        
        // Function to update the age-specific data display
        function updateAgeSpecificData() {
            // If viewing the full range (0-85), use the cached total data
            if (minAge === 0 && maxAge === 85) {
                $('.republic-age-range').text('0-85+ yoshlilar');
                $('.republic-youth').text(totalPopulationCache.data.total_population.toLocaleString());
            } else {
                // For specific age ranges, calculate from the age groups in the cached data
                const ageRangeText = `${minAge}-${maxAge === 85 ? '85+' : maxAge}`;
                $('.republic-age-range').text(ageRangeText + ' yoshlilar');
                
                let agePopulation = 0;
                totalPopulationCache.data.age_groups.forEach(function(group) {
                    const range = group.range;
                    let groupMinAge, groupMaxAge;
                    if (range.endsWith('+')) {
                        groupMinAge = parseInt(range);
                        groupMaxAge = 200; // yuqori limit, realda yetarli
                    } else {
                        const rangeParts = range.split('-');
                        groupMinAge = parseInt(rangeParts[0]);
                        groupMaxAge = parseInt(rangeParts[1]);
                    }
                    // Diapazonlar to'g'ri kesishishini tekshirish
                    if (
                        (groupMinAge >= minAge && groupMinAge <= maxAge) ||
                        (groupMaxAge >= minAge && groupMaxAge <= maxAge) ||
                        (groupMinAge <= minAge && groupMaxAge >= maxAge)
                    ) {
                        agePopulation += group.population;
                    }
                });
                
                $('.republic-youth').text(agePopulation.toLocaleString());
            }
        }
        
        // If we have valid cached data, use it directly
        if (cacheIsValid) {
            $('.republic_total_population').text(totalPopulationCache.data.total_population.toLocaleString());
            updateAgeSpecificData();
        } else {
            // Otherwise, fetch the full range data and cache it
            const url = `/api/statistics?start_date=${startDate}&end_date=${endDate}&gender=${selectedGender}&region=respublika&min_age=0&max_age=85`;
            
            $.get(url, function(data) {
                // Cache the data
                totalPopulationCache = {
                    year: year,
                    gender: selectedGender,
                    data: data
                };
                
                // Update the display
                $('.republic_total_population').text(data.total_population.toLocaleString());
                updateAgeSpecificData();
            });
        }
    }
});

/**
 * Format numbers with comma separators
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/**
 * Format numbers with comma separators
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}

/**
 * Show loading state while fetching data
 */
function showLoadingState() {
    // Could add spinners or loading indicators here
}

/**
 * Show error state if data loading fails
 */
function showErrorState() {
    // Could show error messages here
    $('#total-population').text('Error');
    $('#youth-population').text('Error');
}
