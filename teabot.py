#!/usr/bin/env python

import os
import cgi

if 'REQUEST_METHOD' in os.environ:
    import cgitb
    cgitb.enable()
    print 'Content-Type: text/html'
    print
    from email_server import email_server_dummy as email_server
else:
    from email_server import email_server

import sys
import time

from teabot_utils import *

entries = get_arxiv_entries()
people = get_kipac_members()

if not entries or not people:
    sys.exit(0)

scores, keywords= calc_scores(entries, people, 7)
active_idx = get_active_indices_and_clean_up(people)

from_me = 'KIPAC TeaBot <teabot@kipac.stanford.edu>'
footer =  u'<br><p>This message is automatically generated and sent by KIPAC TeaBot. <br>'
footer += u'<a href="https://github.com/yymao/kipac-teabot/issues?state=open">Create an issue</a> if you have any suggestions/questions.</p>'

email = email_server()

#find papers that members are interested
to = 'KIPAC tealeaks <tealeaks@kipac.stanford.edu>'
title = '{0} new papers on arXiv'.format(time.strftime('%m/%d',time.localtime()))
msg = prepare_email_to_organizers(entries, people, scores, active_idx)
if msg:
    email.send(from_me, to, '[TeaBot] ' + title, msg + footer)

#find interesting papers for individual members
footer += u'<p>To unsubscribe or to update your preferences, <a href="https://web.stanford.edu/~yymao/cgi-bin/kipac-teabot/subscribe.html">click here</a>.</p>'
for to, title, msg in iter_prepare_email_to_individuals(entries, people, scores, keywords):
    email.send(from_me, to, '[TeaBot] ' + title, msg + footer)

email.close()

