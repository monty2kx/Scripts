#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import pprint
import datetime

def main():
    """
    Print mail sent if count of recipient > 10
    """

    RESULTS = {}
    pattern = re.compile(
        '^(?P<datetime>[a-zA-Z]+ {1,2}[0-9]{1,2} {1,2}[0-9]{1,2}:[0-9]{1,2}'
        ':[0-9]{1,2}) (?:(?P<year>[0-9]{4})/)?'
        '(?P<hostname>[0-9a-z\_-]+) postfix/(qmgr|smtp|pipe)\[(?P<pid>[0-9]+)\]: '
        '(?P<id>[A-F0-9]+): (from=<(?P<from>[^>]+)|to=<(?P<to>[^>]+))'
    )
    with open('/var/log/mail.log', 'r') as mail_log:
        for line in mail_log.readlines():
            match = pattern.search(line)
            if match:
                match = match.groupdict()
                # Extraire la date, si l'annÃ~C©e n'existe pas, prendre celle en cours.
                year = match['year'] or datetime.date.today().year
                row_date = datetime.datetime.strptime(
                    '%s %s' % (match['datetime'], year),
                    '%b %d %H:%M:%S %Y'
                )
                # CrÃ~C©er un sous-dictionnaire avec pour clÃ~C© l'ID du mail.
                current = RESULTS.setdefault(match['id'], {})

                # Ajouter les informations.
                if match.get('from'):
                    current['from'] = match['from']
                elif match.get('to'):
                    current.setdefault('to', []).append(match['to'])

        for mail_id, val in RESULTS.items():
            if len(val.get('to',[])) >= 10:
                print '%s %s \n\t%s \nTotal %s' %(mail_id, val.get('from',None), "\t\n\t".join(val.get('to',[])), len(val.get('to',[])))



if __name__ == '__main__':

    main()
