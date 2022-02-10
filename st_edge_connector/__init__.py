"""
ST Edge Connector
Copyright (c) 2018 fison67 <fison67@nate.com>
Licensed under MIT
"""
import requests
import logging
import json
import base64
import select

import struct
import socket
import threading
import getmac
import time

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
# import asyncio
# import asyncudp

import voluptuous as vol

# from .aes import AESCipher

import homeassistant.loader as loader
from homeassistant.const import (STATE_UNKNOWN, EVENT_STATE_CHANGED)
import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from homeassistant.helpers.device_registry import (
    CONNECTION_UPNP,
    async_get as async_get_device_registry,
)

from homeassistant.helpers import discovery

_LOGGER = logging.getLogger(__name__)

NAME                = 'ST Edge Cordinator'
MANUFACTURER        = "fison67"
MODEL               = 'Edge Driver'
CONNECTIONS_VALUE   = "fison67"
IDENTIFIERS_VALUE   = "fison67"
DOMAIN              = "st_edge_connector"
VERSION             = "1.0.0"
CONF_HUB_ADDR       = 'hub_addr'
CONF_HA_ADDR        = 'ha_addr'
CONF_HA_PORT        = 'ha_port'
CONF_BUFFER_SIZE    = 10240

CONF_MCAST_GRP      = '239.255.255.250'
CONF_MCAST_PORT     = 30000


class EdgeDriver:

    def __init__(self, hass, config_entry):
        self.hass = hass
        self.config_entry = config_entry
        self.deviceDataMap = {}
        self.hub_addr = self.config_entry.data[CONF_HUB_ADDR]
        self.ha_addr = self.config_entry.data[CONF_HA_ADDR]
        self.ha_port = self.config_entry.data[CONF_HA_PORT]

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP,socket.inet_aton(CONF_MCAST_GRP) + socket.inet_aton(self.ha_addr))
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 128)
        self.sock.bind((CONF_MCAST_GRP, CONF_MCAST_PORT))

        self.entity_registry = self.hass.helpers.entity_registry.async_get(self.hass)

        t = threading.Thread(target=self.initUDP, args=())
        t.start()

        t2 = threading.Thread(target=self.initTCP, args=())
        t2.start()

    def getDevices(self, type):
        list = self.hass.states.async_all()
        result = []
        for state in list:
            if state.entity_id.startswith('st_edge_connector.' + type):
                result.append({
                    "id": state.entity_id,
                    "name": state.name
                })
        return result

    def processPairing(self, data, addr):
        try:
            stateList = self.hass.states.async_all()

            content = self.entity_registry._data_to_save()
            title = 'st_edge_connector.' + data
            list = []
            for entity in content["entities"]:
                entity_id = entity["entity_id"]
                if entity_id.startswith(title):
                    origianl_entity_id = data + "." + entity_id[(len(title)+1):len(entity_id)]
                    targetState = {}
                    for state in stateList:
                        if state.entity_id == origianl_entity_id:
                            targetState = state
                            break
                    list.append({"id":origianl_entity_id, "attributes": targetState.as_dict()["attributes"]})

            content = json.dumps({"port":self.tcpPort, "data":list})
            self.sock.sendto(content.encode('UTF-8'), addr)
        except Exception as e:
            logging.error("error: ")
            logging.error(e)

    def procesProtocol(self, data, addr):
        try:
            if isinstance(data, bytes):
                data = data.decode("utf-8")

            jsonObj = json.loads(data)
            if 'cmd' in jsonObj:
                if jsonObj['cmd'] == 'search':
                    self.processPairing(jsonObj['data'], addr)
        except Exception as e:
            logging.error("error: ")
            logging.error(e)

    def initTCP(self):
        self.handler = Handler(self.hass, self.entity_registry, self.hub_addr)
        httpd = HTTPServer(('0.0.0.0', self.ha_port), self.handler)
        self.tcpPort = httpd.server_address[1]
        logging.info(f'Server running on port:{self.tcpPort}')
        httpd.serve_forever()

    def initUDP(self):
        while True:
          data, addr = self.sock.recvfrom(CONF_BUFFER_SIZE)
          # logging.info("Receive UDP")
          self.procesProtocol(data, addr)


    def current_milli_time(self):
        return round(time.time() * 1000)

    def eventCallback(my, event):
        newState = event.data['new_state']
        id  = newState.entity_id
        target = my.entity_registry.async_get(DOMAIN + "." + id.replace(".", "_"))
        if target is not None:
            try:
                deviceMap = my.handler.getDeviceDataMap()
                if id in deviceMap:
                    addr = "http://" + deviceMap[id] + "/push-state"
                    uuid = "http://" + my.ha_addr  + ":" + str(my.ha_port) + "/" + id
                    data = json.dumps({"uuid":uuid, "time": my.current_milli_time(), "data":newState.state, "attributes": newState.as_dict().get('attributes')}).encode('UTF-8')
                    # logging.info(data)
                    res = requests.post(addr, data=data)
                else :
                    logging.warn("Non exist edge address: " + id)
            except Exception as e:
                logging.error("EventCallback Error: ")
                logging.error(e)


