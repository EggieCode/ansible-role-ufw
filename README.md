UFW Rules setup
##############

Ansible playbook rule for setting up UFW. With support for IPv4/IPv6 forwarding.

Requirements 
---------

Testing on Ubuntu 16.04

Variables
---------
- default.yml
Explanation:
```yaml


ufw.kernel_modules:  	      _#Set iptables kernel modules_
ufw.policy:  		      _#Set default policy to deny/allow_

ufw.forwarding: []            _#IPv4 forwarding rules_
  - comment:                  _#Comment_
    incomming_dev:            _#Incomming interface_
    incomming_network:        _#Incomming network/subnet_
    outgoing_dev:             _#Outgoing interface_
    outgoing_network:         _#Outgoing network/subnet_
    masquerading:             _#Enable masquerading (boolean)_
    conntrack_state:          _#Incomming traffic ctstat setting _
    reroute: []               _#Reroute outgoing IP of host (Useful for internal subnets)_
      - comment:              _#Comment_
        routed_ip:            _#Reroute IP_
        source_ip:            _#Source is internal ip where is routed out_
    forwards: []              _#Port forwarding_
      - comment:              _#Comment_
        protocols: []         _#Protocol. TCP/UDP as array_
        allowed_sources: []   _#Allowed IPs_
        incomming_ip:         _#Orignal destiantion ip_
        incomming_port:       _#Orignal destiantion port_
        destination_ip:       _#Outgoing IP addresss_
        destination_port:     _#Outgoing IP addresss_

ufw.forwarding6: []           _#_#IPv4 forwarding rules_
  - incomming_dev:            _#Incomming interface_
    incomming_network:        _#Incomming network/subnet_
    outgoing_dev:             _#Outgoing interface_
    outgoing_network:         _#Outgoing network/subnet_
    conntrack_state:          _#Incomming traffic ctstat setting_
    forwards: []              _#Port forwarding
      - destination_network:  _#Outgoing network/subnet addresss_
        destination_port:     _#Outgoing IP addresss_
        protocols:            _#Protocol_

```

Custom rules
------------

If you want to add custom rules to you machine(s) just use UFW module of ansible:
http://docs.ansible.com/ansible/ufw_module.html

Example playbook
----------------

Simple example with custom ufw rules
```yaml
- name: Setup UFW 
  hosts: all
  roles:
    - ufw

- name: Custom UFW rules
  hosts: all
  tasks:
    - name: Allow OpenSSH on port 22
      ufw: rule=allow name=OpenSSH
    - name: Allow HTTP 
      ufw: rule=allow port=80 proto=tcp 
    - name: Allow HTTPS 
      ufw: rule=allow port=https proto=tcp 
    - name: Allow port 8443 from 1 host 
      ufw: rule=allow interface="{{ item.incomming_dev }}" direction=in proto=tcp src="2001:db8:1337:beef:cafe::1" to_port=8443
      with_items:
        - "{{ ufw.forwarding6 }}"
    
```


Licence
-------

MIT

Author
-------

Egbert Verhage <egbert@eggiecode.org>
