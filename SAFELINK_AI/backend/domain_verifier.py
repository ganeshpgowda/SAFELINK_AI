"""SafeLink AI - Domain Existence & DNS Verification Engine.

Performs safe, lightweight DNS address verification without sending HTTP requests
or loading remote content from the evaluated URL.
"""

import socket
import ipaddress
from typing import Dict, Any, List


def check_domain_existence(host: str, timeout: float = 3.5) -> Dict[str, Any]:
    """Verifies whether the submitted host / domain exists in global DNS.
    
    Safe & Privacy-Preserving: Performs purely standard DNS resolution
    (getaddrinfo). Does NOT open TCP connections, HTTP requests, or fetch payloads.
    """
    clean_host = host.split(":")[0].strip("[] ").lower()
    
    if not clean_host:
        return {
            "exists": False,
            "status": "Invalid Hostname",
            "resolved_ips": [],
            "explanation": "No valid hostname provided for domain verification."
        }

    # Check if host is already a raw IP address
    try:
        ipaddress.ip_address(clean_host)
        return {
            "exists": True,
            "status": "Direct IP Address",
            "resolved_ips": [clean_host],
            "explanation": f"Host is a raw numerical IP address ({clean_host}), not a domain name."
        }
    except ValueError:
        pass

    # Save original default timeout and set temporary socket timeout
    orig_timeout = socket.getdefaulttimeout()
    try:
        socket.setdefaulttimeout(timeout)
        addr_info = socket.getaddrinfo(clean_host, None, family=socket.AF_UNSPEC, type=socket.SOCK_STREAM)
        
        # Extract unique IP addresses
        resolved_ips: List[str] = []
        for item in addr_info:
            ip = item[4][0]
            if ip not in resolved_ips:
                resolved_ips.append(ip)
                
        if resolved_ips:
            return {
                "exists": True,
                "status": "Active / Resolving Domain",
                "resolved_ips": resolved_ips[:5],  # Cap at 5 for concise display
                "explanation": f"The domain '{clean_host}' actively exists and resolves in global DNS to: {', '.join(resolved_ips[:3])}."
            }
        else:
            return {
                "exists": False,
                "status": "No IP Records Found",
                "resolved_ips": [],
                "explanation": f"The domain '{clean_host}' did not return any A/AAAA address records."
            }

    except (socket.gaierror, socket.herror) as e:
        # Host name resolution failure (NXDOMAIN / Name or service not known)
        return {
            "exists": False,
            "status": "Non-Existent / Inactive (NXDOMAIN)",
            "resolved_ips": [],
            "explanation": (
                f"Domain '{clean_host}' does NOT exist in global DNS (NXDOMAIN). "
                "This indicates either a fabricated link, a domain already suspended/takedown by security teams, or an inactive server."
            )
        }
    except socket.timeout:
        return {
            "exists": False,
            "status": "DNS Lookup Timed Out",
            "resolved_ips": [],
            "explanation": f"DNS resolution for '{clean_host}' timed out after {timeout}s. The authoritative nameservers may be unreachable."
        }
    except Exception as e:
        return {
            "exists": False,
            "status": "Unresolvable",
            "resolved_ips": [],
            "explanation": f"Domain lookup failed: {str(e)}"
        }
    finally:
        socket.setdefaulttimeout(orig_timeout)

