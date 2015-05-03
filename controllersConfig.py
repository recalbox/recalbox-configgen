#!/usr/bin/env python
import xml.etree.ElementTree as ET

esInputs = "/root/.emulationstation/es_input.cfg"


class Input:
    def __init__(self, name, type, id, value):
        self.name = name
        self.type = type
        self.id = id
        self.value = value


class Controller:
    def __init__(self, name, type, guid, index="-1", realName="", inputs=None):
        self.type = type
        self.name = name
        self.index = index
        self.realName = realName
        self.guid = guid
        if inputs == None:
            self.inputs = dict()
        else:
            self.inputs = inputs


# Load all controllers from the es_input.cfg
def loadAllControllersConfig():
    controllers = dict()
    tree = ET.parse(esInputs)
    root = tree.getroot()
    for controller in root.findall(".//inputConfig"):
        controllerInstance = Controller(controller.get("deviceName"), controller.get("type"),
                                        controller.get("deviceGUID"))
        uid = controller.get("deviceGUID")
        controllers[uid] = controllerInstance
        for input in controller.findall("input"):
            inputInstance = Input(input.get("name"), input.get("type"), input.get("id"), input.get("value"))
            controllerInstance.inputs[input.get("name")] = inputInstance
    return controllers


# Create a controller array with the player id as a key
def loadControllerConfig(p1index, p1guid, p1name, p2index, p2guid, p2name, p3index, p3guid, p3name, p4index, p4guid,
                         p4name):
    playerControllers = dict()
    controllers = loadAllControllersConfig()
    for controllerGUID in controllers:
        controller = controllers[controllerGUID]
        if controller.guid == p1guid:
            newController = Controller(controller.name, controller.type, controller.guid, p1index, p1name,
                                       controller.inputs)
            playerControllers["1"] = newController
        if controller.guid == p2guid:
            newController = Controller(controller.name, controller.type, controller.guid, p2index, p2name,
                                       controller.inputs)
            playerControllers["2"] = newController
        if controller.guid == p3guid:
            newController = Controller(controller.name, controller.type, controller.guid, p3index, p3name,
                                       controller.inputs)
            playerControllers["3"] = newController
        if controller.guid == p4guid:
            newController = Controller(controller.name, controller.type, controller.guid, p4index, p4name,
                                       controller.inputs)
            playerControllers["4"] = newController
    return playerControllers
