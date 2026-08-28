// ============================================
// GLOBAL VARIABLES
// ============================================

let allLocations = [];

let markers = [];


// ============================================
// CREATE MAP
// ============================================

const map = L.map("map").setView(
    [25.5, 92.5],
    6
);


// ============================================
// MAP TILES
// ============================================

L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        attribution:
            "&copy; OpenStreetMap contributors"
    }
).addTo(map);


// ============================================
// RISK COLORS
// ============================================

function getRiskColor(risk) {

    if (risk === "VERY HIGH") {

        return "#c62828";

    }

    if (risk === "HIGH") {

        return "#ef6c00";

    }

    if (risk === "MODERATE") {

        return "#f9a825";

    }

    return "#2e7d32";

}


// ============================================
// LOAD RISK DATA
// ============================================

async function loadRiskData() {

    const status =
        document.getElementById("status");


    try {

        status.innerText =
            "Loading risk data...";


        const response =
            await fetch("/risk-map");


        if (!response.ok) {

            throw new Error(
                "Failed to load risk data"
            );

        }


        const data =
            await response.json();


        console.log(
            "Risk data:",
            data
        );


        // Store locations globally

        allLocations =
            data.locations;


        // Populate filters

        populateStateFilter();

        populateDistrictFilter();


        // Display locations

        displayLocations(
            allLocations
        );


        status.innerText =
            data.count +
            " locations monitored";


    }

    catch (error) {

        console.error(error);


        status.innerText =
            "Unable to load risk data";

    }

}


// ============================================
// STATE FILTER
// ============================================

function populateStateFilter() {

    const stateFilter =
        document.getElementById(
            "stateFilter"
        );


    const states =
        [
            ...new Set(
                allLocations.map(
                    location =>
                        location.state
                )
            )
        ]
        .sort();


    states.forEach(
        function(state) {

            const option =
                document.createElement(
                    "option"
                );


            option.value =
                state;

            option.textContent =
                state;


            stateFilter.appendChild(
                option
            );

        }
    );

}


// ============================================
// DISTRICT FILTER
// ============================================

function populateDistrictFilter(
    selectedState = "ALL"
) {

    const districtFilter =
        document.getElementById(
            "districtFilter"
        );


    // Clear old options

    districtFilter.innerHTML = `

        <option value="ALL">
            All Districts
        </option>

    `;


    let locations =
        allLocations;


    // If a state is selected

    if (
        selectedState !== "ALL"
    ) {

        locations =
            locations.filter(
                location =>
                    location.state ===
                    selectedState
            );

    }


    const districts =
        [
            ...new Set(
                locations.map(
                    location =>
                        location.district
                )
            )
        ]
        .sort();


    districts.forEach(
        function(district) {

            const option =
                document.createElement(
                    "option"
                );


            option.value =
                district;

            option.textContent =
                district;


            districtFilter.appendChild(
                option
            );

        }
    );

}


// ============================================
// DISPLAY LOCATIONS
// ============================================

function displayLocations(
    locations
) {

    // Remove old markers

    markers.forEach(
        function(marker) {

            map.removeLayer(
                marker
            );

        }
    );


    markers = [];


    // Add new markers

    locations.forEach(
        function(location) {

            const color =
                getRiskColor(
                    location.risk
                );


            const marker =
                L.circleMarker(
                    [
                        location.latitude,
                        location.longitude
                    ],
                    {

                        radius: 7,

                        fillColor:
                            color,

                        color:
                            "#ffffff",

                        weight: 1,

                        fillOpacity:
                            0.85

                    }
                );

            location.marker = marker;

            marker.addTo(map);


            // Click event

            marker.on(
                "click",
                function() {

                    showDetails(
                        location
                    );

                }
            );


            markers.push(
                marker
            );

        }
    );

}


// ============================================
// APPLY FILTERS
// ============================================

function applyFilters() {

    const state =
        document.getElementById(
            "stateFilter"
        ).value;


    const district =
        document.getElementById(
            "districtFilter"
        ).value;


    const risk =
        document.getElementById(
            "riskFilter"
        ).value;


    let filtered =
        allLocations;


    // State filter

    if (state !== "ALL") {

        filtered =
            filtered.filter(
                location =>
                    location.state ===
                    state
            );

    }


    // District filter

    if (district !== "ALL") {

        filtered =
            filtered.filter(
                location =>
                    location.district ===
                    district
            );

    }


    // Risk filter

    if (risk !== "ALL") {

        filtered =
            filtered.filter(
                location =>
                    location.risk ===
                    risk
            );

    }


    // Display filtered markers

    displayLocations(
        filtered
    );


    // Update status

    document.getElementById(
        "status"
    ).innerText =
        filtered.length +
        " locations shown";

}


// ============================================
// STATE CHANGE
// ============================================

