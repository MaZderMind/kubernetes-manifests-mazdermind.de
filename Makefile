# Makefile for K8s Cluster Management

include .env

TEMPLATES_DIR_NAME=templates
RESULTS_DIR_NAME=results

TEMPLATES_DIR=${TEMPLATES_DIR_NAME}
RESULTS_DIR=${RESULTS_DIR_NAME}

ifneq (${NAMESPACE},)
TEMPLATES_DIR:=${TEMPLATES_DIR}/${NAMESPACE}
RESULTS_DIR:=${RESULTS_DIR}/${NAMESPACE}
endif

default: use generate

prepare:
	go get -u github.com/bborbe/teamvault_utils/bin/teamvault_config_dir_generator

use:
	kubectl config use-context ${CLUSTER_CONTEXT}

generate:
	@test -f ~/.teamvault-sm.json || echo "\nMissing file ~/.teamvault-sm.json :\n{\n \"url\": \"https://teamvault.apps.seibert-media.net\",\n \"user\": \"mmustermann\",\n \"pass\": \"PASSWORT\"\\n}"
	@test -f ~/.teamvault-sm.json || exit 1
	
	@rm -rf ${RESULTS_DIR_NAME}
	teamvault_config_dir_generator \
		-teamvault-config="~/.teamvault-sm.json" \
		-source-dir=${TEMPLATES_DIR} \
		-target-dir=${RESULTS_DIR} \
		-logtostderr \
		-v=2

apply: use generate
	@kubectl apply --recursive -f results
	@rm -rf results

clear:
	@rm -rf results
