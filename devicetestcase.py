#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
"""
Package for HidaV integration test case generic test classes
"""

import unittest
import datetime
import device
import threading
import logging
import logging.config
import yaml

class DeviceTestCase(unittest.TestCase):
    """ This class is the base class for all HidaV integration tests. It takes
        care of basic device initialization and guarantees that there's only
        one instance of :py:class:`Device` active at any time. 
        
        Classes inheriting from :py:class:`DeviceTestCase` will automatically
        win a logger object and a device object upon initialization. These two
        instance objects are provided by :py:class:`DeviceTestCase` :

        .. code-block:: python
                
                import devicetestcase

                class MyTest(devicetestcase.DeviceTestCase):

                      ....

                    def setUp(self):
                        self.dev.wait_for_network()
                        self.logger.debug("Device IP is: %s." % self.dev.host)

                      ....
    """

    __dev = None
    __devsem = threading.Lock()
    
    
    @classmethod
    def get_device(cls, devicetype, nand_boot=True):
        """ Get the :py:class:`Device` singleton instance. A new instance will
            be created if none is available yet. 
        """
        if not cls.__dev:
            cls.__devsem.acquire()
            if not cls.__dev:
                cls.__create_device(devicetype, nand_boot)
            cls.__devsem.release()
        return cls.__dev


    @classmethod        
    def __create_device(cls, devicetype, nand_boot=True):
        """ boot HidaV-device to NAND """
        filename = "run-%s.log" % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        dictionary = yaml.load(open('logging.conf', 'r'))
        dictionary['handlers']['file']['filename'] = filename
        logging.config.dictConfig(dictionary)
        cls.__dev = device.Device( devtype = devicetype )
        if nand_boot:
            logging.getLogger(__name__).debug("Boot to NAND ...")
            cls.__dev.reboot(to_nand=True)


    def __init__(self, devicetype, *args, **kwargs): # pragma: no cover
        """ The class will create and add to self logger and dev objects upon
            instantiation.
        """
        super(DeviceTestCase, self).__init__(*args, **kwargs)
        self.dev = DeviceTestCase.get_device(devicetype)
        self.logger = logging.getLogger(__name__)
        
