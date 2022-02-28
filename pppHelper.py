#Property++ Helper

def decodePppAttributes(attributes):
    properies = {}
    partProperisAttrib = attributes.itemByName(
        'ProppertiesPP', 'custProp_0').value
    assemblyProperisAttrib = attributes.itemByName(
        'ProppertiesPP', 'custProp_1').value
    desingProperisAttrib = attributes.itemByName(
        'ProppertiesPP', 'custProp_2').value
    commonProperisAttrib = attributes.itemByName(
        'ProppertiesPP', 'custProp_3').value
    # cust_prop0 = cust_prop0.value
    # print(cust_prop0)
    # lines = partProperisAttrib.split('~~')
    # partProperies = {}
    # for line in lines:
    # cols = line.split('~')
    # print(cols)
    # custAttrib = attributes.itemByName('ProppertiesPP', cols[0]).value
    # if custAttrib:
    # print(custAttrib)
    # partProperies[cols[3]] = custAttrib

    # print(partProperies)
    # for attrib in attributes:
    # print('{}:{}'.format(attrib.name, attrib.value))
