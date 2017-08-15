import os
import base64
import getpass
import bcrypt
import hashlib

from pykeepass import PyKeePass

password = None
filename = None

def _encrypt_passwd(passwd):
	passwd_ascii = passwd.encode('ascii')
	salt = salt = "$2a$06$" + hashlib.sha1(passwd_ascii).hexdigest()[0:22] + "$"
	return bcrypt.hashpw(passwd_ascii, salt.encode('ascii')).decode('ascii')

def htpasswd_filter(logins):
	login_lines = map(
		lambda login: login.username+':'+_encrypt_passwd(login.password),
		logins)

	return '\n'.join(login_lines)

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
		filename = input('Enter Path to .kdbx-File: ')
		with open('.keepass-file', 'w') as keepass_file:
			keepass_file.write(filename)

	if not password:
		password = getpass.getpass('Password for {}: '.format(filename))

	return PyKeePass(filename, password)

def keepass_lookup(path):
	keepass = _open_keepass()
	entry = keepass.find_entries_by_path('/'.join(path), first=True)

	if not entry:
		raise RuntimeError('Unable to find entry in Keepass-File: '+str(path))

	return entry

def keepass_filter(path, attribute):
	return getattr(keepass_lookup(path), attribute)

def keepass_group_filter(path):
	keepass = _open_keepass()
	group = keepass.find_groups_by_path('/'.join(path), first=True)

	if not group:
		raise RuntimeError('Unable to find group in Keepass-File: '+str(path))

	return group.entries



def register(jinja2_env):
	jinja2_env.filters['htpasswd'] = htpasswd_filter
	jinja2_env.filters['base64'] = base64_filter
	jinja2_env.globals['keepass'] = keepass_lookup

	jinja2_env.filters['keepass'] = keepass_filter
	jinja2_env.filters['keepass_group'] = keepass_group_filter
