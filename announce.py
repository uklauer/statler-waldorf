#!/usr/bin/env python

import sys
import smtplib
import uuid
from datetime import date, datetime
import time

from email.mime.text import MIMEText

# Where, from whom, subject and what to send:
to = u"MusicBrainz Developer Discussion <musicbrainz-devel@lists.musicbrainz.org>"
sender = "Statler & Waldorf <noreply@musicbrainz.org>"
subject_template = u"Dev chat reminder, issue %s"
msg_template = u'''We've got our weekly dev chat on %s on IRC in #musicbrainz-devel on irc.freenode.net. We're going to meet at Regular Meeting Time [1] (%s) [2].

%sIf there is any topic you would like to discuss during the meeting, please add it to the agenda in the channel topic.

[1] http://musicbrainz.org/doc/Development_Chat
[2] http://www.timeanddate.com/worldclock/fixedtime.html?iso=%s

-- ''' '''
This message brought to you by https://github.com/mayhem/statler-waldorf
Don't even think of responding to this email. We won't answer! http://goo.gl/FSZdF
''';

meeting_time = 20 # UTC; standard time in Europe

unow = datetime.utcnow()
udate = date(unow.year, unow.month, unow.day)

if udate.weekday() == 0 and unow.hour < meeting_time:
    meeting_date = udate
else:
    meeting_date = date.fromtimestamp(time.time() + ((7 - udate.weekday()) * 24 * 60 * 60))

if meeting_date.month > 3 and meeting_date.month < 10:
    meeting_time = 19 # daylight saving time in Europe
elif meeting_date.month == 3 or meeting_date.month == 10:
    is_after_shift = (meeting_date.day - (meeting_date.weekday() + 1) % 7 > 31 - 7)
    # shift to and from DST occurs in Europe on the last Sunday in March and October, respectively
    if (meeting_date.month == 3 and is_after_shift) or (meeting_date.month == 10 and not is_after_shift):
        meeting_time = 19

id_ = uuid.uuid4()
subject = subject_template % id_
msg = MIMEText(msg_template % (
    meeting_date.strftime("%Y-%m-%d"),
    "%02d:00 UTC" % (meeting_time, ),
    "",
    "%sT%02d" % (meeting_date.strftime("%Y%m%d"), meeting_time)
))

msg['Subject'] = subject
msg['From'] = sender
msg['To'] = to
msg['Message-ID'] = "<meeting-announcement-%s@musicbrainz.org>" % id_

s = smtplib.SMTP('localhost')
s.sendmail(sender, [to], msg.as_string())
s.quit()
