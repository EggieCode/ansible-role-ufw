#!/usr/bin/python

from ansible.module_utils.basic import *

class UFWForwards(object):
    def __init__(self, data, ipv6):
        self.ufw_chain = "ufw6" if ipv6 else 'ufw'

        self.nat_rules = []
        self.filter_rules = []
        
        self.reroute_data = []
        self.port_forward_data = []

        args = [
           'incomming_dev', 
           'incomming_network', 
           'outgoing_dev', 
           'outgoing_network', 
           'masquerading', 
           'conntrack_state'
        ]

        if 'reroute' in data:
            self.reroute_data = data['reroute'] 
        else:
            self.reroute_data = []
        
        if 'forwards' in data:
            self.port_forward_data = data['forwards'] 
        else:
            self.port_forward_data = [] 

        for arg in args:
            if arg in data:
                setattr(self, arg, data[arg])
            else:
                setattr(self, arg, None)
        
    def generate(self):
        if self.masquerading:
            for item in self.reroute_data:
                self._reroute_generate(item)

        for item in self.port_forward_data:
            self._port_forward(item)

        if self.masquerading:
            self._masquerade_generate()
        self._forward_generate()
    
    def _port_forward(self, item):
        for k in ['destination_port', 'incomming_port', 'protocol']:
            if k not in item:
                item[k] = [None]
            if not isinstance(item[k], list):
                item[k] = [str(item[k])] 

        if item['incomming_port'][0] is None and len(item['destination_port']) > 1:
            item['incomming_port'] = [None for i in range(len(item['destination_port']))]

        for protocol in item['protocol']:
            ports = zip(item['incomming_port'], item['destination_port'])
            for in_port, dport in ports:
                print(item, protocol, dport)
                self._port_forward_generate(item, protocol, dport)
                if self.masquerading:
                    self._port_forward_dnat_generate(item, protocol, in_port, dport)


    def _reroute_generate(self, item):
        rule = ["-A", "POSTROUTING"]

        if self.incomming_dev:
            rule += ['-o', self.incomming_dev]
        if 'source_ip' in item:
            rule += ['-s', item['source_ip']]
        
        rule += ['-j', 'SNAT']
        rule += ["--to-source", item['routed_ip']]
        if rule not in self.nat_rules:
            self.nat_rules.append(rule)

    def _port_forward_dnat_generate(self, item, protocol, in_port, dport):
        rule = ["-A", "PREROUTING"]

        if self.incomming_dev:
            rule += ['-i', self.incomming_dev]
        if 'incomming_ip' in item:
            rule += ['-d', item['incomming_ip']]

        rule += ['-p', protocol]
        rule += ['-m', protocol]
        rule += ['--dport', str(in_port)]
        rule += ['-j', 'DNAT']
        if self.ufw_chain == "ufw6":
            rule += ["--to-destination", "[{}]:{}".format(item['destination_ip'], str(dport))]
        else:
            rule += ["--to-destination", "{}:{}".format(item['destination_ip'], str(dport))]
        if rule not in self.nat_rules:
            self.nat_rules.append(rule)


    def _port_forward_generate(self, item, protocol, dport):

        rule = ["-A", self.ufw_chain + "-before-forward"]
        
        if self.incomming_dev:
            rule += ['-i', self.incomming_dev]
        if self.outgoing_dev:
            rule += ['-o', self.outgoing_dev]
        if 'destination_ip' in item:
            rule += ['-d', item['destination_ip']]
        elif 'destination_network' in item:
            rule += ['-d', item['destination_network']]

        if protocol and dport:
            rule += ['-p', protocol]
            rule += ['-m', protocol]
            rule += ['--dport', str(dport)]

        rule += ['-j', 'ACCEPT']
        if rule not in self.filter_rules:
            self.filter_rules.append(rule)
        
    
    def _masquerade_generate(self):
        rule = ["-A", "POSTROUTING"]

        if self.incomming_dev:
            rule += ['-o', self.incomming_dev]
        if self.incomming_network:
            rule += ['-d', self.incomming_network]
        if self.outgoing_network:
            rule += ['-s', self.outgoing_network]
        rule += ['-j', 'MASQUERADE']
        
        if rule not in self.nat_rules:
            self.nat_rules.append(rule)

    def _forward_generate(self):
        for i in [('i','s','o','d'),('o','d','i','s')]:
            rule = ["-A", self.ufw_chain + "-before-forward"]
            if self.incomming_dev:
                rule += ['-' + i[0], self.incomming_dev]
            if self.outgoing_dev:
                rule += ['-' + i[2], self.outgoing_dev]
            if self.incomming_network:
                rule += ['-' + i[1], self.incomming_network]
            if self.outgoing_network:
                rule += ['-' + i[3], self.outgoing_network]
            if i[0] == 'i' and self.conntrack_state:
                rule += ['-m conntrack', '--ctstate', self.conntrack_state]
                
            rule += ['-j', 'ACCEPT']
            if rule not in self.filter_rules:
                self.filter_rules.append(rule)

        rule = ["-A", self.ufw_chain + "-before-forward"]
        rule += ['-i', self.outgoing_dev]
        rule += ['-o', self.outgoing_dev]
        rule += ['-j', 'ACCEPT']
        if rule not in self.filter_rules:
            self.filter_rules.append(rule)
    
def main():
    
    fields = {
        "data" : {"required": True, "type": "list"},
        "ipv6" : {"default": False, "type": "bool"},
    }
    module = AnsibleModule(argument_spec=fields)
    response = {
        'nat_rules' : [],
        'filter_rules' : []
    }

    for item in module.params['data']:
        ufw_forwards = UFWForwards(item, module.params['ipv6'])
        ufw_forwards.nat_rules = response['nat_rules']
        ufw_forwards.filter_rules = response['filter_rules']
        ufw_forwards.generate()

    module.exit_json(changed=False, meta=response)


if __name__ == '__main__':  
    main()

