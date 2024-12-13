#!/usr/bin/python

# Copyright: (c) 2024, Your Name <your.email@example.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
from ansible.module_utils.basic import AnsibleModule
from freebox_api import Freepybox
import asyncio

DOCUMENTATION = r'''
---
module: lpi_code.freebox.nat

short_description: Configures NAT (Network Address Translation) rules on a Freebox router.

version_added: "1.0.0"

description: |
    This module configures NAT rules (port forwarding, etc.) on a Freebox router.
    It requires the Freebox API to be accessible and valid credentials for authentication.

options:
    freebox_url:
        description: The URL of the Freebox device (default: 'mafreebox.freebox.fr').
        required: false
        type: str
        default: 'mafreebox.freebox.fr'

    lan_ip:
        description: The internal IP address to forward the traffic to.
        required: true
        type: str

    lan_port:
        description: The internal port to forward the traffic to.
        required: true
        type: int

    wan_port_start:
        description: The starting external port to forward.
        required: true
        type: int

    wan_port_end:
        description: The ending external port to forward.
        required: true
        type: int

    ip_proto:
        description: The protocol for the NAT rule (either 'tcp' or 'udp').
        required: true
        type: str
        choices:
            - tcp
            - udp

    src_ip:
        description: The source IP address allowed for the NAT rule (default: '0.0.0.0').
        required: false
        type: str
        default: '0.0.0.0'

    enabled:
        description: Whether the NAT rule is enabled or not (true/false).
        required: true
        type: bool

    comment:
        description: A comment for the NAT rule.
        required: false
        type: str

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Configure NAT rule for TCP protocol, port range, and internal forwarding
- name: Set NAT rule on Freebox
  freebox_nat:
    freebox_url: "mafreebox.freebox.fr"
    lan_ip: "192.168.1.42"
    lan_port: 4242
    wan_port_start: 4242
    wan_port_end: 4242
    ip_proto: "tcp"
    src_ip: "0.0.0.0"
    enabled: true
    comment: "Test NAT rule"

# Configure NAT rule for UDP protocol, with a port range
- name: Set UDP NAT rule on Freebox
  freebox_nat:
    freebox_url: "mafreebox.freebox.fr"
    lan_ip: "192.168.1.100"
    lan_port: 12345
    wan_port_start: 12345
    wan_port_end: 12345
    ip_proto: "udp"
    src_ip: "0.0.0.0"
    enabled: true
    comment: "Test UDP rule"
'''

RETURN = r'''
original_message:
    description: The original parameters passed to the module.
    type: str
    returned: always
    sample: '{"lan_ip": "192.168.1.42", "lan_port": 4242, "wan_port_start": 4242, "wan_port_end": 4242, "ip_proto": "tcp", "src_ip": "0.0.0.0", "enabled": true}'

message:
    description: The status message from the Freebox API.
    type: str
    returned: always
    sample: 'NAT rule configured successfully'

lan_ip:
    description: The internal IP address to which traffic is forwarded.
    type: str
    returned: always
    sample: '192.168.1.42'

lan_port:
    description: The internal port to which traffic is forwarded.
    type: int
    returned: always
    sample: 4242

wan_port_start:
    description: The starting external port for the NAT rule.
    type: int
    returned: always
    sample: 4242

wan_port_end:
    description: The ending external port for the NAT rule.
    type: int
    returned: always
    sample: 4242

ip_proto:
    description: The protocol for the NAT rule (either 'tcp' or 'udp').
    type: str
    returned: always
    sample: 'tcp'

src_ip:
    description: The source IP address allowed for the NAT rule.
    type: str
    returned: always
    sample: '0.0.0.0'

enabled:
    description: Whether the NAT rule is enabled.
    type: bool
    returned: always
    sample: true

comment:
    description: A comment for the NAT rule.
    type: str
    returned: always
    sample: 'Test NAT rule'
'''

