/**
 * Uzbekistan SVG Map Handler
 * Handles loading, customizing and interacting with the Uzbekistan SVG map
 */

class UzbekistanMap {
    constructor(containerId, onClickCallback) {
        this.containerId = containerId;
        this.container = d3.select(`#${containerId}`);
        this.svgContainer = null;
        this.regions = [];
        this.activeRegion = null;
        this.onRegionClickCallback = onClickCallback;
        this.isInitialized = false;
        this.tooltip = null;
        this.regionData = {}; // Store data for each region
        
        // Define color palette for regions - these are distinct colors
        this.colorPalette = [
            '#f94144', '#f3722c', '#f8961e', '#f9c74f', '#90be6d',
            '#43aa8b', '#577590', '#277da1', '#577590', '#4d908e',
            '#43aa8b', '#90be6d', '#f9c74f', '#f9844a', '#f8961e'
        ];
    }

    /**
     * Initialize the map
     */
    async init() {
        const success = await this.loadMap();
        if (success) {
            this.isInitialized = true;
        }
        return success;
    }

    /**
     * Load the SVG map from local file
     */
    async loadMap() {
        try {
            // Load the SVG map from local file path
            const response = await fetch('/static/images/uz.svg');
            const svgText = await response.text();
            
            // Insert the SVG into the container
            this.container.html(svgText);
            
            // Get reference to the SVG
            this.svgContainer = this.container.select('svg');
            
            // Apply some basic styling and configuration
            this.svgContainer
                .attr('width', '100%')
                .attr('height', '100%')
                .attr('preserveAspectRatio', 'xMidYMid meet');
            
            // Initialize regions
            this.initializeRegions();
            
            return true;
        } catch (error) {
            console.error('Error loading Uzbekistan map:', error);
            return false;
        }
    }
    
    /**
     * Initialize map regions with interactivity
     */
    initializeRegions() {
        // Create tooltip div if it doesn't exist
        if (!this.tooltip) {
            this.tooltip = d3.select('body')
                .append('div')
                .attr('class', 'region-tooltip')
                .style('opacity', 0);
        }
        
        // Get all path elements (regions) from the SVG
        const regionPaths = this.svgContainer.selectAll('path');
        
        // Store regions data and add interactivity to path elements
        regionPaths.each((d, i, nodes) => {
            const path = d3.select(nodes[i]);
            const id = path.attr('id');
            
            if (id) {
                const colorIndex = i % this.colorPalette.length;
                let regionColor = this.colorPalette[colorIndex];
                // Override Farg'ona color to dark green
                if (id === 'fergana') {
                    regionColor = '#006400'; // dark green
                }
                // Override Toshkent color to light onyx
                if (id === 'tashkent') {
                    regionColor = '#A2A2A1'; // light onyx
                }
                // Override Namangan color to Peach
                if (id === 'namangan') {
                    regionColor = '#FFDAB9'; // Peach
                }
                // Override Andijon color to grey
                if (id === 'andijan') {
                    regionColor = '#808080'; // grey
                }
                // Override Buxoro color to light Hazel
                if (id === 'bukhara') {
                    regionColor = '#C9B273'; // light Hazel
                }
                // Override Jizzax color to teal
                if (id === 'jizzakh') {
                    regionColor = '#008080'; // teal
                }
                this.regions.push({
                    id: id,
                    element: path,
                    name: id.replace(/_/g, ' '),
                    color: regionColor
                });
                
                // Add base class and set unique color
                path.classed('region', true)
                    .style('fill', regionColor);
                
                // Add hover handlers
                path.on('mouseover', (event) => {
                    this.showTooltip(event, id);
                })
                .on('mousemove', (event) => {
                    this.moveTooltip(event);
                })
                .on('mouseout', () => {
                    this.hideTooltip();
                });
                
                // Add click handler
                path.on('click', (event) => {
                    if (this.onRegionClickCallback) {
                        this.onRegionClickCallback(id);
                    }
                });
            }
        });
        
        // Add hover functionality to circle elements (region label points)
        // This ensures hovering over a circle label also shows the tooltip
        const labelPointsGroup = this.svgContainer.select('#label_points');
        if (labelPointsGroup.node()) {
            const circles = labelPointsGroup.selectAll('circle');
            
            circles.each((d, i, nodes) => {
                const circle = d3.select(nodes[i]);
                const id = circle.attr('id');
                
                if (id) {
                    // Add hover handlers to circle elements
                    circle.on('mouseover', (event) => {
                        this.showTooltip(event, id);
                    })
                    .on('mousemove', (event) => {
                        this.moveTooltip(event);
                    })
                    .on('mouseout', () => {
                        this.hideTooltip();
                    });
                    
                    // Add click handler
                    circle.on('click', (event) => {
                        if (this.onRegionClickCallback) {
                            this.onRegionClickCallback(id);
                        }
                    });
                }
            });
        }
    }
    
