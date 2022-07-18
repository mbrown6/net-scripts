Lighthouse VPN configuration playbook depends on variables listed in the
/group_vars/opengears.yml file.  This file contains sensitive keying material
and is encrypted using ansible-vault.  To decrypt the file, use the
--ask-vault-pass option when running the playbook.
