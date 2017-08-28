import os
import re
import shutil

import jinja2
import formatter_functions.functions

jinja2_env = jinja2.Environment()
formatter_functions.functions.register(jinja2_env)

def is_yaml_filename(filename):
	base, ext = os.path.splitext(filename)
	return ext in ('.yaml', '.yml')

def format_recursive(template_folder, output_folder):
	for root, subdirs, files in os.walk(template_folder):
		if root.endswith('.disabled'):
			continue

		yaml_files = filter(is_yaml_filename, files)
		relative_root = os.path.relpath(root, template_folder)
		os.makedirs(os.path.join(output_folder, relative_root), exist_ok=True)

		for yaml_file in yaml_files:
			format_file(
				os.path.join(root, yaml_file),
				os.path.join(output_folder, relative_root, yaml_file))

def format_file(template_file, output_file):
	print("formatting {} -> {}".format(template_file, output_file))

	dirname = os.path.dirname(output_file)
	_, last_dir = os.path.split(dirname)

	namespace = re.sub(r"[^a-zA-Z0-9\-\_]", "_", last_dir)
	if namespace == '_':
		namespace = 'default'

	with open(template_file, 'r', encoding='UTF-8') as template_handle:
		with open(output_file, 'w', encoding='UTF-8') as output_handle:
			template = jinja2_env.from_string(template_handle.read())

			rendered_template = template.render(
				namespace=namespace)

			output_handle.write(rendered_template+'\n')


if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser(description='Formats Kubernetes Manifest-Templates')
	parser.add_argument('input', metavar='IN', type=str, help='file or folder to read')
	parser.add_argument('output', metavar='OUT', type=str, help='file or folder to write to')

	args = parser.parse_args()
	if not os.path.exists(args.input):
		raise RuntimeException("input-file/folder {} does not exist".format(args.input))

	if os.path.isdir(args.input):
		if os.path.exists(args.output):
			print("removing output-folder {}".format(args.output))
			shutil.rmtree(args.output)

		os.makedirs(args.output, exist_ok=True)
		format_recursive(args.input, args.output)
	else:
		format_file(args.input, args.output)
