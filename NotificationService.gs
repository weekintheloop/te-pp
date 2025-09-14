/**
 * @fileoverview NotificationService.gs
 * @description Handles creation of notifications and proactive checks.
 */

/**
 * Creates a notification entry (e.g., in a 'Notificacoes' sheet or sends an email).
 * This is a generic function that can be adapted based on notification requirements.
 * @param {string} type - Type of notification (e.g., 'alert', 'warning', 'info').
 * @param {string} message - The notification message.
 * @param {string} recipient - The recipient's email or ID.
 * @param {object} [details={}] - Additional details for the notification.
 */
function createNotification(type, message, recipient, details = {}) {
    console.log(`New Notification: Type=${type}, Message=${message}, Recipient=${recipient}, Details=${JSON.stringify(details)}`);

    // Example: Send an email notification
    try {
        MailApp.sendEmail(recipient, `SIG-TE Notification: ${type.toUpperCase()}`, message);
        console.log(`Email notification sent to ${recipient}`);
    } catch (e) {
        console.error(`Failed to send email notification to ${recipient}: ${e.message}`);
    }

    // In a real system, you might also log this to a 'Notifications' sheet
    // DataManager.create('Notificacoes', { Type: type, Message: message, Recipient: recipient, Timestamp: new Date(), ...details });
}

/**
 * Proactively checks for pending attestations and sends notifications.
 * This is a placeholder and would require a 'Atestados' sheet with status.
 */
function checkPendingAttestations() {
    console.warn("checkPendingAttestations is a placeholder. Requires 'Atestados' sheet and logic.");

    // Example: Check for attestations older than X days that are still 'Pending'
    // const pendingAttestations = DataManager.getByEntity('Atestados', { filter: { Status: 'Pending' } });
    // pendingAttestations.forEach(attestation => {
    //     const attestationDate = new Date(attestation.DataEnvio);
    //     const now = new Date();
    //     const diffTime = Math.abs(now - attestationDate);
    //     const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    //     if (diffDays > 7) { // Attestation pending for more than 7 days
    //         createNotification(
    //             'alert',
    //             `Atestado do aluno ${attestation.AlunoNome} está pendente há ${diffDays} dias.`,
    //             'secretaria@sigte.com', // Example recipient
    //             { attestationId: attestation.ID, studentId: attestation.AlunoID }
    //         );
    //     }
    // });
}


