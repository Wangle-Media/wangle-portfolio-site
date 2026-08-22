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
4. **Deploy > New deployment**, gear icon > **Web app**.
   - Execute as: **Me**
   - Who has access: **Anyone**
   - Deploy, then authorise when Google asks. It will warn that the app is
     unverified; this is your own script, so continue.
5. Copy the **Web app URL**. It looks like
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
