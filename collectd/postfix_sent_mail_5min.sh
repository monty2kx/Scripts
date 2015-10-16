#!/bin/bash
# Récupération de métriques depuis les logs de Postfix
#
# Récupération des mails : sent, bounced, deferred et des connect from
# Le format de sortie est directement interprétable par Collectd et poussé dans 
# une base Whisper

HOSTNAME="${COLLECTD_HOSTNAME:-`hostname --short`}"
INTERVAL="${COLLECTD_INTERVAL:-60}"

DATE_NOW=$(/bin/date +'%e %H:%M')
DATE_MOINS5=$(/bin/date --date '1 min ago' +'%e %H:%M')
 
  VALUE_SENT=$(/usr/bin/nice -n 19 /usr/bin/ionice -c3  /bin/sed -n "/$DATE_MOINS5/ , /$DATE_NOW/p" /var/log/mail.log | /usr/bin/nice -n 19 /usr/bin/ionice -c3  /bin/grep "status=sent" | /usr/bin/nice -n 19 /usr/bin/ionice -c3  /usr/bin/wc -l)
  VALUE_BOUNCE=$(/usr/bin/nice -n 19 /usr/bin/ionice -c3  /bin/sed -n "/$DATE_MOINS5/ , /$DATE_NOW/p" /var/log/mail.log | /usr/bin/nice -n 19 /usr/bin/ionice -c3  /bin/grep "status=bounced" | /usr/bin/nice -n 19 /usr/bin/ionice -c3  /usr/bin/wc -l)
  VALUE_DEFERRED=$(/usr/bin/nice -n 19 /usr/bin/ionice -c3  /bin/sed -n "/$DATE_MOINS5/ , /$DATE_NOW/p" /var/log/mail.log | /usr/bin/nice -n 19 /usr/bin/ionice -c3  /bin/grep "status=deferred" | /usr/bin/nice -n 19 /usr/bin/ionice -c3  /usr/bin/wc -l)
  VALUE_CONNECT=$(/usr/bin/nice -n 19 /usr/bin/ionice -c3  /bin/sed -n "/$DATE_MOINS5/ , /$DATE_NOW/p" /var/log/mail.log | /usr/bin/nice -n 19 /usr/bin/ionice -c3  /bin/grep " connect from" | /usr/bin/nice -n 19 /usr/bin/ionice -c3  /usr/bin/wc -l)

  echo "PUTVAL \"$HOSTNAME/smtp-out/gauge-sent-`hostname --short`\" interval=$INTERVAL N:$VALUE_SENT"
  echo "PUTVAL \"$HOSTNAME/smtp-out/gauge-bounce-`hostname --short`\" interval=$INTERVAL N:$VALUE_BOUNCE"
  echo "PUTVAL \"$HOSTNAME/smtp-out/gauge-deferred-`hostname --short`\" interval=$INTERVAL N:$VALUE_DEFERRED"
  echo "PUTVAL \"$HOSTNAME/smtp-out/gauge-connect-`hostname --short`\" interval=$INTERVAL N:$VALUE_CONNECT"

