/**
 * @file Off Tracker automation
 * @author 3SG Debansha
 * @version 1.1 (021125)
 * 
 * Daily Trigger (Automatic) by Apps Script at 1800 when further changes to day's Duty Roster unlikely
 * Nev version includes ability to externally add and delete offs from sidebars [version 2]
 * Reads the events that would enable a TO to get an off from Standby Roles sheet (still labelled standby off) [version 1.1]
 */
const OFFS_DB_ID = '1tvip-W0IwbzQiKRtEA61uzp5EVyPW4cl19p6v0kEJnc';
const DUTY_ROSTER_ID = '1_0RXX7PI2GD1OlX9Gz6F-YI6A-J1EU2jMeSpw8cBo80';

let standbyRoles = [];

function main(today) {
  if (!(today instanceof Date)) today = new Date(); // Today's Date

  standbyRoles = offEvents();
  dailyRead(today);  // Read Duty Roster and update Database
  cleanUp(today);    // Clean up Database 
}


/**
 * Reads the Duty Roster everyday
 * - On weekdays, it deducts offs from individuals utilising their offs
 * - On weekends, it adds offs for those doing standby duty
 * 
 * @param {Date} today  Today's Date
 * @return {void}
 */
function dailyRead(today) {
  // Open Duty Roster Sheet
  const dutyRoster = SpreadsheetApp.openById(DUTY_ROSTER_ID);

  // Use Logic to open the correct spreadsheet
  if (!(today instanceof Date)) today = new Date()
  const monthyr = Utilities.formatDate(today, Session.getScriptTimeZone(), "MMMM yyyy");
  const monthlyRoster = dutyRoster.getSheetByName(monthyr);
  
  const data = monthlyRoster.getDataRange().getValues();
  const headers = data[1];

  // Find Row Index with names
  const names = headers.indexOf("Rank & Name");

  // Find Row Index with today's date
  const todayRoster = today.getDate() + 3;
  
  if (workingDay(today)) {
    // go through all name - activity pair
    for (let i = 2; i < data.length; i++) {
      // if activity == off
      const activity = String(data[i][todayRoster]);
      if (activity != "" && activity.includes("OFF")) useOff(today, data[i][names]);
    }  
  } else {
    // go through all name - activity pair
    for (let i = 2; i < data.length; i++) {
      const activity = String(data[i][todayRoster]);
      if (activity != "" && doingNTM(activity)) createOff(today, data[i][names], "Standby Offs");
    }
  }
}


/**
 * Manage the offs on a daily basis including:
 *  - Updating the statuses of offs to expire
 *  - Deleting the records of used/ expired offs that are more than a month old
 *
 * @param {Date} now  Today's date for reference
 * @return {void}
 */
function cleanUp(now) {
  const db = SpreadsheetApp.openById(OFFS_DB_ID).getSheetByName("Active");
  const data = db.getDataRange().getValues();
  const headers = data[0];

  // Column indexes
  const expiredCol = headers.indexOf("expiry");
  const usedCol = headers.indexOf("used");
  const statusCol = headers.indexOf("status");
  const ownerCol = headers.indexOf("name");

  if (!(now instanceof Date)) now = new Date();
  const rowsToDelete = [];
  const updates = []; // to batch updates for expired statuses
  const trackerUpdates = {}; // to batch tracker updates by owner

  // Process everything in memory first
  for (let i = 1; i < data.length; i++) {
    const status = data[i][statusCol];
    const expiresAt = data[i][expiredCol] ? new Date(data[i][expiredCol]) : null;
    const usedAt = data[i][usedCol] ? new Date(data[i][usedCol]) : null;
    const owner = data[i][ownerCol];

    // Expire active tokens
    if (status === "active" && expiresAt && now >= expiresAt) {
      updates.push([i + 1, "expired"]);
      trackerUpdates[owner] = (trackerUpdates[owner] || 0) + 0; // mark for expiry update
    }

    // Delete used/expired/deleted tokens older than 1 month
    if (["used", "expired", "deleted"].includes(status)) {
      const refDate = usedAt || expiresAt;
      if (!refDate) continue;

      const diffMonths =
        (now.getFullYear() - refDate.getFullYear()) * 12 +
        (now.getMonth() - refDate.getMonth());

      if (diffMonths >= 1) rowsToDelete.push(i + 1);
    }
  }

  // Batch status updates
  if (updates.length > 0) {
    const statusRange = db.getRange(2, statusCol + 1, data.length - 1, 1);
    const statusValues = statusRange.getValues();

    updates.forEach(([rowIndex]) => {
      statusValues[rowIndex - 2][0] = "expired"; // adjust for header
    });

    statusRange.setValues(statusValues);
  }

  // Batch tracker updates 
  Object.keys(trackerUpdates).forEach(owner => updateTracker(owner, 0));

  // Delete old rows (bottom-up)
  rowsToDelete.reverse().forEach(row => db.deleteRow(row));

  Logger.log(`Updated ${updates.length} expired tokens and deleted ${rowsToDelete.length} old rows.`);
}


/**
 * Updates the database and tracker sheet when an owner is given an off
 *
 * @param {date} created_at  The date the off is given
 * @param {string} owner  The owner's name
 * @param {string} purpose  The reason for off
 * @param {string} creator  Who is giving the off? Auto for system generated offs
 * @return {void}
 */