document.getElementById(
    "stateFilter"
).addEventListener(
    "change",
    function() {

        const state =
            this.value;


        // Rebuild districts

        populateDistrictFilter(
            state
        );


        // Reset district

        document.getElementById(
            "districtFilter"
        ).value = "ALL";


        applyFilters();

    }
);


// ============================================
// DISTRICT CHANGE
// ============================================

document.getElementById(
    "districtFilter"
).addEventListener(
    "change",
    function() {

        applyFilters();

    }
);


// ============================================
// RISK CHANGE
// ============================================

document.getElementById(
    "riskFilter"
).addEventListener(
    "change",
    function() {

        applyFilters();

    }
);


// ============================================
// SHOW LOCATION DETAILS
// ============================================

async function showDetails(location) {

    const details =
        document.getElementById("details");


    // Show basic information first

    details.innerHTML = `

        <div class="risk-card">

            <h3>
                ${location.district},
                ${location.state}
            </h3>

            <p>
                Latitude:
                ${location.latitude.toFixed(5)}
            </p>

            <p>
                Longitude:
                ${location.longitude.toFixed(5)}
            </p>

            <div class="risk-value">
                ${location.probability}%
            </div>

            <p>
                Landslide probability
            </p>

            <h3>
                Risk:
                ${location.risk}
            </h3>

            <hr>

            <div class="weather-section">
                <h3>Current Weather</h3>

                <p>🌡️ Temperature: <span id="temperature">Loading...</span> °C</p>
                <p>💧 Humidity: <span id="humidity">Loading...</span> %</p>
                <p>🌧️ Current Rain: <span id="current-rain">Loading...</span> mm</p>

                <h3>Rainfall Forecast</h3>

                <p>🌧️ Next 24 hours: <span id="rainfall-24h">Loading...</span> mm</p>
                <p>☔ Rain probability: <span id="rain-probability">Loading...</span> %</p>
            </div>

        </div>

    `;


    try {

        const response = await fetch(
            `/weather?latitude=${location.latitude}&longitude=${location.longitude}`
        );


        if (!response.ok) {

            throw new Error(
                "Weather request failed"
            );

        }


        const weather =
            await response.json();

        // Calculate combined risk
        let finalRisk = location.risk;

        const rainfall = weather.rainfall_next_24h;
        const rainProbability = weather.max_rain_probability;

        if (rainfall >= 20 && rainProbability >= 70) {

            if (location.risk === "LOW") {
                finalRisk = "MODERATE";
            } 
            else if (location.risk === "MODERATE") {
                finalRisk = "HIGH";
            } 
            else if (location.risk === "HIGH") {
                finalRisk = "VERY HIGH";
            }

        }
        else if (rainfall >= 10 && rainProbability >= 50) {

            if (location.risk === "LOW") {
                finalRisk = "MODERATE";
            }

        }        
        // Update marker color based on final weather-adjusted risk
        if (location.marker) {

        location.marker.setStyle({
            fillColor: getRiskColor(finalRisk)
        });

        }

        // Display weather

        details.innerHTML = `

            <div class="risk-card">

                <h3>
                    ${location.district},
                    ${location.state}
                </h3>


                <p>
                    Latitude:
                    ${location.latitude.toFixed(5)}
                </p>


                <p>
                    Longitude:
                    ${location.longitude.toFixed(5)}
                </p>


                <div class="risk-value">
                    ${location.probability}%
                </div>


                <p>
                    Landslide probability
                </p>


                <h3>
                    Risk:
                    ${finalRisk}
                </h3>


                <hr>


                <h3>
                    Current Weather
                </h3>


                <p>
                    🌡️ Temperature:
                    ${weather.temperature} °C
                </p>


                <p>
                    💧 Humidity:
                    ${weather.humidity} %
                </p>


                <p>
                    🌧️ Current Rain:
                    ${weather.current_rain} mm
                </p>


                <h3>
                    Rainfall Forecast
                </h3>


                <p>
                    🌧️ Next 24 hours:
                    ${weather.rainfall_next_24h} mm
                </p>


                <p>
                    ☔ Rain probability:
                    ${weather.max_rain_probability} %
                </p>

                <hr>

                <h3>⚠️ Weather Alert</h3>

                <p>
                    ${
                        weather.rainfall_next_24h >= 20 && weather.max_rain_probability >= 70
                            ? "🚨 HIGH WEATHER ALERT: Heavy rainfall is likely in the next 24 hours. Landslide risk may increase significantly."
                            : weather.rainfall_next_24h >= 10 && weather.max_rain_probability >= 50
                            ? "⚠️ MODERATE WEATHER ALERT: Significant rainfall is possible in the next 24 hours."
                            : "✅ LOW WEATHER ALERT: No significant rainfall threat detected."
                    }
                </p>

            </div>

        `;

    }

    catch (error) {

        console.error(
            "Weather error:",
            error
        );


        details.innerHTML += `

            <p>
                ⚠️ Weather data unavailable.
            </p>

        `;

    }

}


// ============================================
// START APPLICATION
// ============================================

loadRiskData();