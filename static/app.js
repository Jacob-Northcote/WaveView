// SurfWave AI Frontend Application
class SurfWaveApp {
    constructor() {
        this.currentLocation = null;
        this.currentData = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.checkServerHealth();
    }

    bindEvents() {
        // Location selector
        const locationSelect = document.getElementById('location-select');
        const analyzeBtn = document.getElementById('analyze-btn');
        const rankingsBtn = document.getElementById('rankings-btn');

        analyzeBtn.addEventListener('click', () => this.analyzeLocation());
        rankingsBtn.addEventListener('click', () => this.getRankings());

        // Enable analyze button when location is selected
        locationSelect.addEventListener('change', (e) => {
            this.currentLocation = e.target.value;
            analyzeBtn.disabled = !this.currentLocation;
        });
    }

    async checkServerHealth() {
        try {
            const response = await fetch('/api/health');
            if (response.ok) {
                console.log('Server is healthy');
            } else {
                console.error('Server health check failed');
            }
        } catch (error) {
            console.error('Server health check error:', error);
        }
    }

    async analyzeLocation() {
        if (!this.currentLocation) {
            this.showError('Please select a location first');
            return;
        }

        this.showLoading(true);
        this.hideResults();

        try {
            // Get surf data
            const surfData = await this.fetchSurfData(this.currentLocation);
            
            // Get AI analysis
            const analysis = await this.fetchAnalysis(this.currentLocation);
            
            // Display results
            this.displayResults(surfData, analysis);
            
        } catch (error) {
            console.error('Analysis error:', error);
            this.showError('Failed to analyze surf conditions. Please try again.');
        } finally {
            this.showLoading(false);
        }
    }

