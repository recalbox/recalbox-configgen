#!/usr/bin/env python
import xml.etree.ElementTree as ET
import recalboxFiles

esInputs = recalboxFiles.esInputs


class Input:
    def __init__(self, name, type, id, value):
        self.name = name
        self.type = type
        self.id = id
        self.value = value


class Controller:
    def __init__(self, configName, type, guid, player, index="-1", realName="", inputs=None):
        self.type = type
        self.configName = configName
        self.index = index
        self.realName = realName
        self.guid = guid
        self.player = player
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
                                        controller.get("deviceGUID"), None)
        uidname = controller.get("deviceGUID") + controller.get("deviceName")
        controllers[uidname] = controllerInstance
        for input in controller.findall("input"):
            inputInstance = Input(input.get("name"), input.get("type"), input.get("id"), input.get("value"))
            controllerInstance.inputs[input.get("name")] = inputInstance
    return controllers


# Create a controller array with the player id as a key
def loadControllerConfig(p1index, p1guid, p1name, p2index, p2guid, p2name, p3index, p3guid, p3name, p4index, p4guid,
                         p4name):
    playerControllers = dict()
    controllers = loadAllControllersConfig()

    newController = findBestControllerConfig(controllers, '1', p1guid, p1index, p1name)
    if newController:
        playerControllers["1"] = newController
    newController = findBestControllerConfig(controllers, '2', p2guid, p2index, p2name)
    if newController:
        playerControllers["2"] = newController
    newController = findBestControllerConfig(controllers, '3', p3guid, p3index, p3name)
    if newController:
        playerControllers["3"] = newController
    newController = findBestControllerConfig(controllers, '4', p4guid, p4index, p4name)
    if newController:
        playerControllers["4"] = newController
    return playerControllers

def findBestControllerConfig(controllers, x, pxguid, pxindex, pxname):
    # when there will have more joysticks, use hash tables
    for controllerGUID in controllers:
        controller = controllers[controllerGUID]
        if controller.guid == pxguid and controller.configName == pxname:
            return Controller(controller.configName, controller.type, controller.guid, x, pxindex, pxname,
                              controller.inputs)
    for controllerGUID in controllers:
        controller = controllers[controllerGUID]
        if controller.guid == pxguid:
            return Controller(controller.configName, controller.type, controller.guid, x, pxindex, pxname,
                              controller.inputs)
    for controllerGUID in controllers:
        controller = controllers[controllerGUID]
        if controller.configName == pxname:
            return Controller(controller.configName, controller.type, controller.guid, x, pxindex, pxname,
                              controller.inputs)

    return None
