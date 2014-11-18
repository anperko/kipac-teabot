#!/usr/bin/env python
import cgi
score = 0.25

form = cgi.FieldStorage()
arxiv_id = str(form.getvalue('id'))
name = form.getvalue('name')
key = form.getvalue('key')

if name and key:
    import md5
    from database import keypass, model_dir
    if md5.md5(arxiv_id + name + keypass).hexdigest() == key:
        import anydbm
        d = anydbm.open('%s/%s'%(model_dir, name), 'w')
        if arxiv_id not in d or float(d[arxiv_id]) < score:
            d[arxiv_id] = str(score)
        d.close()

url = ('http://arxiv.org/pdf/%s.pdf'%(arxiv_id)) if arxiv_id else 'http://arxiv.org'

print 'Location:', url
print

