import time
import json
import logging
import requests
import scapy.all as s

def lookup_mac_addr(mac: str) -> str:
    url = f'https://www.macvendorlookup.com/api/v2/{mac}/json'
    logging.debug(url)

    try:
        response = requests.get(url)
    except Exception as e:
        logging.exception(e)

    if response.status_code == 200:
        company = json.loads(response.content)[0].get('company')
        return company
    else:
        logging.debug(
            f'Response code: {response.status_code}, body: {response.text}'
        )


def get_mac_vendor(mac: str) -> str:
    """
    Takes in a MAC address as a string and returns the vendor of that address.
    If the vendor cannot be determined, the function returns 'Unknown'.
    :param mac: the mac address in question
    :return: the vendor name or 'Unknown' if not found
    """
    vendor = lookup_mac_addr(mac)

    if vendor:
        return vendor
    
    else:
        logging.debug('checking lookup file for mac address...')
        mac = mac.upper().replace(':', '')[0:6]
        try:
            with open("mac-vendor.txt", "r", encoding='utf-8') as f:
                for line in f:
                    if mac in line:
                        return line[7:]
        except FileNotFoundError:
            exit("error: mac-vendor.txt file not found.")
        return 'Unknown'


def scan_network(ip: str) -> None:
    """
    This function scans the network and sends a message to the Telegram bot when a new device is connected or disconnected.
    :param update: update object for the Telegram bot
    :param context: context object for the Telegram bot
    """
    connected_hosts = {}
    old_hosts = []
    logging.info('Scanning wifi network...')
    while True:
        ans, _ = s.arping(ip, verbose=0)
        hosts = [host[1].src for host in ans]
        logging.info(f'{len(hosts)} devices detected on network..')

        for host in ans:
            mac_address = host[1].src
            mac_vendor = get_mac_vendor(mac_address).strip()
            ip_address = host[1].psrc
            if mac_address not in connected_hosts:
                msg = f"New device connected: {mac_vendor} ({ip_address} - {mac_address})"
                logging.info(msg)
            connected_hosts[mac_address] = (mac_vendor, ip_address)

        for mac_address in old_hosts:
            if mac_address not in hosts:
                mac_vendor, ip_address = connected_hosts[mac_address]
                msg = f"Device disconnected: {mac_vendor} ({ip_address} - {mac_address})"
                logging.info(msg)
                del connected_hosts[mac_address]
        old_hosts = hosts
        time.sleep(5)


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    logging.basicConfig(format="%(levelname)s:%(asctime)s:%(message)s")

    with open('conf.json') as f:
        conf = json.load(f)
        IP_ADDR = conf["NETWORK"]
    
    scan_network(IP_ADDR)