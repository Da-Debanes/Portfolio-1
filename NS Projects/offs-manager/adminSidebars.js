/**
 * @file Off Tracker automation
 * @author 3SG Debansha
 * @version 2.0 (291025)
 * 
 * Create sidebars that enables administrators to manually create and delete offs
 */

/**
 * Creates the tab on Google sheets (Offs Manager) that enables sidebars to be opened
 */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  
  // Create custom menu
  ui.createMenu('Offs Manager')
    .addItem('Filter Offs', 'openFilterSidebar')
    .addItem('Create Off', 'openCreateSidebar')
    .addItem('Delete Off', 'openDeleteSidebar')
    .addToUi();
}
// Helper functions to call showSidebar with the right type
function openFilterSidebar() {showSidebar('filter');}
function openCreateSidebar() {showSidebar('create');}
function openDeleteSidebar() {showSidebar('delete');}


/**
 * Select the sidebar and run the relevant functions to enable them
 * Ensure the style sheet is loaded up on each sidebar too (for aesthetics)
 * 
 * @param {string} type 'filter'(if none) OR 'create' OR 'delete'
 * @return {void}
 */
function showSidebar(type = "filter") {
  let htmlOutput;

  // Prepare common style
  const style = HtmlService.createHtmlOutputFromFile('style').getContent();

  switch (type) {
    case "filter":
      htmlOutput = HtmlService.createTemplateFromFile('filter');
      break;
    case "create":
      const email = Session.getActiveUser().getEmail() || "Unknown";   // Email of user giving offs
      const createTemplate = HtmlService.createTemplateFromFile('create');
      createTemplate.creatorEmail = email;
      htmlOutput = createTemplate;
      break;
    case "delete":
      htmlOutput = HtmlService.createTemplateFromFile('delete');
      break;
    default:
      htmlOutput = HtmlService.createTemplateFromFile('filter');  // Default filter sidebar
  }

  // Inject shared stylesheet content into each HTML file
  const evaluated = htmlOutput.evaluate();
  evaluated.setTitle(
    type.charAt(0).toUpperCase() + type.slice(1) + " Off"
  );

  // Replace a placeholder with the style
  let content = evaluated.getContent().replace(
    '</head>',
    `${style}</head>`
  );

  const finalHtml = HtmlService.createHtmlOutput(content)
    .setTitle(evaluated.getTitle());

  SpreadsheetApp.getUi().showSidebar(finalHtml);
}


/**
 * Enables administrators to delete the earliest off of an individual
 * 
 * @param {string} name
 * @param {string} reason  Will be placed in the notes section of the off tracker
 * @return {void}
 */
function deleteOff(namev, reason) {
  const sheet = SpreadsheetApp.openById(OFFS_DB_ID).getSheetByName("Active");
  const data = sheet.getDataRange().getValues();
  const headers = data[0];

  const nameCol = headers.indexOf("name");
  const statusCol = headers.indexOf("status");
  const usedCol = headers.indexOf("used");
  const notesCol = headers.indexOf("notes");

  //finds the first off belonging to {name} and sets its status as deleted
  for (let i = 1; i < data.length; i++) {
    let cName = String(data[i][nameCol]);
    if (name(cName) === namev) {
      const deleted_at = new Date();
      sheet.getRange(i + 1, statusCol + 1).setValue("deleted");
      sheet.getRange(i + 1, usedCol + 1).setValue(deleted_at);
      sheet.getRange(i + 1, notesCol + 1).setValue(reason)
      updateTracker(cName, -1);
      Logger.log(`Deleted row for ${namev}`);
      return;
    }
  }
  Logger.log(`No row found for ${name}`);
}


/**
 * Filter out the dataset based on name queries and status of offs
 * 
 * @param {object} filter  search filter for the offs based on name query and off status
 * @return {object}  list of offs that match filtering criteria
 */
function getOffs(filter = {}) {
  // filter: { name: 'partialName', status: 'active'/'used'/etc. }
  const sheet = SpreadsheetApp.openById(OFFS_DB_ID).getSheetByName("Active");
  const data = sheet.getDataRange().getValues();
  const headers = data[0];

  const nameCol = headers.indexOf("name");
  const statusCol = headers.indexOf("status");
  const expiryCol = headers.indexOf("expiry");

  return data.slice(1)
    .map(row => ({
      name: row[nameCol],
      status: row[statusCol],
      expiry: row[expiryCol] ? Utilities.formatDate(new Date(row[expiryCol]), Session.getScriptTimeZone(), "yyyy-MM-dd") : ""
    }))
    .filter(row => {
      let pass = true;
      if (filter.name) pass = row.name.toLowerCase().includes(filter.name.toLowerCase());
      if (pass && filter.status) pass = row.status === filter.status;
      return pass;
    });
}


/**
 * Returns a list of individuals and their offs if they have at least one
 * 
 * @param {void}
 * @return {object} eligible
 */
function getEligibleNames() {
  const tracker = SpreadsheetApp.openById(OFFS_DB_ID).getSheetByName("Tracker");
  const data = tracker.getDataRange().getValues();
  const headers = data[0];
  const nameCol = headers.indexOf("name");
  const offsCol = headers.indexOf("offs unconsumed");

  const eligible = [];

  for (let i = 1; i < data.length; i++) {
    const name = data[i][nameCol];
    const offs = data[i][offsCol];
    if (offs >= 1) {
      eligible.push({ name, offs });
    }
  }
  return eligible;
}

