/**
 * @fileoverview DataManager.gs
 * @description Generic CRUD (Create, Read, Update, Delete) service that interacts with the Google Sheet.
 */

/**
 * Fetches data from a sheet with support for filtering, sorting, and pagination.
 * @param {string} entityName - The name of the entity to fetch data for.
 * @param {object} options - Options for filtering, sorting, and pagination.
 * @returns {Array} - An array of objects representing the fetched data.
 */
function getByEntity(entityName, options = {}) {
    const sheetName = getSheetName(entityName);
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
    if (!sheet) {
        throw new Error(`Sheet not found: ${sheetName}`);
    }

    const headers = getSheetHeaders(sheetName);
    const data = sheet.getDataRange().getValues();
    data.shift(); // Remove header row

    let results = data.map(row => {
        const obj = {};
        headers.forEach((header, index) => {
            obj[header] = row[index];
        });
        return obj;
    });

    // Apply filtering
    if (options.filter) {
        results = results.filter(item => {
            for (const key in options.filter) {
                if (item[key] != options.filter[key]) {
                    return false;
                }
            }
            return true;
        });
    }

    // Apply sorting
    if (options.sort) {
        results.sort((a, b) => {
            const field = options.sort.field;
            const order = options.sort.order === 'desc' ? -1 : 1;
            if (a[field] < b[field]) return -1 * order;
            if (a[field] > b[field]) return 1 * order;
            return 0;
        });
    }

    // Apply pagination
    if (options.page && options.pageSize) {
        const startIndex = (options.page - 1) * options.pageSize;
        results = results.slice(startIndex, startIndex + options.pageSize);
    }

    return results;
}

/**
 * Fetches a single record by its ID.
 * @param {string} entityName - The name of the entity to fetch data for.
 * @param {number} id - The ID of the record to fetch.
 * @returns {object|null} - The fetched record, or null if not found.
 */
function getById(entityName, id) {
    const sheetName = getSheetName(entityName);
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
    if (!sheet) {
        throw new Error(`Sheet not found: ${sheetName}`);
    }

    const data = sheet.getDataRange().getValues();
    const headers = data.shift();
    const idIndex = headers.indexOf('ID');

    for (const row of data) {
        if (row[idIndex] == id) {
            const obj = {};
            headers.forEach((header, index) => {
                obj[header] = row[index];
            });
            return obj;
        }
    }

    return null;
}

/**
 * Creates a new record in the specified sheet.
 * @param {string} entityName - The name of the entity to create a record for.
 * @param {object} data - The data for the new record.
 * @returns {object} - The created record.
 */
function create(entityName, data) {
    const validation = ValidationService.validateEntityData(entityName, data);
    if (!validation.isValid) {
        throw new Error(`Validation failed: ${validation.errors.join(', ')}`);
    }

    const sheetName = getSheetName(entityName);
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
    if (!sheet) {
        throw new Error(`Sheet not found: ${sheetName}`);
    }

    const headers = getSheetHeaders(sheetName);
    const newRow = headers.map(header => data[header] || '');
    sheet.appendRow(newRow);

    return data;
}

/**
 * Updates an existing record in the specified sheet.
 * @param {string} entityName - The name of the entity to update a record for.
 * @param {number} id - The ID of the record to update.
 * @param {object} data - The new data for the record.
 * @returns {object} - The updated record.
 */
function update(entityName, id, data) {
    const sheetName = getSheetName(entityName);
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
    if (!sheet) {
        throw new Error(`Sheet not found: ${sheetName}`);
    }

    const dataRange = sheet.getDataRange();
    const values = dataRange.getValues();
    const headers = values.shift();
    const idIndex = headers.indexOf('ID');

    for (let i = 0; i < values.length; i++) {
        if (values[i][idIndex] == id) {
            const oldData = {};
            headers.forEach((header, index) => {
                oldData[header] = values[i][index];
            });

            // Log history
            const historySheetName = `${sheetName}_History`;
            const historySheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(historySheetName);
            if (historySheet) {
                historySheet.appendRow([new Date(), Session.getActiveUser().getEmail(), 'UPDATE', JSON.stringify(oldData)]);
            }

            const newRow = headers.map(header => data[header] !== undefined ? data[header] : values[i][headers.indexOf(header)]);
            sheet.getRange(i + 2, 1, 1, newRow.length).setValues([newRow]);
            return data;
        }
    }

    throw new Error(`Record with ID ${id} not found.`);
}

/**
 * Soft deletes a record by setting its 'Ativo' or 'Status' column to 'INATIVO'.
 * @param {string} entityName - The name of the entity to delete a record from.
 * @param {number} id - The ID of the record to delete.
 * @returns {object} - The deleted record.
 */
function deleteRecord(entityName, id) {
    const sheetName = getSheetName(entityName);
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
    if (!sheet) {
        throw new Error(`Sheet not found: ${sheetName}`);
    }

    const dataRange = sheet.getDataRange();
    const values = dataRange.getValues();
    const headers = values.shift();
    const idIndex = headers.indexOf('ID');
    const statusIndex = headers.indexOf('Ativo') !== -1 ? headers.indexOf('Ativo') : headers.indexOf('Status');

    if (statusIndex === -1) {
        throw new Error(`No 'Ativo' or 'Status' column found for soft delete in ${entityName}`);
    }

    for (let i = 0; i < values.length; i++) {
        if (values[i][idIndex] == id) {
            const oldData = {};
            headers.forEach((header, index) => {
                oldData[header] = values[i][index];
            });

            // Log history
            const historySheetName = `${sheetName}_History`;
            const historySheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(historySheetName);
            if (historySheet) {
                historySheet.appendRow([new Date(), Session.getActiveUser().getEmail(), 'DELETE', JSON.stringify(oldData)]);
            }

            sheet.getRange(i + 2, statusIndex + 1).setValue('INATIVO');
            return oldData;
        }
    }

    throw new Error(`Record with ID ${id} not found.`);
}


