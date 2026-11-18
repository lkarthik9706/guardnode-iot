import os
import sys

SCAPY_AVAILABLE = False
try:
    from scapy.all import get_if_list, conf, IFACES
    SCAPY_AVAILABLE = True
except Exception:
    SCAPY_AVAILABLE = False


def is_routable_ip(ip: str) -> bool:
    """Checks if an IP address is a valid non-loopback, non-APIPA address."""
    if not ip or ip == "No IP" or not isinstance(ip, str):
        return False
    ip_str = ip.strip()
    if ip_str.startswith("127.") or ip_str.startswith("169.254.") or ip_str == "0.0.0.0":
        return False
    return True


def get_default_scapy_interface():
    """Returns the primary active network interface as determined by Scapy."""
    if not SCAPY_AVAILABLE:
        return "default"
    try:
        if hasattr(conf, "iface") and conf.iface is not None:
            # conf.iface can be an interface object or string
            return str(getattr(conf.iface, "name", conf.iface))
    except Exception:
        pass
    return "default"


def resolve_active_interface(requested: str = "default") -> str:
    """
    Safely resolves a requested interface ID.
    If requested is 'default', empty, or a virtual WAN Miniport,
    automatically resolves to the system's active internet adapter.
    """
    if not SCAPY_AVAILABLE:
        return requested or "default"

    default_iface = get_default_scapy_interface()

    if not requested or requested in ["default", "auto", "None", ""]:
        return default_iface

    # If requested interface is in IFACES, check if it's a dummy WAN Miniport
    try:
        if hasattr(IFACES, "data") and requested in IFACES.data:
            desc = getattr(IFACES.data[requested], "description", "")
            ip = getattr(IFACES.data[requested], "ip", "")
            mac = getattr(IFACES.data[requested], "mac", "")
            if "WAN Miniport" in desc or (not ip and not mac):
                print(f"[INFO] Requested interface '{desc}' is a virtual WAN Miniport. Auto-resolving to active adapter: {default_iface}")
                return default_iface
    except Exception:
        pass

    return requested


def detect_network_interfaces():
    """
    Detects available network interfaces on the local system.
    Filters out virtual WAN Miniports and prioritizes the active physical adapter.
    """
    active_interfaces = []
    other_interfaces = []

    if SCAPY_AVAILABLE:
        try:
            default_iface_str = get_default_scapy_interface()

            if hasattr(IFACES, "data"):
                for iface_name, iface_obj in IFACES.data.items():
                    name_str = getattr(iface_obj, "name", str(iface_name))
                    desc_str = getattr(iface_obj, "description", name_str)
                    ip_str = getattr(iface_obj, "ip", "")
                    mac_str = getattr(iface_obj, "mac", "")

                    # 1. Filter out virtual WAN Miniports that never receive packets
                    if "WAN Miniport" in desc_str:
                        continue
                    if not mac_str and not ip_str:
                        continue

                    is_active = (
                        is_routable_ip(ip_str) or
                        str(iface_name) == default_iface_str or
                        name_str == default_iface_str
                    )

                    clean_name = f"{name_str} ({desc_str})" if name_str != desc_str else name_str
                    if ip_str:
                        clean_name += f" - {ip_str}"

                    if is_active:
                        clean_name += " [ACTIVE]"
                        active_interfaces.append({
                            "id": str(iface_name),
                            "name": clean_name,
                            "description": f"{desc_str} (IP: {ip_str or 'DHCP'}, MAC: {mac_str or 'N/A'})",
                            "available": True,
                            "is_active": True
                        })
                    else:
                        other_interfaces.append({
                            "id": str(iface_name),
                            "name": clean_name,
                            "description": f"{desc_str} (IP: {ip_str or 'None'})",
                            "available": True,
                            "is_active": False
                        })

            if not active_interfaces and not other_interfaces:
                raw_list = get_if_list()
                for i, ifname in enumerate(raw_list):
                    if "WAN Miniport" in str(ifname):
                        continue
                    other_interfaces.append({
                        "id": str(ifname),
                        "name": f"Interface #{i+1}: {ifname}",
                        "description": f"Network Adapter {ifname}",
                        "available": True,
                        "is_active": False
                    })
        except Exception as e:
            print(f"[WARNING] Scapy interface detection error: {e}")

    # Build prioritized list: Active interfaces first, then secondary
    all_adapters = active_interfaces + other_interfaces

    # Add smart auto-detect option at the very top
    primary_label = "Auto-Detect Default Adapter"
    if active_interfaces:
        primary_label = f"Auto: {active_interfaces[0]['name']}"

    final_list = [
        {
            "id": "default",
            "name": primary_label,
            "description": "Automatically routes packet capture via the system's primary active network adapter",
            "available": True,
            "is_active": True
        }
    ] + all_adapters

    return final_list