    /**
     * Show tooltip with region data
     */
    showTooltip(event, regionId) {
        const region = this.regions.find(r => r.id === regionId);
        const data = this.regionData[regionId] || {};
        // Format the region name with proper capitalization
        const regionName = data.name || (region ? region.name : regionId);
        // Only show the region name in the tooltip
        let tooltipContent = `<div class="tooltip-header">${regionName}</div>`;
        this.tooltip.html(tooltipContent)
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 28) + 'px')
            .style('opacity', 1);
    }
    
    /**
     * Move tooltip with mouse
     */
    moveTooltip(event) {
        this.tooltip
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 28) + 'px');
    }
    
    /**
     * Hide tooltip
     */
    hideTooltip() {
        this.tooltip.style('opacity', 0);
    }
    
    /**
     * Select/highlight a region
     */
    selectRegion(regionId) {
        // Remove active class from previously selected region
        if (this.activeRegion) {
            this.svgContainer.select(`#${this.activeRegion}`)
                .classed('active', false);
        }
        
        // Add active class to newly selected region
        const regionElement = this.svgContainer.select(`#${regionId}`);
        if (!regionElement.empty()) {
            regionElement.classed('active', true);
            // Update active region
            this.activeRegion = regionId;
        }
    }
    
    /**
     * Set region color based on density category
     * With our new coloring system, we'll modify the opacity based on density
     */
    setRegionDensity(regionId, densityCategory) {
        // Skip if regionId is empty or invalid
        if (!regionId || regionId === '') {
            console.warn('Attempted to set density for region with empty ID');
            return;
        }
        
        const regionElement = this.svgContainer.select(`#${regionId}`);
        if (!regionElement.empty()) {
            // Get the region from our stored regions
            const region = this.regions.find(r => r.id === regionId);
            if (region) {
                // Adjust opacity based on density category (1-4)
                const baseColor = region.color;
                const opacity = 0.4 + (densityCategory * 0.15); // Ranges from 0.4 to 1.0
                
                // Apply the color with adjusted opacity
                regionElement.style('fill-opacity', opacity);
            }
            
            // Store density category for tooltips
            if (!this.regionData[regionId]) {
                this.regionData[regionId] = {};
            }
            this.regionData[regionId].densityCategory = densityCategory;
            
            // Ensure active region stays highlighted
            if (regionId === this.activeRegion) {
                regionElement.classed('active', true);
            }
        }
    }
    
    /**
     * Update data for a specific region (used for tooltips)
     */
    updateRegionData(regionId, data) {
        // Skip if regionId is empty or invalid
        if (!regionId || regionId === '') {
            console.warn('Attempted to update data for region with empty ID');
            return;
        }
        
        if (!this.regionData[regionId]) {
            this.regionData[regionId] = {};
        }
        
        // Merge the new data with existing data
        this.regionData[regionId] = {
            ...this.regionData[regionId],
            ...data
        };
    }
    
    /**
     * Handle window resize
     */
    resize() {
        if (this.svgContainer) {
            // You can add specific resize handling if needed
            // For now, the SVG is already set to 100% width and height
            // with preserveAspectRatio so it should handle resize naturally
        }
    }
    
    /**
     * Clear active region selection
     */
    clearSelection() {
        if (this.activeRegion) {
            this.svgContainer.select(`#${this.activeRegion}`)
                .classed('active', false);
            this.activeRegion = null;
        }
    }
    
    /**
     * Get the ID of the currently active region
     */
    getActiveRegion() {
        return this.activeRegion;
    }
}
