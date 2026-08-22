/**
 * mediakit.gs
 *
 * Google Apps Script backend for the media-kit request form on wangle.media.
 *
 * Does three things on each request:
 *   1. appends {timestamp, email, name, company} to the active Sheet
 *   2. emails the requester the deck link straight away, so the experience is
 *      instant and does not depend on anyone being awake
 *   3. emails Geoff a notification, so he can follow up personally while they
 *      are still reading it. That follow-up is the actual point of the form;
 *      the deck does not win work, the reply to a warm lead does.
 *
 * DELIBERATELY A SEPARATE DEPLOYMENT from waitlist.gs. That one writes to the
 * course sheet and mails "New course signup". Sharing an endpoint would mix two
 * unrelated funnels into one sheet and make both useless.
 *
 * Deploy: see MEDIAKIT_SETUP.md, same five clicks as the waitlist script.
 */

// Served from Drive, not from this public repo: a Drive file can be replaced or
// revoked, a file committed to a public repo is permanent in git history.
var DECK_URL = 'https://drive.google.com/file/d/1FTC7mVZfMODeKxjKnf6MgMEDqv8RBZ0N/view';
var OWNER = 'geoff@wanglemedia.com';

function doPost(e) {
  var result = { ok: false };
  try {
    var data = JSON.parse(e.postData.contents);
    var email = (data.email || '').toString().trim();
    var name = (data.name || '').toString().trim();
    var company = (data.company || '').toString().trim();

    if (!email || email.indexOf('@') < 1) {
      return jsonOutput({ ok: false, error: 'missing or malformed email' });
    }

    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['timestamp', 'email', 'name', 'company']);
    }
    sheet.appendRow([new Date(), email, name, company]);

    // Send the deck. Isolated so a mail failure never loses the row, which is
    // already saved above, and never breaks the response to the browser.
    try {
      MailApp.sendEmail({
        to: email,
        subject: 'The Wangle media kit',
        name: 'Wangle',
        replyTo: OWNER,
        body:
          'Thanks for asking.\n\n' +
          'The Wangle media kit is here: ' + DECK_URL + '\n\n' +
          'It covers what we do for corporate communications: presentations and\n' +
          'decks, conference and brand film, product visualization, and the\n' +
          'versioning work that tells you which of them is actually landing.\n\n' +
          'If anything in it looks relevant to something you are working on,\n' +
          'just reply to this email and it comes straight to me.\n\n' +
          'Geoffrey Hancock\n' +
          'Wangle\n' +
          'wangle.media'
      });
    } catch (mailErr) {
      // swallow: the request is captured regardless
    }

    // Notify the owner. Separate try for the same reason.
    try {
      MailApp.sendEmail(
        OWNER,
        'Media kit requested: ' + email,
        'Someone requested the media kit from wangle.media.\n\n' +
          'Email   : ' + email + '\n' +
          'Name    : ' + (name || '(none)') + '\n' +
          'Company : ' + (company || '(none)') + '\n\n' +
          'The deck has already been sent to them automatically.\n' +
          'A short personal reply now, while they are reading it, is worth more\n' +
          'than the deck is.\n\n' +
          'Row added to the media kit sheet.'
      );
    } catch (mailErr2) {
      // swallow
    }

    result.ok = true;
  } catch (err) {
    result.ok = false;
    result.error = err.toString();
  }
  return jsonOutput(result);
}

function jsonOutput(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
