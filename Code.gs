/**
 * @fileoverview Code.gs
 * @description Main server-side script for the Google Apps Script web application.
 * Handles web app requests, includes HTML files, and exposes server-side functions to the frontend.
 */

/**
 * Handles GET requests to the web application.
 * This function is the entry point for the web app.
 * @returns {HtmlOutput} - The HTML content to be served.
 */
function doGet(e) {
  // Check if the user is authenticated
  const userEmail = Session.getActiveUser().getEmail();
  if (!userEmail) {
    return HtmlService.createTemplateFromFile("Login.html").evaluate();
  }

  // You might want to check roles here and redirect to NotAuthorized.html if needed
  // For now, we'll assume any logged-in user can access the main app.
  // const user = authenticate(null); // In a real scenario, this would involve token verification
  // if (!user) {
  //   return HtmlService.createTemplateFromFile("Login.html").evaluate();
  // }

  // Serve the main application HTML
  return HtmlService.createTemplateFromFile("Index.html")
      .evaluate()
      .setTitle("SIG-TE Dashboard")
      .addMetaTag("viewport", "width=device-width, initial-scale=1");
}

/**
 * Includes an HTML file into another HTML file.
 * This is a common pattern in Google Apps Script to modularize HTML.
 * @param {string} filename - The name of the HTML file to include (without .html extension).
 * @returns {HtmlTemplate} - The evaluated HTML template.
 */
function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}

// Expose server-side functions to the frontend via google.script.run
// These functions will be called from JavaScript.html or main.js

/**
 * Example function to get all students.
 * @returns {Array} - List of student objects.
 */
function getAllAlunos() {
  // Implement permission check
  // if (!hasPermission(Session.getActiveUser().getEmail(), "view_alunos")) {
  //   throw new Error("User not authorized to view students.");
  // }
  return getByEntity("Aluno");
}

/**
 * Example function to create a student.
 * @param {object} studentData - The data for the new student.
 * @returns {object} - The created student object.
 */
function createAluno(studentData) {
  // Implement permission check
  // if (!hasPermission(Session.getActiveUser().getEmail(), "manage_alunos")) {
  //   throw new Error("User not authorized to create students.");
  // }
  return create("Aluno", studentData);
}

/**
 * Example function to get a single student by ID.
 * @param {number} id - The ID of the student.
 * @returns {object} - The student object.
 */
function getAlunoById(id) {
  return getById("Aluno", id);
}

/**
 * Example function to update a student.
 * @param {number} id - The ID of the student to update.
 * @param {object} studentData - The data to update.
 * @returns {object} - The updated student object.
 */
function updateAluno(id, studentData) {
  return update("Aluno", id, studentData);
}

/**
 * Example function to soft delete a student.
 * @param {number} id - The ID of the student to delete.
 * @returns {object} - The deleted student object.
 */
function deleteAluno(id) {
  return deleteRecord("Aluno", id);
}

// Add other entity CRUD functions as needed (Rotas, Onibus, etc.)

/**
 * Function to get all sheet names for dynamic form generation.
 * @returns {object} - An object containing all sheet names.
 */
function getSheetNames() {
  return SHEET_NAMES;
}

/**
 * Function to get schema for a given entity.
 * @param {string} entityName - The name of the entity.
 * @returns {object} - The schema object for the entity.
 */
function getEntitySchema(entityName) {
  return getSchema(entityName);
}

/**
 * Function to get sheet headers for a given sheet name.
 * @param {string} sheetName - The name of the sheet.
 * @returns {Array<string>} - An array of header strings.
 */
function getSheetHeadersForSheet(sheetName) {
  return getSheetHeaders(sheetName);
}

/**
 * Function to get user authentication status and roles.
 * @returns {object|null} - User object with email and roles, or null if not authenticated.
 */
function getUserAuthInfo() {
  const userEmail = Session.getActiveUser().getEmail();
  if (!userEmail) {
    return null;
  }
  // In a real scenario, you'd pass a token to authenticate, but for Apps Script,
  // we'll simulate by checking roles based on the active user's email.
  return authenticate(null); // Pass null as token for simulation
}