def base_config_schema(config: dict = {}) -> dict:
    """Return a shcema configuration dict for HA-Connector."""
    if not config:
        config = {
            CONF_HUB_ADDR: "",
            CONF_HA_ADDR: "",
            CONF_HA_PORT: 20000
        }
    return {
        vol.Required(CONF_HUB_ADDR): str,
        vol.Required(CONF_HA_ADDR): str,
        vol.Required(CONF_HA_PORT): int,
    }


def config_combined() -> dict:
    """Combine the configuration options."""
    base = base_config_schema()

    return base

CONFIG_SCHEMA = vol.Schema({DOMAIN: config_combined()}, extra=vol.ALLOW_EXTRA)

async def async_setup_entry(hass, config_entry):
    """Set up this integration using UI."""
    conf = hass.data.get(DOMAIN)

    if config_entry.source == config_entries.SOURCE_IMPORT:
        if conf is None:
            # user removed config from configuration.yaml, abort setup
            hass.async_create_task(hass.config_entries.async_remove(entry.entry_id))
            return False

        if conf != config_entry.data:
            # user changed config from configuration.yaml, use conf to setup
            hass.config_entries.async_update_entry(config_entry, data=conf)

    if conf is None:
        conf = config_entry.data

    device_registry = await hass.helpers.device_registry.async_get_registry()
    device = device_registry.async_get_or_create(
        config_entry_id=config_entry.entry_id,
        connections={(CONNECTION_UPNP, CONNECTIONS_VALUE)},
        identifiers={(DOMAIN, IDENTIFIERS_VALUE)},
        name=NAME,
        manufacturer=MANUFACTURER,
        model=MODEL,
        sw_version=VERSION
    )

    driver = EdgeDriver(hass, config_entry)

    def event_listener(event):
         driver.eventCallback(event)

    hass.data[DOMAIN] = driver
    hass.bus.async_listen(EVENT_STATE_CHANGED, event_listener)
    return True


class Handler(BaseHTTPRequestHandler):

    def __init__(self, hass, entity_registry, hub_addr):
        self.hass = hass
        self.entity_registry = entity_registry
        self.hub_addr = hub_addr
        self.deviceDataMap = {}

    def __call__(self, *args, **kwargs):
        """ Handle a request """
        super().__init__(*args, **kwargs)

    def getState(self, id):
        list = self.hass.states.async_all()
        result = []
        for state in list:
            if state.entity_id == id:
                return state
        return {}

    def getDeviceDataMap(self):
        return self.deviceDataMap

    def _setOK(self, content):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(content.encode('UTF-8'))

    def _setError(self):
        self.send_response(400)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()

    def _processGet(self, id, cmd, query):
        if cmd == 'refresh':
            # content = self.entity_registry._data_to_save()
            content = json.dumps({"state":self.getState(id).as_dict()})
            self._setOK(content)
        else:
            self._setError("")

    def _processPost(self, id, cmd, query):
        d = dict(x.split("=") for x in query.split("&"))
        if cmd == 'ping':
            self.deviceDataMap[id] = d["address"] + ":" + d["port"]
            self._setOK(json.dumps({"result":True}))
        elif cmd == 'control':
            data = {"entity_id": id}
            if "s_command" in d:
                data[d["s_command"]] = d["s_value"]
                if d["s_value"].isnumeric() == True:
                    data[d["s_command"]] = int(d["s_value"])
            # logging.info("#### Command ####")
            # logging.info(data)
            self.hass.services.call(
                d["type"],
                d["command"],
                data,
                blocking=False,
            )
            self._setOK(json.dumps({"result":True}))
        else:
            self._setError()

    def getQueryData(self):
        path = self.path.split("/")
        if len(path) < 2:
            return False, '', ''
        else:
            id = path[1]
            cmd = path[2]
            query = ""
            if "?" in cmd:
                tmp = cmd.split("?")
                cmd = tmp[0]
                query = tmp[1]
            return True, id, cmd, query

    def do_POST(self):
        if self.client_address[0] == self.hub_addr:
            result, id, cmd, query = self.getQueryData()
            if result == True:
                self._processPost(id, cmd, query)
            else:
                self._setError()
        else:
            logging.warn("Request from " + self.client_address[0])
            self._setError()

    def do_GET(self):
        if self.client_address[0] == self.hub_addr:
            result, id, cmd, query = self.getQueryData()
            if result == True:
                self._processGet(id, cmd, query)
            else:
                self._setError()
        else:
            logging.warn("Request from " + self.client_address[0])
            self._setError()
