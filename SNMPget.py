from pysnmp.hlapi import *


def getSNMP(direccion, usuario, password, mib):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               UsmUserData(usuario, password),
               UdpTransportTarget((direccion, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(mib)))
    )
    resultado = "ERROR"
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        resultado = ""
        for varBind in varBinds:
            resultado = resultado + ' = '.join([x.prettyPrint() for x in varBind])

    return resultado
