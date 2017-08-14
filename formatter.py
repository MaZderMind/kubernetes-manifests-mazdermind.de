import os
import re

from jinja2 import Template

def is_yaml_filename(filename):
	base, ext = os.path.splitext(filename)
	return ext in ('.yaml', '.yml')

def format_recursive(template_folder, output_folder):
	for root, subdirs, files in os.walk(template_folder):
		yaml_files = filter(is_yaml_filename, files)
		relative_root = os.path.relpath(root, template_folder)
		namespace = re.sub(r"[^a-zA-Z0-9\-\_]", "_", relative_root)
		if namespace == '_':
			namespace = 'default'

		os.makedirs(os.path.join(output_folder, relative_root), exist_ok=True)
		for yaml_file in yaml_files:
			format_file(
				os.path.join(root, yaml_file),
				os.path.join(output_folder, relative_root, yaml_file),
				context = {'namespace': namespace})

def format_file(template_file, output_file, context = {}):
	print("formatting {} -> {}".format(template_file, output_file))


if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser(description='Formats Kubernetes Manifest-Templates')
	parser.add_argument('input', metavar='IN', type=str, help='file or folder to read')
	parser.add_argument('output', metavar='OUT', type=str, help='file or folder to write to')

	args = parser.parse_args()
	if not os.path.exists(args.input):
		raise RuntimeException("input-file/folder {} does not exist".format(args.input))

	if os.path.isdir(args.input):
		os.makedirs(args.output, exist_ok=True)
		format_recursive(args.input, args.output)
	else:
		format_file(args.input, args.output)
