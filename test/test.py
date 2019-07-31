#!/usr/bin/env python3

import imp
import os
import unittest
from pprint import pprint
imp.load_source('ufw_forward', os.path.join(os.path.dirname(__file__), os.path.pardir, 'library', 'ufw_forward.py'))
from ufw_forward import UFWForwards




class TestBase(unittest.TestCase):
  def test_do_magic(self):

    test = {  "incomming_dev": "eth0",
              "outgoing_dev": "lxdbr0",
              "outgoing_network": "10.20.10.0/24",
              "masquerading": True,
              "conntrack_state": "RELATED,ESTABLISHED",
              "reroute": [],
              "forwards": [
                  {
                      "container": "mumble.baviaan.eggie.zone",
                      "destination_ip": "10.20.10.11",
                      "destination_port": [
                          64738
                      ],
                      "incomming_ip": "88.99.152.112",
                      "incomming_port": [
                          64738
                      ],
                      "protocol": [
                          "tcp",
                          "udp"
                      ]
                  },
                  {
                      "container": "brandon-minecraft.baviaan.eggie.zone",
                      "destination_ip": "10.20.10.12",
                      "destination_port": [
                          25565
                      ],
                      "incomming_ip": "88.99.152.112",
                      "incomming_port": [
                          25565
                      ],
                      "protocol": [
                          "tcp"
                      ]
                  }
              ]
           }

    response = {
        'nat_rules' : [],
        'filter_rules' : []
    }

    ufw_forwards = UFWForwards(test, False)
    ufw_forwards.nat_rules = response['nat_rules']
    ufw_forwards.filter_rules = response['filter_rules']

    ufw_forwards.generate()

    for rule in response['nat_rules']:
        print(" ".join(rule))
    pprint(response['filter_rules']))
    for rule in response['filter_rules']:
        print(" ".join(rule))


if __name__ == '__main__':
    unittest.main()
