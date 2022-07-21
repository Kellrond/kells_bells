from db.mailserver import Mailserver, Virtual_aliases, Virtual_domains, Virtual_users

db = Mailserver()

def returnUsers(domain=None):
  if domain == None:
    domain = Virtual_users.id
  else:
    sql = f'SELECT v.id FROM virtual_domains v WHERE v.name = { domain }'
    domain = db.engine.execute(sql).scalar()
  query = db.session.query(Virtual_users).filter(Virtual_users.id == domain).all()
  return [ x.__dict__ for x in query ]