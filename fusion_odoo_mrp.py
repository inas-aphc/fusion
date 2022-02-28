# Author-sulaimanhabsi
# Description-This add-in allows the integration with odoo mrp and inventory modules
import os
import adsk.core
import adsk.fusion
import adsk.cam
import traceback
import threading
# from adsk import *


from .pppHelper import *
from .odooHelper import *

import json
_uid = None
_app: adsk.core.Application = adsk.core.Application.get()
_ui: adsk.core.UserInterface = _app.userInterface
# _product: adsk.core.Product = _app.activeProduct
PALETTE_NAME = "odoo_mrp"
# Author-Patrick Rainsberry
# Description-A sample Fusion 360 Addin to demonstrate various UI elements.


handlers = []
stopFlag = None


def run(context):

    try:
        odooMrpCreateCommad()
        createPalette()
        adsk.autoTerminate(False)
    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):

    try:

        cmdDefs = _ui.commandDefinitions
        odooMrpCmd = cmdDefs.itemById('OdooMRP')
        odooMrpCmd.deleteMe()

        designWS = _ui.workspaces.itemById('FusionSolidEnvironment')
        # Get the SOLID tab.
        toolsTab = designWS.toolbarTabs.itemById('ToolsTab')
        # Get the CREATE panel.
        addinsPanel = toolsTab.toolbarPanels.itemById(
            'SolidScriptsAddinsPanel')
        odooPanelBtn = addinsPanel.controls.itemById('OdooMRP')
        odooPanelBtn.deleteMe()

        palette = _ui.palettes.itemById(PALETTE_NAME)
        if palette:
            palette.deleteMe()
        # ui.messageBox('Stop addin')

    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def odooMrpCreateCommad():
    # app = adsk.core.Application.get()
    # ui = app.userInterface
    cmdDefs = _ui.commandDefinitions
    odooMrpCmd = None
    try:
        odooMrpCmd = cmdDefs.addButtonDefinition(
            'OdooMRP', 'Odoo MRP', 'Odoo MRP')
    except:
        odooMrpCmd = cmdDefs.itemById('OdooMRP')

    btnCreateHdlr = odooButtonCreatedHandler()
    odooMrpCmd.commandCreated.add(btnCreateHdlr)
    handlers.append(btnCreateHdlr)
    # Get the DESIGN workspace.
    designWS = _ui.workspaces.itemById('FusionSolidEnvironment')
    # Get the SOLID tab.
    toolsTab = designWS.toolbarTabs.itemById('ToolsTab')

    # Get the CREATE panel.
    addinsPanel = toolsTab.toolbarPanels.itemById(
        'SolidScriptsAddinsPanel')
    addinsPanel.controls.addCommand(odooMrpCmd)

    # ui.messageBox('Odoo MRP Add-in Started')


def createPalette():
    # app = adsk.core.Application.get()
    # ui = app.userInterface
    palette = _ui.palettes.add(
        PALETTE_NAME, 'Odoo MRP', 'login.html', False, True, False, 400, 300, True)
    _odooFromHTMLHandler = odooIncomingFromHtml()
    palette.incomingFromHTML.add(_odooFromHTMLHandler)
    handlers.append(_odooFromHTMLHandler)


def showPalettes():
    # app = adsk.core.Application.get()
    # ui = app.userInterface
    palette = _ui.palettes.itemById(PALETTE_NAME)
    palette.setPosition(0, 0)
    if loginFromSession():
        rootObj = json.loads('{"cmd":"AUTOLOGIN"}')
        rootDoc =json.dumps(rootObj)
        palette.sendInfoToHTML('send', rootDoc)
    palette.isVisible = True


def renameFile(name):
    doc = _app.activeDocument
    # print(doc.name)
    # doc.close()
    activeProduct = _app.activeProduct
    doc.dataFile.name = name
    rootComponent :adsk.core.Component = activeProduct.rootComponent
    rootComponent.partNumber = name
    
    doc.save(
        "Odoo MRP Addin: Generate Part Number and rename the file to the par number")

def getname():
    doc = _app.activeDocument
    # print(doc.name)
    # doc.close()
    activeProduct = _app.activeProduct
   
    rootComponent :adsk.core.Component = activeProduct.rootComponent
    name = rootComponent.partNumber 
    return name

    
