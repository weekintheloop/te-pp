/**
 * @fileoverview GoogleMapsService.gs
 * @description A wrapper for the Google Maps API, handling API key management and requests for geocoding and route optimization.
 */

const GOOGLE_MAPS_API_KEY = PropertiesService.getScriptProperties().getProperty("GOOGLE_MAPS_API_KEY");

/**
 * Performs geocoding to convert an address into geographical coordinates (latitude and longitude).
 * @param {string} address - The address string to geocode.
 * @returns {object|null} - An object containing latitude and longitude, or null if geocoding fails.
 */
function geocodeAddress(address) {
    if (!GOOGLE_MAPS_API_KEY) {
        throw new Error("GOOGLE_MAPS_API_KEY is not set in Script Properties.");
    }

    const url = `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(address)}&key=${GOOGLE_MAPS_API_KEY}`;
    const response = UrlFetchApp.fetch(url);
    const json = JSON.parse(response.getContentText());

    if (json.status === "OK" && json.results.length > 0) {
        const location = json.results[0].geometry.location;
        return { lat: location.lat, lng: location.lng };
    } else {
        console.error(`Geocoding failed for address "${address}": ${json.status} - ${json.error_message || "No results"}`);
        return null;
    }
}

/**
 * Optimizes a route given an origin, destination, and optional waypoints.
 * @param {string} origin - The starting point of the route.
 * @param {string} destination - The ending point of the route.
 * @param {Array<string>} [waypoints=[]] - An array of intermediate points.
 * @returns {object|null} - An object containing route details (distance, duration, optimized waypoint order), or null if route optimization fails.
 */
function optimizeRoute(origin, destination, waypoints = []) {
    if (!GOOGLE_MAPS_API_KEY) {
        throw new Error("GOOGLE_MAPS_API_KEY is not set in Script Properties.");
    }

    let waypointsParam = "";
    if (waypoints.length > 0) {
        waypointsParam = `&waypoints=optimize:true|${waypoints.map(wp => encodeURIComponent(wp)).join("|")}`;
    }

    const url = `https://maps.googleapis.com/maps/api/directions/json?origin=${encodeURIComponent(origin)}&destination=${encodeURIComponent(destination)}${waypointsParam}&key=${GOOGLE_MAPS_API_KEY}`;
    const response = UrlFetchApp.fetch(url);
    const json = JSON.parse(response.getContentText());

    if (json.status === "OK" && json.routes.length > 0) {
        const route = json.routes[0];
        const leg = route.legs[0]; // Assuming a single leg for simplicity, or sum up all legs

        let totalDistanceMeters = 0;
        let totalDurationSeconds = 0;

        route.legs.forEach(l => {
            totalDistanceMeters += l.distance.value;
            totalDurationSeconds += l.duration.value;
        });

        return {
            distance: totalDistanceMeters,
            duration: totalDurationSeconds,
            optimizedWaypointOrder: route.waypoint_order,
            legs: route.legs,
            summary: route.summary,
        };
    } else {
        console.error(`Route optimization failed: ${json.status} - ${json.error_message || "No routes found"}`);
        return null;
    }
}

/**
 * Generates a Google Maps URL for a given route.
 * @param {string} origin - The starting point.
 * @param {string} destination - The ending point.
 * @param {Array<string>} [waypoints=[]] - Intermediate points.
 * @param {Array<number>} [optimizedOrder=[]] - Optional optimized order of waypoints.
 * @returns {string} - The Google Maps URL.
 */
function buildGoogleMapUrl(origin, destination, waypoints = [], optimizedOrder = []) {
    let url = `https://www.google.com/maps/dir/${encodeURIComponent(origin)}/`;

    let orderedWaypoints = waypoints;
    if (optimizedOrder.length > 0 && waypoints.length === optimizedOrder.length) {
        orderedWaypoints = optimizedOrder.map(index => waypoints[index]);
    }

    orderedWaypoints.forEach(point => {
        url += `${encodeURIComponent(point)}/`;
    });

    url += `${encodeURIComponent(destination)}/`;
    return url;
}


