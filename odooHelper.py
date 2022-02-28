import re
from .odooclient import client
#import odooclient.client as client
_url = 'odoodev.sulaimanhabsi.com'
db = 'aphcarios'
user = 'inas@aphcarios.com'
pwd = '99579023'



_odoo: client.OdooClient = None


def setOdooServer(server):
    global _url
    _url = server


def authenticateOdooServer(username, password):
    global _odoo
    _odoo = client.OdooClient(host=_url,
                              dbname=db, protocol='xmlrpcs', port=443)

    if _odoo:
        print(_odoo.ServerInfo())
        try:
            uid = _odoo.Authenticate(username, password)
            return uid
        except:
            return False

    else:
        return False


def CreateProduct(name, data): #create new product
    global _odoo
    product = _odoo.Create('product.template', {'name':data['name'], 'categ_id': int(data['catId'])})
    print(product)
    product = _odoo.Read('product.template', product, ['default_code','id'])
    
    partNumber = product[0]['default_code']
    product = _odoo.Write('product.template', product[0]['id'], {
        'name': data['name'],'discription': data['disc'], 'default_code':partNumber})
    print(product)   
    return data['name']

  
# Event handler for the commandCreated event.

def CreateProduct1(data , filename):  #renaming
    global _odoo
    product = _odoo.Search('product.template',[('name','=',filename)])
    if product:
        product = _odoo.Read('product.template', product, ['default_code','id'])
        print(product)
        partNumber = product[0]['default_code']
        product = _odoo.Write('product.template', product[0]['id'], {
                'name': data['name'], 'discription': data['disc'], 'default_code':partNumber})
        return data['name']
    else:
        return CreateProduct('defaultFusionProductName',data)
# Event handler for the commandCreated event.

def isProductExists(partNumber):
    products = _odoo.Search('product.template',[('name','=',partNumber)],{})
    if len(products)> 0:
        return True
    else:
        return False

def getSubCategoris():
    global _odoo

    subCategories = _odoo.SearchRead(
        'product.category', [('x_is_in_fusion', '=', True)], ['id', 'name'])
    return subCategories

def getInfo(name):
    global _odoo
    names=_odoo.SearchRead('product.template', [('name', '=', name)], ['id', 'name','default_code'])
    return names


def creatWref(name):
    '''
    global _odoo
    names=_odoo.SearchRead('product.template', [('name', '=', name)], ['id', 'name','default_code'])'''
    return name
    
def getSubsubCategoris():
    global _odoo

    subCategories = _odoo.SearchRead(
        'product.category', [('parent_id', '=', 'All / Hardware')], ['id', 'name'])
    return subCategories