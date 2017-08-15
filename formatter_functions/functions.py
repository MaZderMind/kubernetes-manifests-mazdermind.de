import base64

def htpasswd_filter(logins):
	return 'htpasswd encoded logins from '+str(logins)

def base64_filter(string):
	return base64.standard_b64encode(string.encode('ascii')).decode('ascii')

def keepass_lookup(path):
	return {
		'username': "username",
		'password': 'password',
	}

def keepass_username_filter(path):
	return keepass_lookup(path)['username']

def keepass_password_filter(path):
	return keepass_lookup(path)['password']

def keepass_all_filter(path):
	return {
		'user1': "pass1",
		'user2': 'pass2',
	}

def register(jinja2_env):
	jinja2_env.filters['htpasswd'] = htpasswd_filter
	jinja2_env.filters['base64'] = base64_filter
	jinja2_env.globals['keepass'] = keepass_lookup

	jinja2_env.filters['keepass_username'] = keepass_username_filter
	jinja2_env.filters['keepass_password'] = keepass_password_filter
	jinja2_env.filters['keepass_all'] = keepass_all_filter