async def configure_nat(freebox_url, lan_ip, lan_port, wan_port_start, wan_port_end, ip_proto, src_ip, enabled, comment, session_token):
    """
    Configures the NAT (Network Address Translation) rule on the Freebox router.

    Args:
        freebox_url (str): The URL of the Freebox device.
        lan_ip (str): The internal IP address to forward the traffic to.
        lan_port (int): The internal port to forward the traffic to.
        wan_port_start (int): The starting external port to forward.
        wan_port_end (int): The ending external port to forward.
        ip_proto (str): The protocol (TCP/UDP) for the NAT rule.
        src_ip (str): The source IP address allowed for the NAT rule.
        enabled (bool): Whether the rule is enabled or disabled.
        comment (str): A comment for the NAT rule.
        session_token (str): The authentication token for the Freebox API.

    Returns:
        bool: True if the NAT configuration is successful. False if nothing changed.

    Raises:
        Exception: If the configuration fails.
    """
    try:
        # Connect to the Freebox API
        fb = Freepybox()
        await fb.open(freebox_url, 443)

        # Check if the NAT rule already exists
        nat_rules = await fb.fw.get_all_port_forwarding_configuration()
        for rule in nat_rules:
            if (rule['lan_ip'] == lan_ip and
                rule['lan_port'] == lan_port and
                rule['wan_port_start'] == wan_port_start and
                rule['wan_port_end'] == wan_port_end and
                rule['ip_proto'].upper() == ip_proto.upper()):
                return False  # Rule already exists

        # Make the request to configure the NAT rule
        result = await fb.fw.create_port_forwarding_configuration(
            {
                "enabled": enabled,
                "comment": comment,
                "lan_port": lan_port,
                "wan_port_start": wan_port_start,
                "wan_port_end": wan_port_end,
                "lan_ip": lan_ip,
                "ip_proto": ip_proto,
                "src_ip": src_ip
            }
        )

        if result.get("enabled") is not None:
            return True
        else:
            raise Exception(f"Failed to configure NAT rule: {result['msg']}")
    
    except Exception as e:
        raise Exception(f"Error configuring NAT: {str(e)}")


async def run_module():
    # Define the arguments/parameters that can be passed to the module
    module_args = dict(
        freebox_url=dict(type='str', required=False, default='mafreebox.freebox.fr'),
        lan_ip=dict(type='str', required=True),
        lan_port=dict(type='int', required=True),
        wan_port_start=dict(type='int', required=True),
        wan_port_end=dict(type='int', required=True),
        ip_proto=dict(type='str', required=True, choices=['tcp', 'udp']),
        src_ip=dict(type='str', required=False, default='0.0.0.0'),
        enabled=dict(type='bool', required=True),
        comment=dict(type='str', required=False, default="")
    )

    # Seed the result dictionary
    result = dict(
        changed=False,
        original_message='',
        message='',
        lan_ip='',
        lan_port=0,
        wan_port_start=0,
        wan_port_end=0,
        ip_proto='',
        src_ip='',
        enabled=False,
        comment=''
    )

    # Instantiate the AnsibleModule object
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Extract the parameters
    freebox_url = module.params['freebox_url']
    lan_ip = module.params['lan_ip']
    lan_port = module.params['lan_port']
    wan_port_start = module.params['wan_port_start']
    wan_port_end = module.params['wan_port_end']
    ip_proto = module.params['ip_proto']
    src_ip = module.params['src_ip']
    enabled = module.params['enabled']
    comment = module.params['comment']

    # Try to configure the NAT rule and handle errors
    try:
        # Authenticate and configure NAT rule
        session_token = 'your_session_token'  # Replace with actual authentication token or session
        result['changed'] = await configure_nat(freebox_url, lan_ip, lan_port, wan_port_start, wan_port_end, ip_proto, src_ip, enabled, comment, session_token)
        result['message'] = f"NAT rule configured for {ip_proto} from external port {wan_port_start} to internal {lan_ip}:{lan_port}"
        result['lan_ip'] = lan_ip
        result['lan_port'] = lan_port
        result['wan_port_start'] = wan_port_start
        result['wan_port_end'] = wan_port_end
        result['ip_proto'] = ip_proto
        result['src_ip'] = src_ip
        result['enabled'] = enabled
        result['comment'] = comment

        # Return the result
        module.exit_json(**result)

    except Exception as e:
        # In case of an error, return a failure message
        result['message'] = str(e)
        module.fail_json(msg=result['message'], **result)


def main():
    asyncio.run(run_module())


if __name__ == '__main__':
    main()
