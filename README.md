# Wifi Device Monitor
This is a simple Python based wifi network scanner which allows you to discover devices on a network.

## Features
- Discover devices on a network by sending ARP requests
- Print device ip, mac address and device name (by NIC) to terminal

## Usage
Use git clone to gather the scripts.

Create a conf.json file in the root directory of the projects with the following:

```
{
    "NETWORK": <desired-ip-addr>,
}
```

Install requirements then run the main.py file:

```
sudo python3 main.py
```