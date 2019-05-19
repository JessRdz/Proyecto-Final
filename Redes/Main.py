import threading
from ConfigurationManagement import obtenerConfiguraciones

configThread = threading.Thread(target=obtenerConfiguraciones)
configThread.run()