function createOff(created, owner, purpose, creator) {
  const db = SpreadsheetApp.openById(OFFS_DB_ID).getSheetByName("Active");
  const lastRow = db.getLastRow();
  if (!creator) creator = "auto";
  if (!purpose) purpose = "";

  const id = "T" + new Date().getTime(); // ID generation to ensure uniqueness
  
  let createdAt;
  if (created instanceof Date) {
    createdAt = created;
  } else if (typeof created === "string" && !isNaN(Date.parse(created))) {
    createdAt = new Date(created);
  } else {
    // fallback if nothing valid provided
    createdAt = new Date();
  }

  const expiresAt = new Date(createdAt.getFullYear(), createdAt.getMonth(), createdAt.getDate());
  expiresAt.setMonth(expiresAt.getMonth() + 1);

  db.appendRow([id, owner, createdAt, expiresAt, "active", "", creator, purpose]);
  updateTracker(owner, 1);
}


/**
 * Updates the database and tracker sheet when an owner uses an off
 *
 * @param {date} used_at  The date the off is redeemed
 * @param {string} ownerName  The owner's name
 * @return {void}
 */
function useOff(used_at, ownerName) {
  const db = SpreadsheetApp.openById(OFFS_DB_ID).getSheetByName("Active");
  
  const data = db.getDataRange().getValues();
  const headers = data[0];
  const ownerCol = headers.indexOf("name");
  const createdCol = headers.indexOf("created");
  const statusCol = headers.indexOf("status");
  const usedCol = headers.indexOf("used");

  // Filter Offs belonging to owner
  const allOffs = data.slice(1)
    .map((row, i) => ({
      rowIndex: i + 2,
      owner: row[ownerCol],
      created: new Date(row[createdCol]),
      status: row[statusCol]
    }));

  const offs =  allOffs.filter(off => off.owner === ownerName && off.status === "active");

  if (offs.length === 0) {
    Logger.log(`No tokens found for ${ownerName}`);
    updateTracker(ownerName, -2);
    return;
  }

  // Find earliest created
  const earliest = offs.reduce((a, b) => (a.created < b.created ? a : b));
  
  // Update its status to "used"
  //const used_at = new Date();
  db.getRange(earliest.rowIndex, statusCol + 1).setValue("used");
  db.getRange(earliest.rowIndex, usedCol + 1).setValue(used_at);
  updateTracker(ownerName, -1);

  Logger.log(`Marked earliest token for ${ownerName} as USED on ${used_at.toDateString()}`);
}


/**
 * Updates the tracker sheet with changes to a user's off counts.
 *
 * @param {string} owner  The owner's name.
 * @param {number} change +1 for creation, -1 for use/deletion, 0 for expiry, -2 for unaccounted offs.
 * @return {void}
 */
function updateTracker(owner, change) {
  const tracker = SpreadsheetApp.openById(OFFS_DB_ID).getSheetByName("Tracker");
  let data = tracker.getDataRange().getValues();
  let ind = -1;

  // Find matching owner
  for (let i = 1; i < data.length; i++) {
    if (data[i][0] === name(owner)) {
      ind = i;
      break;
    }
  }
  // If not found, append new row
  if (ind === -1) {
    tracker.appendRow([name(owner), 0, 0]);
    data = tracker.getDataRange().getValues();
    ind = data.length - 1;
  }

  let offs = data[ind][1];
  let exp = data[ind][2];
  let unacc = data[ind][3];

  if (change === 1) {
    tracker.getRange(ind + 1, 2).setValue(offs + 1);
  } else if (change === -1) {
    if (offs > 0) tracker.getRange(ind + 1, 2).setValue(offs - 1);
  } else if (change === 0) {
    tracker.getRange(ind + 1, 2).setValue(offs - 1);
    tracker.getRange(ind + 1, 3).setValue(exp + 1);
  } else if (change === -2) {
    tracker.getRange(ind + 1, 2).setValue(unacc + 1);
  }
}


/**
 * Helper function to create a date with standardised times for comparing 2 dates that are the same
 *
 * @param {Date} date
 * @return {Date}
 */
function normalise(date) {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate());
}


/**
 * Helper function to determine if any given date is a working day (weekday) or not (weekend or public holiday)
 *
 * @param {Date} date  
 * @return {boolean}
 */
function workingDay(date) {
  const day = date.getDay(); // convert each date to a indexed day of the week
  if (day === 0 || day === 6) return false; // 0 = Sunday, 6 = Saturday

  // Holiday calendar ID
  const calendarId = 'en.singapore#holiday@group.v.calendar.google.com';
  const calendar = CalendarApp.getCalendarById(calendarId);

  const holidays = calendar.getEventsForDay(date); // See if there is actually a holiday on the given day
  if (holidays.length > 0) return false;

  return true;
}


/**
 * Helper function to generate the list of roles/ exercises a TO can take to generate an off
 * 
 * @param {void}
 * @return {object}  array of roles/events
 */
function offEvents() { 
  const sheet = SpreadsheetApp.openById(OFFS_DB_ID).getSheetByName("Standby Roles"); 
  const roles = sheet.getRange("B2:B").getValues(); 
  return roles.map(row => row[0]).filter(v => v !== ""); 
}


/**
 * Helper function to determine if a TO is doing standby on weekends in particular
 *
 * @param {string} activity  What a TO is doing that day
 * @return {boolean}  If the role is standby activity
 */
function doingNTM(activity) {
  for (const role of standbyRoles) {
    if (activity.includes(role)) return true; // If the TO does standby (including HOTO days)
  }
  return false;
}


/**
 * Helper function to convert Rank/Name to just name in off tracker
 * 
 * @param {string} rankName  Original Rank & Name
 * @return {string}  Name of TO
 */
function name(rankName) {
  return rankName.replace(/^[A-Z0-9][A-Z]{2}\s+/, '').replace(/\s*\(TOG\)$/, '').trim();
}


/**
 * Helper used inside HTML templates to include other HTML files (e.g. styles or snippets).
 * Usage in HTML: <?!= include('style') ?>
 */
function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}