def saveSession(server, user, pwd):
    data = {'server': server, 'username': user, 'password': pwd}
    # rootDoc = json.dumps(data)
    activeProduct = _app.activeProduct
    print(activeProduct.attributes.groupNames)
    activeProduct.attributes.add('odoo_mrp', 'server', server)
    activeProduct.attributes.add('odoo_mrp', 'username', user)
    activeProduct.attributes.add('odoo_mrp', 'password', pwd)
    # print(os.getcwd())
    # file.write("hellow world!!")
    # file.close()

def deleteSession():
    activeProduct = _app.activeProduct
    activeProduct.attributes.itemByName('odoo_mrp', 'server').deleteMe()
    activeProduct.attributes.itemByName('odoo_mrp', 'username').deleteMe()
    activeProduct.attributes.itemByName('odoo_mrp', 'password').deleteMe()

def loginFromSession():
    server = None
    username = None
    password = None
    try:
        activeProduct = _app.activeProduct
        server = activeProduct.attributes.itemByName('odoo_mrp', 'server')
        username = activeProduct.attributes.itemByName('odoo_mrp', 'username')
        password = activeProduct.attributes.itemByName('odoo_mrp', 'password')
    except NameError:
        pass
    if server and username and password :
        setOdooServer(server.value)
        _uid = authenticateOdooServer(username.value,password.value)
        if _uid :
            return True
        else :
            return False

def setComponentProperties(partNumber):
    doc = _app.activeDocument
    design = adsk.core.Application.get().activeProduct
    rootComponent = design.rootComponent
    rootComponent.partNumber = partNumber
    # attribs = design.rootComponent.attributes.groupNames
    pppAttribures = rootComponent.attributes
    # pppAttribures = rootComponent.attributes.itemsByGroup('ProppertiesPP')
    decodePppAttributes(pppAttribures)

def isPartNumberAssigned():
    activeProduct = _app.activeProduct
    print(type(activeProduct.productType))
    if activeProduct.productType =='DesignProductType':
        rootComponent :adsk.core.Component = activeProduct.rootComponent
        partNumber = rootComponent.partNumber
        if isProductExists(partNumber):
            return True
        else:
            return False
    # rootComponent = 
    
class odooButtonCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)
        cmd = eventArgs.command

        # Connect to the execute event.
        onExecute = odooButtonExecuteHandler()
        cmd.execute.add(onExecute)
        handlers.append(onExecute)


# Event handler for the execute event.


class odooButtonExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        eventArgs = adsk.core.CommandEventArgs.cast(args)

        # Code to react to the event.
        # app = adsk.core.Application.get()
        # ui = app.userInterface
        # palettes = ui.palettes
        # print(palettes)
        # ui.messageBox('In command execute event handler.')
        showPalettes()

        # adsk.terminate()
        # setComponentProperties("TST00002")


class sendToHtmlThread(threading.Thread):
    htmlData = None

    def __init__(self, data):
        threading.Thread.__init__(self)
        self.htmlData = data

    def run(self):
        palette = _ui.palettes.itemById(PALETTE_NAME)
        print(self.htmlData)
        palette.sendInfoToHTML('send', self.htmlData)
        


