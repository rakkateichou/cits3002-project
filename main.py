# main.py
import sys
import config
from devices import Host, Router

# 1. Initialize Nodes
host_a = Host("Host A", config.HOST_A_IP, config.HOST_A_MAC, config.R1_INT1_IP, config.R1_INT1_MAC)
host_b = Host("Host B", config.HOST_B_IP, config.HOST_B_MAC, config.R1_INT2_IP, config.R1_INT2_MAC)
router = Router("Router R1")

# 2. Wire the Topology together
host_a.link = router
host_b.link = router
router.interfaces["Interface 1"]["link"] = host_a
router.interfaces["Interface 2"]["link"] = host_b

# 3. Start the process (They will handle sys.argv for file size here)
# ...
# host_a.send_transport(data)