/**
 * Function to initiate password recovery (placeholder).
 * @param {string} email - User's email.
 * @returns {boolean} - Success status.
 */
function requestPasswordRecovery(email) {
  return initiatePasswordRecovery(email);
}

/**
 * Function to reset password (placeholder).
 * @param {string} token - Recovery token.
 * @param {string} newPassword - New password.
 * @returns {boolean} - Success status.
 */
function performPasswordReset(token, newPassword) {
  return resetPassword(token, newPassword);
}

// Include other service functions that need to be exposed to the frontend
// For example, from GoogleMapsService, GeminiReportService, etc.

/**
 * Geocodes an address using Google Maps Service.
 * @param {string} address - The address to geocode.
 * @returns {object} - Geocoding results.
 */
function geocodeAddressFromMaps(address) {
  return geocodeAddress(address);
}

/**
 * Optimizes a route using Google Maps Service.
 * @param {string} origin - Origin address.
 * @param {string} destination - Destination address.
 * @param {Array<string>} waypoints - Array of waypoint addresses.
 * @returns {object} - Optimized route details.
 */
function optimizeRouteFromMaps(origin, destination, waypoints) {
  return optimizeRoute(origin, destination, waypoints);
}

/**
 * Builds a Google Map URL for visualization.
 * @param {string} origin - Origin address.
 * @param {string} destination - Destination address.
 * @param {Array<string>} waypoints - Array of waypoint addresses.
 * @param {Array<number>} optimizedOrder - Optimized order of waypoints.
 * @returns {string} - Google Maps URL.
 */
function buildGoogleMapUrlFromMaps(origin, destination, waypoints, optimizedOrder) {
  return buildGoogleMapUrl(origin, destination, waypoints, optimizedOrder);
}

/**
 * Generates a diagnostic report using Gemini Report Service.
 * @returns {string} - The generated report.
 */
function generateDiagnosticReportFromGemini() {
  return generateDiagnosticReport();
}

/**
 * Generates an entity summary using Gemini Report Service.
 * @param {string} entityName - The name of the entity.
 * @param {number} id - The ID of the entity record.
 * @returns {string} - The generated summary.
 */
function generateEntitySummaryFromGemini(entityName, id) {
  return generateEntitySummary(entityName, id);
}

/**
 * Analyzes critical routes using Critical Routes Service.
 * @returns {Array} - List of critical routes.
 */
function analyzeCriticalRoutesFromService() {
  return analyzeCriticalRoutes();
}

/**
 * Creates a notification using Notification Service.
 * @param {string} type - Type of notification.
 * @param {string} message - Notification message.
 * @param {string} recipient - Recipient of the notification.
 * @param {object} details - Additional details.
 * @returns {boolean} - Success status.
 */
function createNotificationFromService(type, message, recipient, details) {
  return createNotification(type, message, recipient, details);
}

/**
 * Checks for pending attestations using Notification Service (placeholder).
 * @returns {Array} - List of pending attestations.
 */
function checkPendingAttestationsFromService() {
  return checkPendingAttestations();
}

/**
 * Placeholder for Absence Analysis Service function.
 * @returns {Array} - List of students at risk.
 */
function getStudentsAtRisk() {
  return analyzeAbsencePatterns();
}

// Functions for scheduled tasks (if needed to be triggered manually or viewed)
function adjustScheduleTrigger() {
  // This function would typically be called once during setup or by an admin.
  // For web app exposure, it might be used to show current triggers or allow manual adjustment.
  // It's not meant to be called frequently by the frontend.
  Logger.log("adjustScheduleTrigger called. This function manages time-based triggers.");
  // Example: You might return current trigger info or a success message.
  return "Schedule trigger adjustment initiated (check logs for details).";
}

function respondToHourlyTrigger() {
  // This function is designed to be called by a time-based trigger, not directly by the frontend.
  // Exposing it here is mainly for completeness or if an admin needs to manually run it.
  Logger.log("respondToHourlyTrigger called. This function processes hourly tasks.");
  // Example: You might return a status message.
  return "Hourly tasks processed (check logs for details).";
}


