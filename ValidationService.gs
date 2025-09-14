/**
 * @fileoverview ValidationService.gs
 * @description Service for server-side data validation.
 * Ensures data integrity before it's written to the sheet, enforcing business rules defined in the schema.
 */

/**
 * Validates an entire data object against its schema from SchemaService.
 * @param {string} entityName - The name of the entity whose data is being validated.
 * @param {object} data - The data object to validate.
 * @returns {object} - An object containing validation status (isValid) and an array of error messages.
 */
function validateEntityData(entityName, data) {
    const schema = getSchema(entityName);
    if (!schema) {
        return { isValid: false, errors: [`Schema for entity '${entityName}' not found.`] };
    }

    const errors = [];

    for (const fieldName in schema.fields) {
        const fieldDef = schema.fields[fieldName];
        const value = data[fieldName];

        // Check for required fields
        if (fieldDef.required && (value === undefined || value === null || value === "")) {
            errors.push(`${fieldDef.label} é obrigatório.`);
            continue; // Skip further validation for this field if it's missing
        }

        // If value is not required and not provided, skip type validation
        if (!fieldDef.required && (value === undefined || value === null || value === "")) {
            continue;
        }

        // Type validation
        switch (fieldDef.type) {
            case 'string':
                if (typeof value !== 'string') errors.push(`${fieldDef.label} deve ser um texto.`);
                break;
            case 'number':
                if (typeof value !== 'number' || isNaN(value)) errors.push(`${fieldDef.label} deve ser um número.`);
                break;
            case 'date':
                if (!(value instanceof Date) || isNaN(value.getTime())) errors.push(`${fieldDef.label} deve ser uma data válida.`);
                break;
            case 'boolean':
                if (typeof value !== 'boolean') errors.push(`${fieldDef.label} deve ser um valor booleano (verdadeiro/falso).`);
                break;
            case 'cpf':
                if (!validateCPF(value)) errors.push(`${fieldDef.label} inválido.`);
                break;
            case 'phone':
                if (!validatePhone(value)) errors.push(`${fieldDef.label} inválido.`);
                break;
            case 'email':
                if (!validateEmail(value)) errors.push(`${fieldDef.label} inválido.`);
                break;
            // Add other custom types as needed
        }

        // Additional validation rules (e.g., readonly - handled by UI/backend logic, not data validation)
    }

    return { isValid: errors.length === 0, errors: errors };
}

/**
 * Validates a CPF number.
 * @param {string} cpf - The CPF string to validate.
 * @returns {boolean} - True if the CPF is valid, false otherwise.
 */
function validateCPF(cpf) {
    if (typeof cpf !== 'string') return false;
    cpf = cpf.replace(/[^\d]/g, ''); // Remove non-digit characters

    if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) return false; // Check length and if all digits are the same

    let sum = 0;
    let remainder;

    for (let i = 1; i <= 9; i++) sum = sum + parseInt(cpf.substring(i - 1, i)) * (11 - i);
    remainder = (sum * 10) % 11;

    if ((remainder === 10) || (remainder === 11)) remainder = 0;
    if (remainder !== parseInt(cpf.substring(9, 10))) return false;

    sum = 0;
    for (let i = 1; i <= 10; i++) sum = sum + parseInt(cpf.substring(i - 1, i)) * (12 - i);
    remainder = (sum * 10) % 11;

    if ((remainder === 10) || (remainder === 11)) remainder = 0;
    if (remainder !== parseInt(cpf.substring(10, 11))) return false;

    return true;
}

/**
 * Validates a phone number (basic format check).
 * @param {string} phone - The phone number string to validate.
 * @returns {boolean} - True if the phone number is valid, false otherwise.
 */
function validatePhone(phone) {
    if (typeof phone !== 'string') return false;
    phone = phone.replace(/[^\d]/g, ''); // Remove non-digit characters
    // Basic validation for Brazilian phone numbers (10 or 11 digits)
    return /^[1-9]{2}(?:[2-9]|9[1-9])[0-9]{7,8}$/.test(phone);
}

/**
 * Validates an email address (basic format check).
 * @param {string} email - The email string to validate.
 * @returns {boolean} - True if the email is valid, false otherwise.
 */
function validateEmail(email) {
    if (typeof email !== 'string') return false;
    // Basic regex for email validation
    return /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(email);
}


