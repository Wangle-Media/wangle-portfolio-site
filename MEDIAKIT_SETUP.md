# Media kit form: the five-click deploy

The form on wangle.media is built and live. It needs one thing to go from
"tells people to email Geoff" to "sends the deck automatically": an Apps Script
endpoint. Same shape as the course waitlist script, so this is familiar.

**Until it is deployed the form still works.** With no endpoint set it tells the
visitor to email `geoff@wanglemedia.com` for the kit. A lead is never silently
dropped, which is the one thing a broken form must not do.

## Deploy

1. Go to <https://sheets.new> and name the sheet something like
   **Wangle media kit requests**.
2. **Extensions > Apps Script**. Delete the placeholder `myFunction`.
3. Paste the whole contents of `mediakit.gs` from this repo.
4. **Narrow the permissions before deploying.** In the editor, click the gear
   (Project Settings) and tick **Show "appsscript.json" manifest file**. Open the
   `appsscript.json` that appears in the file list and replace its contents with
   the `appsscript.json` from this repo.

   This matters. Without it Apps Script asks for **"see, edit, create and delete
   all your Google Sheets spreadsheets"**, which is far more than this needs. The
   manifest pins it to two scopes:

   - `spreadsheets.currentonly` - only the sheet the script is attached to, not
     every spreadsheet in the account
   - `script.send_mail` - send mail as you, which is unavoidable: mailing the
     deck and the notification is the entire job

   The consent screen should then say **"See, edit, create and delete only the
   specific Google Drive file used with this app"** instead of all of them.

5. **Deploy > New deployment**, gear icon > **Web app**.
   - Execute as: **Me**
   - Who has access: **Anyone**
   - Deploy, then authorise. Google will warn the app is unverified and show no
     privacy policy. That is expected: it is your own personal script, not a
     third-party app, and the consent screen is simply named after the sheet.
6. Copy the **Web app URL**. It looks like
   `https://script.google.com/macros/s/AKfy...../exec`.

## Wire it up

Open `template.html`, find:

```js
var ENDPOINT = ''; // set after deploying mediakit.gs
```

Paste the URL between the quotes, then run `python build.py` and push. That is
the whole change.

## What happens on each request

1. A row is appended to the sheet: timestamp, email, name, company.
2. The requester is emailed the deck link immediately, with a reply-to that
   reaches Geoff directly.
3. Geoff is emailed a notification.

The notification is the point. The deck does not win the work; a short personal
reply while they are still reading it does.

## Deliberately a separate deployment

Do NOT point this at the course waitlist endpoint. That script writes to the
course sheet and sends a mail titled "New course signup". Sharing one endpoint
would merge two unrelated funnels into a single sheet and make both useless for
deciding anything.

## The endpoint is public, and that is unavoidable

A static page has to be able to call it, so the URL is visible in view-source
whether or not this repo is public. Committing it here adds no exposure.

What it does mean is that **anyone can POST to it**. The script mails the deck to
whatever address is submitted, so without a limit someone could use it to send
thousands of emails from Geoff's domain, exhaust the daily send quota, and
silently break the form for real leads.

`MAX_SENDS_PER_DAY` (40) caps the SENDING and never the RECORDING. Past the cap
a request is still written to the sheet and Geoff gets one alert, so a genuine
spike looks like a spike rather than like the form going quiet. Raise it after
checking the sheet, not before.

## What the script can actually do

Read `mediakit.gs`; it is 100 lines and does exactly three things. It appends a
row to the attached sheet, mails the requester the deck link, and mails Geoff a
notification. It reads nothing else, and with the manifest above it *cannot*
reach another spreadsheet even if it tried.

The permission you grant is still broader than the code uses, which is true of
any Apps Script. The protection is that you are the only person who can edit the
script, and the code is versioned in this repo where a change would be visible
in the diff.

## Where the deck lives

**Google Drive**, not this repo. `DECK_URL` in `mediakit.gs` points at it.

That is the right way round. A Drive file can be replaced or its sharing
revoked; a file committed to a public repo is permanent in git history, so a
figure that later needed retracting could not be taken back.

The deck was briefly committed here before being moved. It is gone from the
served site, but that one commit remains in history. If it ever needs to be
truly unrecoverable, that requires a history rewrite and a force push, which is
worth doing only if the content becomes genuinely sensitive.

**Check the Drive file is shared as "anyone with the link"**, or requesters will
be asked to request access, which defeats the whole point of an instant send.
