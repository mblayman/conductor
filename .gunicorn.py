accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s'
bind = '127.0.0.1:8080'
keyfile = 'playbooks/roles/loadbalancer/files/privkey.pem'
certfile = 'playbooks/roles/loadbalancer/files/chain.pem'
reload = True
