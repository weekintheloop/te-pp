/**
 * @fileoverview AuthService.gs
 * @description Manages user authentication and permissions.
 * Secures the application by ensuring only authorized users can access and modify data.
 */

/**
 * Verifies a Google ID token from the frontend and checks user roles.
 * @param {string} googleToken - The Google ID token.
 * @returns {object} - An object containing user information and roles, or null if authentication fails.
 */
function authenticate(googleToken) {
    // In a real scenario, you would verify the Google ID token with Google's OAuth2 API.
    // For this Apps Script context, we'll simulate by checking the email against predefined sheets.
    // This assumes the googleToken somehow provides the user's email.
    // In a production environment, you'd use UrlFetchApp to call Google's tokeninfo endpoint.

    const userEmail = Session.getActiveUser().getEmail(); // Placeholder for actual token verification

    if (!userEmail) {
        return null; // No email found, authentication failed
    }

    const user = { email: userEmail, roles: [] };

    // Check if user is a Secretário
    const secretariosSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAMES.SECRETARIOS);
    if (secretariosSheet) {
        const secretariosEmails = secretariosSheet.getDataRange().getValues().flat();
        if (secretariosEmails.includes(userEmail)) {
            user.roles.push("Secretário");
        }
    }

    // Check if user is a Monitor
    const monitoresSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAMES.MONITORES);
    if (monitoresSheet) {
        const monitoresEmails = monitoresSheet.getDataRange().getValues().flat();
        if (monitoresEmails.includes(userEmail)) {
            user.roles.push("Monitor");
        }
    }

    if (user.roles.length === 0) {
        return null; // User not found in any role sheet
    }

    return user;
}

/**
 * Checks if a user has the necessary permission for an action.
 * @param {object} user - The user object (containing their roles).
 * @param {string} requiredPermission - The permission string (e.g., "manage_alunos", "view_rotas").
 * @returns {boolean} - True if the user has permission, false otherwise.
 */
function hasPermission(user, requiredPermission) {
    if (!user || !user.roles || user.roles.length === 0) {
        return false;
    }

    // Define a simple role-based permission matrix
    const permissionsMatrix = {
        "Secretário": [
            "manage_alunos", "view_alunos",
            "manage_rotas", "view_rotas",
            "manage_onibus", "view_onibus",
            "manage_monitores", "view_monitores",
            "manage_escolas", "view_escolas",
            "manage_pais", "view_pais",
            "manage_pontos_de_parada", "view_pontos_de_parada",
            "manage_ocorrencias", "view_ocorrencias",
            "manage_frequencia", "view_frequencia",
            "generate_reports",
            "admin_settings"
        ],
        "Monitor": [
            "view_alunos",
            "view_rotas",
            "view_onibus",
            "manage_frequencia",
            "manage_ocorrencias"
        ]
    };

    for (const role of user.roles) {
        if (permissionsMatrix[role] && permissionsMatrix[role].includes(requiredPermission)) {
            return true;
        }
    }

    return false;
}

/**
 * Initiates password recovery for a local account (if any).
 * NOTE: This implementation is a placeholder as the current system relies on Google Identity.
 * If local accounts were to be implemented, this would generate a token, store it, and send an email.
 * @param {string} email - The email of the user requesting password recovery.
 * @returns {boolean} - True if recovery initiated, false otherwise.
 */
function initiatePasswordRecovery(email) {
    console.warn("Password recovery for local accounts is not implemented as the system uses Google Identity.");
    // Placeholder for future implementation if local accounts are introduced.
    // Generate token, store with expiry, send email.
    return false;
}

/**
 * Resets password for a local account (if any).
 * NOTE: This implementation is a placeholder as the current system relies on Google Identity.
 * If local accounts were to be implemented, this would validate the token and update the password.
 * @param {string} token - The recovery token.
 * @param {string} newPassword - The new password.
 * @returns {boolean} - True if password reset, false otherwise.
 */
function resetPassword(token, newPassword) {
    console.warn("Password reset for local accounts is not implemented as the system uses Google Identity.");
    // Placeholder for future implementation if local accounts are introduced.
    // Validate token, update password.
    return false;
}


