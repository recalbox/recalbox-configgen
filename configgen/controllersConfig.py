#!/usr/bin/env python
import xml.etree.ElementTree as ET
import recalboxFiles

esInputs = recalboxFiles.esInputs


class Input:
    def __init__(self, name, type, id, value, code):
        self.name = name
        self.type = type
        self.id = id
        self.value = value
        self.code = code


class Controller:
    def __init__(self, configName, type, guid, player, index="-1", realName="", inputs=None, dev=None, nbaxes=None):
        self.type = type
        self.configName = configName
        self.index = index
        self.realName = realName
        self.guid = guid
        self.player = player
        self.dev = dev
        self.nbaxes = nbaxes
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
                                        controller.get("deviceGUID"), None, None)
        uidname = controller.get("deviceGUID") + controller.get("deviceName")
        controllers[uidname] = controllerInstance
        for input in controller.findall("input"):
            inputInstance = Input(input.get("name"), input.get("type"), input.get("id"), input.get("value"), input.get("code"))
            controllerInstance.inputs[input.get("name")] = inputInstance
    return controllers


# Load all controllers from the es_input.cfg
def loadAllControllersByNameConfig():
    controllers = dict()
    tree = ET.parse(esInputs)
    root = tree.getroot()
    for controller in root.findall(".//inputConfig"):
        controllerInstance = Controller(controller.get("deviceName"), controller.get("type"),
                                        controller.get("deviceGUID"), None, None)
        deviceName = controller.get("deviceName")
        controllers[deviceName] = controllerInstance
        for input in controller.findall("input"):
            inputInstance = Input(input.get("name"), input.get("type"), input.get("id"), input.get("value"), input.get("code"))
            controllerInstance.inputs[input.get("name")] = inputInstance
    return controllers


# Create a controller array with the player id as a key
def loadControllerConfig(p1index, p1guid, p1name, p1dev, p1nbaxes, p2index, p2guid, p2name, p2dev, p2nbaxes, p3index, p3guid, p3name, p3dev, p3nbaxes,
                         p4index, p4guid, p4name, p4dev, p4nbaxes, p5index, p5guid, p5name, p5dev, p5nbaxes):
    playerControllers = dict()
    controllers = loadAllControllersConfig()

    newController = findBestControllerConfig(controllers, '1', p1guid, p1index, p1name, p1dev, p1nbaxes)
    if newController:
        playerControllers["1"] = newController
    newController = findBestControllerConfig(controllers, '2', p2guid, p2index, p2name, p2dev, p2nbaxes)
    if newController:
        playerControllers["2"] = newController
    newController = findBestControllerConfig(controllers, '3', p3guid, p3index, p3name, p3dev, p3nbaxes)
    if newController:
        playerControllers["3"] = newController
    newController = findBestControllerConfig(controllers, '4', p4guid, p4index, p4name, p4dev, p4nbaxes)
    if newController:
        playerControllers["4"] = newController
    newController = findBestControllerConfig(controllers, '5', p5guid, p5index, p5name, p5dev, p5nbaxes)
    if newController:
        playerControllers["5"] = newController
    return playerControllers

def loadControllerConfig2(**kwargs):
    playerControllers = dict()
    controllers = loadAllControllersConfig()
    
    for i in range(1, 6):
        num = str(i)
        pguid = kwargs.get('p{}guid'.format(num), None)
        pindex = kwargs.get('p{}index'.format(num), None)
        pname = kwargs.get('p{}name'.format(num), None)
        pdev = kwargs.get('p{}dev'.format(num), None)
        pnbaxes = kwargs.get('p{}nbaxes'.format(num), None)
        if pdev is None:
            pdev = kwargs.get('p{}devicepath'.format(num), None)
        newController = findBestControllerConfig(controllers, num, pguid, pindex, pname, pdev, pnbaxes)
        if newController:
            playerControllers[num] = newController
    return playerControllers

def findBestControllerConfig(controllers, x, pxguid, pxindex, pxname, pxdev, pxnbaxes):
    # when there will have more joysticks, use hash tables
    for controllerGUID in controllers:
        controller = controllers[controllerGUID]
        if controller.guid == pxguid and controller.configName == pxname:
            return Controller(controller.configName, controller.type, controller.guid, x, pxindex, pxname,
                              controller.inputs, pxdev, pxnbaxes)
    for controllerGUID in controllers:
        controller = controllers[controllerGUID]
        if controller.guid == pxguid:
            return Controller(controller.configName, controller.type, controller.guid, x, pxindex, pxname,
                              controller.inputs, pxdev, pxnbaxes)
    for controllerGUID in controllers:
        controller = controllers[controllerGUID]
        if controller.configName == pxname:
            return Controller(controller.configName, controller.type, controller.guid, x, pxindex, pxname,
                              controller.inputs, pxdev, pxnbaxes)
    return None