class odooIncomingFromHtml(adsk.core.HTMLEventHandler):
    def __init__(self) -> None:
        super().__init__()

    def notify(self, args):
        # app = adsk.core.Application.get()
        # ui = app.userInterface
        try:
            htmlArgs = adsk.core.HTMLEventArgs.cast(args)
            data = json.loads(htmlArgs.data)

            # print(palette.name)
            # print(data)
            if 'cmd' in data and data['cmd'] == 'NPN':
                partNumber = None
                if not isPartNumberAssigned():
                    partNumber = CreateProduct(
                    'defaultFusionProductName', data)
                    renameFile(partNumber)
                else:
                    partNumber = 'exists'
                rootObj = json.loads('{"cmd":"NPN"}')
                rootObj['data'] = partNumber
                rootDoc =json.dumps(rootObj)
                myThread = sendToHtmlThread(rootDoc)
                myThread.start()
            elif 'cmd' in data and data['cmd'] == 'RN':
               # partNumber = None  
                filename=getname()
                partNumber=CreateProduct1(data, filename)
                renameFile(data['name'])
                rootObj = json.loads('{"cmd":"RN"}')
                rootObj['data'] = data['name']
                rootDoc =json.dumps(rootObj)
                myThread = sendToHtmlThread(rootDoc)
                myThread.start()
            elif 'cmd' in data and data['cmd'] == 'LOGIN':
                # print(data)
                setOdooServer(data['server'])
                rootObj = json.loads('{"cmd":"LOGIN"}')
                _uid = authenticateOdooServer(
                    data['uid'], data['pwd'])
                if _uid:
                    rootObj['uid'] = True
                    rootDoc = json.dumps(rootObj)
                    saveSession(data['server'], data['uid'], data['pwd'])
                    # print(rootDoc)
                    myThread = sendToHtmlThread(rootDoc)
                    myThread.start()

                else:
                    rootObj['uid'] = False
                    rootDoc = json.dumps(rootObj)
                    # print(rootDoc)
                    myThread = sendToHtmlThread(rootDoc)
                    myThread.start()

            elif 'cmd' in data and data['cmd'] == 'LOAD_SUBCAT':
                
                # _uid = authenticateOdooServer(user, pwd)
                
                categories = getSubCategoris()
               
                rootObj = json.loads('{"cmd":"CATS"}')
                rootObj['data'] = categories
                rootDoc = json.dumps(rootObj)
                # print(rootObj)
                myThread = sendToHtmlThread(rootDoc)
                myThread.start()
            elif 'cmd' in data and data['cmd'] == 'LOAD_SUBsubCAT':
                
                # _uid = authenticateOdooServer(user, pwd)
                
                categories = getSubsubCategoris()
               
                rootObj = json.loads('{"cmd":"SUBCATS"}')
                rootObj['data'] = categories
                rootDoc = json.dumps(rootObj)
                # print(rootObj)
                myThread = sendToHtmlThread(rootDoc)
                myThread.start()
            elif 'cmd' in data and data['cmd'] == 'LOAD_INFO':
                
                # _uid = authenticateOdooServer(user, pwd)
                
                info = getInfo(getname())
               
                rootObj = json.loads('{"cmd":"INFO"}')
                rootObj['data'] = info
                rootDoc = json.dumps(rootObj)
                # print(rootObj)
                myThread = sendToHtmlThread(rootDoc)
                myThread.start()
            elif 'cmd' in data and data['cmd'] == 'LOAD_RCT':
                
                # _uid = authenticateOdooServer(user, pwd)
                
                info = creatWref(getname())
               
                rootObj = json.loads('{"cmd":"RCT"}')
                rootObj['data'] = info
                rootDoc = json.dumps(rootObj)
                # print(rootObj)
                myThread = sendToHtmlThread(rootDoc)
                myThread.start()
            elif 'cmd' in data and data['cmd'] == 'LOGOUT':
                deleteSession()
                rootObj = json.loads('{"cmd":"LOGOUT"}')
                rootDoc = json.dumps(rootObj)
                myThread = sendToHtmlThread(rootDoc)
                myThread.start()

        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def run(context):
    try:
        odooMrpCreateCommad()
        createPalette()
        adsk.autoTerminate(False)
    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):

    try:

        cmdDefs = _ui.commandDefinitions
        odooMrpCmd = cmdDefs.itemById('OdooMRP')
        odooMrpCmd.deleteMe()

        designWS = _ui.workspaces.itemById('FusionSolidEnvironment')
        # Get the SOLID tab.
        toolsTab = designWS.toolbarTabs.itemById('ToolsTab')
        # Get the CREATE panel.
        addinsPanel = toolsTab.toolbarPanels.itemById(
            'SolidScriptsAddinsPanel')
        odooPanelBtn = addinsPanel.controls.itemById('OdooMRP')
        odooPanelBtn.deleteMe()

        palette = _ui.palettes.itemById(PALETTE_NAME)
        if palette:
            palette.deleteMe()
        # ui.messageBox('Stop addin')

    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

