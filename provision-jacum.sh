#!/bin/bash
echo -e "\n===== Provisioning Environment ACCEPT ====="

ansible-playbook \
  --vault-password-file=~/.vault \
  --inventory-file=inventory/jacum-hz2 \
  --list-hosts \
  jacum-hz2.yml

time ansible-playbook -v \
  --vault-password-file=~/.vault \
  --inventory-file=inventory/jacum-hz2 \
  jacum-hz2.yml

