"""
Polyglot v3 node server
Copyright (C) 2021 Steven Bailey
MIT License
"""
import udi_interface
import sys
import time
import urllib3
import asyncio
from bascontrolns import Device, Platform

LOGGER = udi_interface.LOGGER


class IrrigationNode(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name, ip, ip1, ip2, ip3, ip4, ip5, bc):
        super(IrrigationNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (address, name)
        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)
        self.bc = bc
        LOGGER.info(address)
        # IP Address Sorter
        if address == 'zone_{}'.format(0):
            self.ipaddress = ip
        elif address == 'zone_{}'.format(1):
            self.ipaddress = ip1
        elif address == 'zone_{}'.format(2):
            self.ipaddress = ip2
        elif address == 'zone_{}'.format(3):
            self.ipaddress = ip3
        elif address == 'zone_{}'.format(4):
            self.ipaddress = ip4
        elif address == 'zone_{}'.format(5):
            self.ipaddress = ip5
        else:
            pass

    def start(self):
        if self.ipaddress is not None:
            self.bc = Device(self.ipaddress)
        ### Do we have a BASpi or an Edge Device ###
        if self.bc.ePlatform == Platform.BASC_PI or self.bc.ePlatform == Platform.BASC_PO:  # if a BASpi-6u6r Device is found
            LOGGER.info('connected to BASpi-6U6R')
        elif self.bc.ePlatform == Platform.BASC_ED:  # if a BASpi-Edge Device is found
            LOGGER.info('connected to BASpi-Edge')
            self.setDriver('ST', 1)
        elif self.bc.ePlatform == Platform.BASC_NONE:  # if there is NO Device found
            LOGGER.info('Unable to connect to Device')
            LOGGER.info('ipaddress')
        else:
            pass

        # How many nodes or points does the device have
        LOGGER.info('\t' + str(self.bc.uiQty) +
                    ' Universal inputs in this Device')
        LOGGER.info('\t' + str(self.bc.boQty) +
                    ' Binary outputs in this Device')
        LOGGER.info('\t' + str(self.bc.vtQty) +
                    ' Virtual points In This Device')

        # Input/Output Status
        LOGGER.info('Inputs')
        for i in range(1, 7):
            LOGGER.info(str(self.bc.universalInput(i)))
        LOGGER.info('Outputs')
        for i in range(1, 7):
            LOGGER.info(str(self.bc.binaryOutput(i)))

        ### Universal Inputs ###
        self.setInputDriver('GV0', 1)
        self.setInputDriver('GV1', 2)
        self.setInputDriver('GV2', 3)
        self.setInputDriver('GV3', 4)
        self.setInputDriver('GV4', 5)

        # Input 6 Conversion
        input_six = self.bc.universalInput(6)
        if input_six is not None:
            sumss_count = int(float(input_six))
            self.setDriver('GV5', int(sumss_count))
        if input_six is not None:
            sumss_count = int(float(self.bc.universalInput(6)))
        else:
            return

    ### Universal Input Conversion ###
    def setInputDriver(self, driver, input):
        input_val = self.bc.universalInput(input)
        count = 0
        if input_val is not None:
            count = int(float(input_val))
            self.setDriver(driver, count)
        else:
            return

        # Binary/Digital Outputs
        self.setOutputDriver('GV6', 1)
        self.setOutputDriver('GV7', 2)
        self.setOutputDriver('GV8', 3)
        self.setOutputDriver('GV9', 4)
        self.setOutputDriver('GV10', 5)
        self.setOutputDriver('GV11', 6)

    ### Binary Output Conversion ###
    def setOutputDriver(self, driver, input):
        output_val = self.bc.binaryOutput(input)
        count = 0
        if output_val is not None:
            count = (output_val)
            self.setDriver(driver, count)
        else:
            return
        pass

        # Dict for 6 output ON OFF function
        self.mapping = {
            'BON1': {'output': 'GV6', 'index': (1)},
            'BOF1': {'output': 'GV6', 'index': (1)},
            'BON2': {'output': 'GV7', 'index': (2)},
            'BOF2': {'output': 'GV7', 'index': (2)},
            'BON3': {'output': 'GV8', 'index': (3)},
            'BOF3': {'output': 'GV8', 'index': (3)},
            'BON4': {'output': 'GV9', 'index': (4)},
            'BOF4': {'output': 'GV9', 'index': (4)},
            'BON5': {'output': 'GV10', 'index': (5)},
            'BOF5': {'output': 'GV10', 'index': (5)},
            'BON6': {'output': 'GV11', 'index': (6)},
            'BOF6': {'output': 'GV11', 'index': (6)},
        }

    # ON OFF Control Commands
    # All Zones
    def cmdOn(self, command):
        output = self.mapping[command['cmd']]['output']
        index = self.mapping[command['cmd']]['index']
        if self.bc.binaryOutput(index) != 1:
            self.bc.binaryOutput(index, 1)
            self.setDriver(output, 1)
            LOGGER.info('Zone {} On'.format(index))

    def cmdOff(self, command):
        output = self.mapping[command['cmd']]['output']
        index = self.mapping[command['cmd']]['index']
        if self.bc.binaryOutput(index) != 0:
            self.bc.binaryOutput(index, 0)
            self.setDriver(output, 0)
            LOGGER.info('Zone {} Off'.format(index))

    def poll(self, polltype):
        if 'longPoll' in polltype:
            LOGGER.debug('longPoll (node)')
        else:
            self.start()
            LOGGER.debug('shortPoll (node)')

    def query(self, command=None):
        self.start()
        LOGGER.info(self.bc)

    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'GV0', 'value': 1, 'uom': 17},  # OSA Temp
        {'driver': 'GV1', 'value': 1, 'uom': 56},  # Spare
        {'driver': 'GV2', 'value': 1, 'uom': 56},  # Spare
        {'driver': 'GV3', 'value': 1, 'uom': 56},  # Spare
        {'driver': 'GV4', 'value': 1, 'uom': 56},  # Spare
        {'driver': 'GV5', 'value': 1, 'uom': 25},  # Soil Moisture
        {'driver': 'GV6', 'value': 0, 'uom': 80},  # Zone 1 Output
        {'driver': 'GV7', 'value': 0, 'uom': 80},  # Zone 2 Output
        {'driver': 'GV8', 'value': 0, 'uom': 80},  # Zone 3 Output
        {'driver': 'GV9', 'value': 0, 'uom': 80},  # Zone 4 Output
        {'driver': 'GV10', 'value': 0, 'uom': 80},  # Zone 5 Output
        {'driver': 'GV11', 'value': 0, 'uom': 80},  # Zone 6 Output
    ]

    id = 'zone'

    commands = {
        'BON1': cmdOn,
        'BOF1': cmdOff,
        'BON2': cmdOn,
        'BOF2': cmdOff,
        'BON3': cmdOn,
        'BOF3': cmdOff,
        'BON4': cmdOn,
        'BOF4': cmdOff,
        'BON5': cmdOn,
        'BOF5': cmdOff,
        'BON6': cmdOn,
        'BOF6': cmdOff,
        'PING': query
    }
