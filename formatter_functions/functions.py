import os
import base64
import getpass

from pykeepass import PyKeePass

password = None
filename = None

def htpasswd_filter(logins):
	login_str = map(lambda login: login.username+':'+login.password, logins)
	return list(login_str)

def base64_filter(string):
	return base64.standard_b64encode(string.encode('ascii')).decode('ascii')


def _open_keepass():
	global filename
	global password

	if not filename:
		filename = os.environ.get('KEEPASS', default=None)

	if not filename:
		try:
			with open('.keepass-file', 'r') as keepass_file:
				filename = keepass_file.read()
		except FileNotFoundError:
			filename = None

	if not filename:
		filename = input('Enter PAth to .kdbx-File: ')
		with open('.keepass-file', 'w') as keepass_file:
			keepass_file.write(filename)

	if not password:
		password = getpass.getpass()

	return PyKeePass(filename, password)

def keepass_lookup(path):
	keepass = _open_keepass()
	entry = keepass.find_entries_by_path('/'.join(path), first=True)

	if not entry:
		raise RuntimeError('Unable to find entry in Keepass-File: '+str(path))

	return entry

def keepass_username_filter(path):
	return keepass_lookup(path).username

def keepass_password_filter(path):
	return keepass_lookup(path).password

def keepass_group_filter(path):
	keepass = _open_keepass()
	group = keepass.find_groups_by_path('/'.join(path), first=True)
	print(group)

	if not group:
		raise RuntimeError('Unable to find group in Keepass-File: '+str(path))

	return group.entries



def register(jinja2_env):
	jinja2_env.filters['htpasswd'] = htpasswd_filter
	jinja2_env.filters['base64'] = base64_filter
	jinja2_env.globals['keepass'] = keepass_lookup

	jinja2_env.filters['keepass_username'] = keepass_username_filter
	jinja2_env.filters['keepass_password'] = keepass_password_filter
	jinja2_env.filters['keepass_group'] = keepass_group_filter
