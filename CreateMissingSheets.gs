/**
 * @fileoverview CreateMissingSheets.gs
 * @description Script to create missing sheets and set up initial headers based on SchemaService.gs.
 */

function createMissingSheets() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  for (const sheetKey in SHEET_NAMES) {
    const sheetName = SHEET_NAMES[sheetKey];
    let sheet = ss.getSheetByName(sheetName);

    if (!sheet) {
      sheet = ss.insertSheet(sheetName);
      Logger.log(`Sheet '${sheetName}' created.`);
    } else {
      Logger.log(`Sheet '${sheetName}' already exists.`);
    }

    // Set headers if the sheet is not a history sheet and has a defined schema
    if (!sheetName.endsWith('_History')) {
      const headers = getSheetHeaders(sheetName);
      if (headers.length > 0) {
        const range = sheet.getRange(1, 1, 1, headers.length);
        range.setValues([headers]);
        Logger.log(`Headers set for sheet '${sheetName}': ${headers.join(', ')}`);
      }
    }
  }

  // Create history sheets with default headers (Timestamp, Action, User, Record ID, Changes)
  for (const sheetKey in SHEET_NAMES) {
    const sheetName = SHEET_NAMES[sheetKey];
    if (sheetName.endsWith('_History')) {
      let historySheet = ss.getSheetByName(sheetName);
      if (!historySheet) {
        historySheet = ss.insertSheet(sheetName);
        Logger.log(`History sheet '${sheetName}' created.`);
      }
      const historyHeaders = ['Timestamp', 'Action', 'User', 'Record ID', 'Changes'];
      const range = historySheet.getRange(1, 1, 1, historyHeaders.length);
      range.setValues([historyHeaders]);
      Logger.log(`Headers set for history sheet '${sheetName}': ${historyHeaders.join(', ')}`);
    }
  }
}

function onOpen() {
  createMissingSheets();
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('SIG-TE Admin')
      .addItem('Criar/Atualizar Planilhas', 'createMissingSheets')
      .addToUi();
}


