# if this is running from the scripts folder, move up a folder.
import os, sys
if not 'server.py' in os.listdir('.') and 'scripts' in os.listdir('..'):
	os.chdir('..')

sys.path.append('.')

import time, sys
import traceback
from tasserver.LegacyUsers import User

if not len(sys.argv) == 3:
	print 'usage: migrate.py [/path/to/accounts.txt] [dburl]'
	sys.exit()

print
print 'starting migration'
print

accountstxt = sys.argv[1]
dburl = sys.argv[2]

def _bin2dec(s): return int(s, 2)

print 'opening database'
try:
	import sqlalchemy
	engine = sqlalchemy.create_engine(dburl, pool_size=512, pool_recycle=300)
except:
	print '-'*60
	print traceback.format_exc()
	print '-'*60
	print
	print 'could not import sqlalchemy module, try running scripts/fetch_deps.py'
	sys.exit()

UsersHandler = __import__('SQLUsers').UsersHandler
db = UsersHandler(None, engine)

print 'reading accounts'

f = open(accountstxt, 'r')
data = f.read()

f.close()
print 'scanning accounts'
accounts = {}

for line in data.split('\n'):
	if line:
		user = User.fromAccountLine(line)
		accounts[user.casename] = {
			'user':user.casename, 'pass':user.password, 'ingame':user.ingame_time,
			'last_login':user.last_login, 'register_date':user.register_date, 'uid':user.last_id,
			'last_ip':user.last_ip, 'country':user.country, 'bot':user.bot, 'access':user.access,
			}

print
print 'writing accounts to database'
db.inject_users(accounts.values())