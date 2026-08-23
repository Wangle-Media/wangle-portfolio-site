#!/usr/bin/env python3
"""Remove clearly-marked test rows from the media kit and course waitlist sheets.

Defaults to a DRY RUN. Pass --apply to actually delete.

Two safety properties matter here, because one of these sheets holds real course
signups eleven days before the course:

  1. Rows are identified by CONTENT, never by a position captured earlier. The
     read and the delete happen in the same run, and a row only qualifies if it
     carries an explicit test marker.
  2. Deletion runs bottom-up, so removing one row cannot shift the index of
     another still queued for removal.

Anything not carrying a marker is left alone, and the sheet is read back
afterwards so the result is verified rather than assumed.
"""
import sys
import os.path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
TOKEN = os.path.expanduser('~/.credentials/google-sheets-token.json')

SHEETS = {
    'media kit requests': '1Chl564d7eBmH7v7UaNK4H3XBHdAZmCXATMMk_92948M',
    'course waitlist':    '1USYB0ia9xAlRqQGKMH0_wnqMzviIp_HrcFOHcT2PzDg',
}

# A row must contain one of these to be eligible. Deliberately narrow: a real
# lead must never match by accident.
MARKERS = ('delete this row', 'test endpoint check', 'ws14 endpoint check',
           'final test after fix', 'test old waitlist endpoint',
           'test new endpoint you pasted')


def is_test_row(row):
    blob = ' '.join(str(c) for c in row).lower()
    return any(m in blob for m in MARKERS)


def main():
    apply = '--apply' in sys.argv
    creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
    svc = build('sheets', 'v4', credentials=creds)

    for label, sid in SHEETS.items():
        meta = svc.spreadsheets().get(spreadsheetId=sid).execute()
        tab = meta['sheets'][0]['properties']
        rows = svc.spreadsheets().values().get(
            spreadsheetId=sid, range=tab['title']).execute().get('values', [])

        print('\n%s  (%d rows incl. header)' % (label, len(rows)))
        doomed = []
        for idx, row in enumerate(rows):
            if idx == 0:
                continue                     # never touch the header
            if is_test_row(row):
                doomed.append(idx)
                print('   DELETE  row %-3d %s' % (idx + 1, ' | '.join(str(c) for c in row)[:88]))
            else:
                print('   keep    row %-3d %s' % (idx + 1, ' | '.join(str(c) for c in row)[:88]))

        if not doomed:
            print('   nothing to remove')
            continue
        if not apply:
            print('   DRY RUN: %d row(s) would be deleted. Re-run with --apply.' % len(doomed))
            continue

        # bottom-up so earlier indices stay valid
        reqs = [{'deleteDimension': {'range': {
                    'sheetId': tab['sheetId'], 'dimension': 'ROWS',
                    'startIndex': i, 'endIndex': i + 1}}}
                for i in sorted(doomed, reverse=True)]
        svc.spreadsheets().batchUpdate(
            spreadsheetId=sid, body={'requests': reqs}).execute()

        after = svc.spreadsheets().values().get(
            spreadsheetId=sid, range=tab['title']).execute().get('values', [])
        left = [r for i, r in enumerate(after) if i and is_test_row(r)]
        print('   deleted %d, %d rows remain, test rows still present: %d'
              % (len(doomed), len(after), len(left)))


if __name__ == '__main__':
    main()
