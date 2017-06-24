UFW Rules setup
##############

Ansible playbook rule for setting up UFW. With support for IPv4/IPv6 forwarding.

Requirements 
---------

Testing on Ubuntu 16.04

Variables
---------

<tt>default.yml</tt> (Default can be found there)

*<tt>ufw.kernel_modules: </tt> Set iptables kernel modules
*<tt>ufw.policy: </tt> Set default policy to deny/allow 

*<tt>ufw.forwarding: [] </tt> IPv4 forwarding rules 
**<tt>	- comment: </tt> Comment
**<tt>	  incomming_dev: </tt> Incomming interface 
**<tt>	  incomming_network: </tt> Incomming network/subnet 
**<tt>	  outgoing_dev: </tt> Outgoing interface
**<tt>	  outgoing_network: </tt> Outgoing network/subnet 
**<tt>	  masquerading: </tt> Enable masquerading yes or no
**<tt>	  conntrack_state: </tt> Incomming traffic ctstat setting 
**<tt>	  reroute: [] </tt> Reroute outgoing IP of host (Usefull for internal subnets) 
***<tt>	    - comment: </tt> Comment 
***<tt>	      routed_ip: </tt> Reroute IP
***<tt>	      source_ip: </tt> Source is internal ip where is routed out
**<tt>	  forwards: [] </tt> Port forwarding 
***<tt>	    - comment: </tt> Comment 
***<tt>	      protocols: [] </tt> Protocol. TCP/UDP as array
***<tt>	      allowed_sources: [] </tt> Allowed IPs 
***<tt>	      incomming_ip: </tt> Orignal destiantion ip 
***<tt>	      incomming_port: </tt> Orignal destiantion port 
***<tt>	      destination_ip: </tt> Outgoing IP addresss 
***<tt>	      destination_port: </tt> Outgoing IP addresss 

*<tt>ufw.forwarding6: [] </tt> IPv4 forwarding rules 
**<tt>	  incomming_dev: </tt> Incomming interface 
**<tt>	  incomming_network: </tt> Incomming network/subnet 
**<tt>	  outgoing_dev: </tt> Outgoing interface
**<tt>	  outgoing_network: </tt> Outgoing network/subnet 
**<tt>	  conntrack_state: </tt> Incomming traffic ctstat setting 
**<tt>	  forwards: []</tt> Port forwarding
***<tt>	      destination_network: </tt> Outgoing network/subnet addresss
***<tt>	      destination_port: </tt> Outgoing IP addresss 

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