    async fetchSurfData(locationId) {
        const response = await fetch(`/api/surf-data/${locationId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    }

    async fetchAnalysis(locationId) {
        const response = await fetch(`/api/analysis/${locationId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    }

    async getRankings() {
        const rankingsBtn = document.getElementById('rankings-btn');
        const rankingsContent = document.getElementById('rankings-content');
        
        rankingsBtn.disabled = true;
        rankingsBtn.textContent = 'Loading...';
        
        try {
            const response = await fetch('/api/rankings');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            this.displayRankings(data.rankings);
            
        } catch (error) {
            console.error('Rankings error:', error);
            this.showError('Failed to load rankings. Please try again.');
        } finally {
            rankingsBtn.disabled = false;
            rankingsBtn.textContent = 'Get Current Rankings';
        }
    }

    displayResults(surfData, analysis) {
        // Update surf data display
        this.updateSurfStats(surfData);
        
        // Update analysis display
        this.updateAnalysis(analysis);
        
        // Update wave visualization
        this.updateWaveVisualization(surfData, analysis);
        
        // Show results
        this.showResults();
    }

    updateSurfStats(surfData) {
        document.getElementById('wave-height').textContent = surfData.wave_height;
        document.getElementById('wave-period').textContent = surfData.wave_period;
        document.getElementById('wave-direction').textContent = surfData.wave_direction;
        document.getElementById('wind-speed').textContent = surfData.wind_speed;
        document.getElementById('wind-direction').textContent = surfData.wind_direction;
        document.getElementById('temperature').textContent = surfData.temperature;
        document.getElementById('tide-height').textContent = surfData.tide_height;
        
        // Calculate and display quality score
        const qualityScore = this.calculateQualityScore(surfData);
        document.getElementById('quality-score').textContent = Math.round(qualityScore);
    }

    updateAnalysis(analysis) {
        const analysisContent = document.getElementById('analysis-content');
        analysisContent.textContent = analysis.analysis || 'No analysis available';
    }

    updateWaveVisualization(surfData, analysis) {
        const waveViz = document.getElementById('wave-visualization');
        
        // Extract ASCII wave art from analysis
        const analysisText = analysis.analysis || '';
        const waveArt = this.extractWaveArt(analysisText, surfData.wave_height);
        
        waveViz.innerHTML = `
            <div class="wave-art">
                ${waveArt}
            </div>
            <div class="wave-info">
                <p><strong>Wave Height:</strong> ${surfData.wave_height} feet</p>
                <p><strong>Wave Period:</strong> ${surfData.wave_period} seconds</p>
                <p><strong>Direction:</strong> ${surfData.wave_direction}</p>
            </div>
        `;
    }

    extractWaveArt(analysisText, waveHeight) {
        // Look for ASCII art patterns in the analysis
        const lines = analysisText.split('\n');
        let waveArt = '';
        let inWaveSection = false;
        
        for (const line of lines) {
            // Check if line contains wave-like characters
            if (line.includes('~') || line.includes('/') || line.includes('\\') || 
                line.includes('|') || line.includes('_') || line.includes('(') || 
                line.includes(')') || line.includes('*')) {
                waveArt += line + '\n';
                inWaveSection = true;
            } else if (inWaveSection && line.trim() === '') {
                break;
            }
        }
        
        // If no wave art found, generate a simple one based on wave height
        if (!waveArt.trim()) {
            waveArt = this.generateSimpleWaveArt(waveHeight);
        }
        
        return waveArt;
    }

    generateSimpleWaveArt(waveHeight) {
        const height = Math.max(3, Math.min(8, Math.round(waveHeight / 2)));
        let art = '';
        
        // Generate wave based on height
        for (let i = 0; i < height; i++) {
            const spaces = ' '.repeat(height - i);
            const waveChars = '~'.repeat(i * 2 + 1);
            art += spaces + waveChars + '\n';
        }
        
        // Add wave base
        art += ' '.repeat(height - 1) + '___' + '\n';
        
        return art;
    }

    displayRankings(rankings) {
        const rankingsContent = document.getElementById('rankings-content');
        
        if (!rankings || rankings.length === 0) {
            rankingsContent.innerHTML = '<p>No rankings available</p>';
            rankingsContent.classList.remove('hidden');
            return;
        }
        
        let html = '';
        rankings.forEach((ranking, index) => {
            const medal = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : `${index + 1}.`;
            html += `
                <div class="ranking-item">
                    <div class="ranking-info">
                        <span class="ranking-medal">${medal}</span>
                        <span class="ranking-name">${ranking.location_name}</span>
                    </div>
                    <div class="ranking-stats">
                        <span class="ranking-height">${ranking.wave_height}ft</span>
                        <span class="ranking-score">${Math.round(ranking.quality_score)}/100</span>
                    </div>
                </div>
            `;
        });
        
        rankingsContent.innerHTML = html;
        rankingsContent.classList.remove('hidden');
    }

    calculateQualityScore(surfData) {
        let score = 0;
        
        // Wave height factor (optimal range: 3-8 feet)
        const waveHeight = surfData.wave_height;
        if (3.0 <= waveHeight && waveHeight <= 8.0) {
            score += 30;
        } else if (2.0 <= waveHeight && waveHeight <= 10.0) {
            score += 20;
        } else {
            score += 10;
        }
        
        // Wave period factor (optimal range: 10-16 seconds)
        const wavePeriod = surfData.wave_period;
        if (10.0 <= wavePeriod && wavePeriod <= 16.0) {
            score += 25;
        } else if (8.0 <= wavePeriod && wavePeriod <= 18.0) {
            score += 15;
        } else {
            score += 5;
        }
        
        // Wind factor (lower is better for most spots)
        const windSpeed = surfData.wind_speed;
        if (windSpeed <= 10.0) {
            score += 25;
        } else if (windSpeed <= 15.0) {
            score += 15;
        } else {
            score += 5;
        }
        
        // Swell consistency factor
        const swellHeight = surfData.swell_height;
        const swellPeriod = surfData.swell_period;
        if (swellHeight >= 3.0 && swellPeriod >= 10.0) {
            score += 20;
        } else {
            score += 10;
        }
        
        return Math.min(score, 100.0);
    }

    showLoading(show) {
        const loading = document.getElementById('loading');
        if (show) {
            loading.classList.remove('hidden');
        } else {
            loading.classList.add('hidden');
        }
    }

    showResults() {
        const results = document.getElementById('results');
        results.classList.remove('hidden');
    }

    hideResults() {
        const results = document.getElementById('results');
        results.classList.add('hidden');
    }

    showError(message) {
        // Create a simple error notification
        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ff6b6b;
            color: white;
            padding: 1rem;
            border-radius: 8px;
            z-index: 1000;
            max-width: 300px;
        `;
        errorDiv.textContent = message;
        
        document.body.appendChild(errorDiv);
        
        // Remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new SurfWaveApp();
});

