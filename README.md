# Ansible Collection - lpi_code.freebox

A collection of Ansible modules for managing Freebox router configurations through the Freebox API.

## Overview

This Ansible collection provides modules to configure and manage Freebox router settings, specifically focusing on DHCP static leases and NAT (Network Address Translation) rules. The collection leverages the `freebox-api` Python library to interact with Freebox routers via their REST API.

## Collection Information

- **Namespace**: `lpi_code`
- **Name**: `freebox`
- **Version**: `1.0.0`
- **License**: GPL-2.0-or-later
- **Ansible Version**: Requires Ansible 2.9.10 or higher

## Requirements

### Python Dependencies

The collection requires the following Python packages (see `requirements.txt`):

- `freebox-api==1.1.0` - Python library for Freebox API interaction
- `aiohttp==3.11.10` - Async HTTP client/server framework
- `asyncio` - Asynchronous I/O support
- Additional dependencies for async operations

### System Requirements

- Python 3.6+
- Ansible 2.9.10+
- Network access to Freebox router
- Valid Freebox API credentials

## Modules

### 1. freebox_static_dhcp

Configures static DHCP mappings on a Freebox router.

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `freebox_url` | str | No | `mafreebox.freebox.fr` | URL of the Freebox device |
| `mac` | str | Yes | - | MAC address of the device |
| `ip` | str | Yes | - | Static IP address (IPv4 or IPv6) |

#### Example Usage

```yaml
- name: Configure static DHCP lease
  lpi_code.freebox.freebox_static_dhcp:
    freebox_url: "mafreebox.freebox.fr"
    mac: "00:11:22:33:44:55"
    ip: "192.168.1.100"

- name: Configure IPv6 static DHCP lease
  lpi_code.freebox.freebox_static_dhcp:
    mac: "00:11:22:33:44:55"
    ip: "2001:db8::1"
```

#### Return Values

- `changed`: Boolean indicating if changes were made
- `message`: Status message from the operation
- `mac_address`: The configured MAC address
- `ip_address`: The assigned IP address

### 2. freebox_nat

Configures NAT (port forwarding) rules on a Freebox router.

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `freebox_url` | str | No | `mafreebox.freebox.fr` | URL of the Freebox device |
| `lan_ip` | str | Yes | - | Internal IP address to forward to |
| `lan_port` | int | Yes | - | Internal port to forward to |
| `wan_port_start` | int | Yes | - | Starting external port |
| `wan_port_end` | int | Yes | - | Ending external port |
| `ip_proto` | str | Yes | - | Protocol (`tcp` or `udp`) |
| `src_ip` | str | No | `0.0.0.0` | Source IP restriction |
| `enabled` | bool | Yes | - | Enable/disable the rule |
| `comment` | str | No | `""` | Rule description |

#### Example Usage

```yaml
- name: Configure TCP port forwarding
  lpi_code.freebox.freebox_nat:
    lan_ip: "192.168.1.42"
    lan_port: 4242
    wan_port_start: 4242
    wan_port_end: 4242
    ip_proto: "tcp"
    enabled: true
    comment: "Web server access"

- name: Configure UDP port range forwarding
  lpi_code.freebox.freebox_nat:
    lan_ip: "192.168.1.100"
    lan_port: 12345
    wan_port_start: 12345
    wan_port_end: 12345
    ip_proto: "udp"
    src_ip: "192.168.1.0/24"
    enabled: true
    comment: "Gaming server"
```

#### Return Values

- `changed`: Boolean indicating if changes were made
- `message`: Status message from the operation
- `lan_ip`: Internal IP address
- `lan_port`: Internal port
- `wan_port_start`: Starting external port
- `wan_port_end`: Ending external port
- `ip_proto`: Protocol used
- `src_ip`: Source IP restriction
- `enabled`: Rule status
- `comment`: Rule description

## Installation

### From Galaxy (when published)

```bash
ansible-galaxy collection install lpi_code.freebox
```

### From Source

```bash
git clone <repository-url>
cd lpi_code.freebox
ansible-galaxy collection build
ansible-galaxy collection install lpi_code-freebox-1.0.0.tar.gz
```

## Authentication

**Important**: Both modules currently use a placeholder session token (`'your_session_token'`). Before using these modules in production, you must implement proper authentication with the Freebox API.

The Freebox API typically requires:
1. Application registration
2. User authorization
3. Session token management

Refer to the [Freebox API documentation](https://dev.freebox.fr/sdk/os/) for proper authentication implementation.

## Testing

The collection includes basic integration tests:

### DHCP Module Test
```yaml
- name: Set a random dhcp lease
  lpi_code.freebox.dhcp:
    ip: "192.168.0.116"
    mac: "ac:fd:ce:22:0e:84"
```

### NAT Module Test
```yaml
- name: Set a random NAT rule
  lpi_code.freebox.nat:
    lan_ip: "192.168.0.116"
    lan_port: 12345
    wan_port_start: 12345
    wan_port_end: 12345
    ip_proto: "udp"
    src_ip: "0.0.0.0"
    enabled: true
    comment: "Test UDP rule"
```

## Known Issues and Limitations

1. **Authentication**: Session token is hardcoded and needs proper implementation
2. **Error Handling**: Limited error handling for API failures
3. **Idempotency**: DHCP module has incomplete idempotency check (TODO comment in code)
4. **Update Operations**: DHCP module doesn't support updating existing rules
5. **Check Mode**: Modules support check mode but may not be fully implemented

## Development Status

This collection is in development and may have incomplete features. Key areas for improvement:

- Implement proper authentication mechanism
- Complete idempotency checks
- Add support for updating existing configurations
- Enhance error handling and validation
- Add more comprehensive testing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This collection is licensed under the GPL-2.0-or-later license. See the LICENSE file for details.

## Support

For issues and questions:
- Check the [Freebox API documentation](https://dev.freebox.fr/sdk/os/)
- Review the module documentation and examples
- Open an issue in the project repository

## Changelog

### Version 1.0.0
- Initial release
- Added `freebox_static_dhcp` module
- Added `freebox_nat` module
- Basic integration tests
- Collection structure and metadata