#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import pprint
import datetime
from time import gmtime, strftime, localtime

def main():
    """
    """

    RESULTS = {}

    #La date actuelle 
    date_now = datetime.datetime.now()
    #La date il y a une heure
    delta5min = datetime.timedelta(seconds=3600)

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
                # Extraire la date, si l'année n'existe ps, prendre celle en cours.
                year = match['year'] or datetime.date.today().year
                datejour = datetime.date.today().year
                row_date = datetime.datetime.strptime(
                    '%s %s' % (match['datetime'], year),
                    '%b %d %H:%M:%S %Y'
                )
                #date_now - row_date genere un delta de temps
                #on compare ce delta a celui calculé plus haut
                #si le delta est superieur a celui choisi alors on passe au suivant sans affichage
                if date_now - row_date > delta5min:
                    continue
                # Creation d'un sous-dictionnaire avec pour clef l'ID du mail.
                current = RESULTS.setdefault(match['id'], {})
                # Ajouter les informations.
                if match.get('datetime'):
                    current['datemail'] = match['datetime']
                if match.get('from'):
                    current['from'] = match['from']
                elif match.get('to'):
                    current.setdefault('to', []).append(match['to'])
        for mail_id, val in RESULTS.items():
            if len(val.get('to',[])) >= 10:
                print '\n%s %s %s Total %s' %(val.get('datemail',None), mail_id, val.get('from',None), len(val.get('to',[])))

if __name__ == '__main__':

    main()

