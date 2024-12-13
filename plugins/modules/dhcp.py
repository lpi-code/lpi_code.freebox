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
module: freebox_static_dhcp

short_description: Configures static DHCP mappings on a Freebox router.

version_added: "1.0.0"

description: |
    This module configures a static DHCP binding on a Freebox router.
    It requires the Freebox API to be accessible and valid credentials for authentication.

options:
    freebox_url:
        description: The URL of the Freebox device (default: 'mafreebox.freebox.fr').
        required: false
        type: str
        default: 'mafreebox.freebox.fr'

    mac:
        description: The MAC address of the device to be configured for static DHCP.
        required: true
        type: str

    ip:
        description: The static IP address (either IPv4 or IPv6) to assign to the device.
        required: true
        type: str

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Configure static DHCP for a device
- name: Set static DHCP lease on Freebox
  freebox_static_dhcp:
    freebox_url: "mafreebox.freebox.fr"
    mac: "00:11:22:33:44:55"
    ip: "192.168.1.100"

# Configure static DHCP for a device with IPv6
- name: Set static DHCP lease for IPv6
  freebox_static_dhcp:
    freebox_url: "mafreebox.freebox.fr"
    mac: "00:11:22:33:44:55"
    ip: "2001:db8::1"
'''

RETURN = r'''
original_message:
    description: The original parameters passed to the module.
    type: str
    returned: always
    sample: '00:11:22:33:44:55'
    
message:
    description: The status message from the Freebox API.
    type: str
    returned: always
    sample: 'Static DHCP configured successfully'

mac_address:
    description: The MAC address for which the static DHCP lease was configured.
    type: str
    returned: always
    sample: '00:11:22:33:44:55'

ip_address:
    description: The IP address configured for the device.
    type: str
    returned: always
    sample: '192.168.1.100'
'''

async def configure_static_dhcp(freebox_url, mac, ip, session_token):
    """
    Configures the static DHCP mapping for the given MAC address and IP.

    Args:
        freebox_url (str): The URL of the Freebox device.
        mac (str): The MAC address to configure.
        ip (str): The static IP address to assign.
        session_token (str): The authentication token for the Freebox API.

    Returns:
        bool: True if the static DHCP configuration is successful. False if nothing changed

    Raises:
        Exception: If the configuration fails.
    """
    try:
        # Connect to the Freebox API
        fb = Freepybox()
        await fb.open(freebox_url, 443)
        # check if does not already exist
        static_confs = await fb.dhcp.get_dhcp_static_leases()
        i = 0
        while i < len(static_confs) and static_confs[i]['mac'].upper() != mac.upper():
            i+= 1
        found_mac = i < len(static_confs) and static_confs[i]['mac'].upper() == mac.upper()
        if found_mac:
            # TODO use a put request to update data
            return False
        

        # Make the request to configure static DHCP
        result = await fb.dhcp.create_dhcp_static_lease(
            {
                "ip" : ip,
                "mac" : mac
            }
        )
        
        if result.get("mac"):
            return True
        else:
            raise Exception(f"Failed to configure static DHCP: {result['msg']}")
    
    except Exception as e:
        raise Exception(f"Error configuring static DHCP: {str(e)}")


async def run_module():
    # Define the arguments/parameters that can be passed to the module
    module_args = dict(
        freebox_url=dict(type='str', required=False, default='mafreebox.freebox.fr'),
        mac=dict(type='str', required=True),
        ip=dict(type='str', required=True)
    )

    # Seed the result dictionary
    result = dict(
        changed=False,
        original_message='',
        message='',
        mac_address='',
        ip_address=''
    )

    # Instantiate the AnsibleModule object
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Extract the parameters
    freebox_url = module.params['freebox_url']
    mac = module.params['mac']
    ip = module.params['ip']

    # Try to configure static DHCP and handle errors
    try:
        # Authenticate and configure static DHCP
        session_token = 'your_session_token'  # Replace with actual authentication token or session
        result['changed'] = await configure_static_dhcp(freebox_url, mac, ip, session_token)
        result['message'] = f"Static DHCP configured for MAC {mac} with IP {ip}"
        result['mac_address'] = mac
        result['ip_address'] = ip

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
