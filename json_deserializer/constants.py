KIND_PE = "pe"
KIND_SP = "sp"

P_NODE = "p_node"
N_NODE = "n_node"
# switch terminal names
SW_IN = "a_in"
SW_OUT = "a_out"

# component types
SRC_CURRENT = "Current Source"
SRC_VOLTAGE = "Voltage Source"
MSR_CURRENT = "Current Measurement"
MSR_VOLTAGE = "Voltage Measurement"
PAS_RESISTOR = "Resistor"
PAS_CAPACITOR = "Capacitor"
PAS_INDUCTOR = "Inductor"
SRC_VCVS = "el_vcvs"  # "Voltage Controlled Voltage Source"
SRC_VCCS = "el_vccs"  # "Voltage Controlled Current Source"
SRC_CCVS = "el_ccvs"  # "Current Controlled Voltage Source"
SRC_CCCS = "el_cccs"  # "Current Controlled Current Source"
EL_SHORT = "el_short"
EL_OPEN = "Open Circuit"  # "el_open"
EL_SWITCH = "Single Pole Single Throw Contactor"
SRC_GND = "Ground"
OFFLINE_SOLVER_COMP_TYPE = "Offline Solver Library/Offline Solver"

COMPONENT_TYPES = [SRC_CURRENT, SRC_VOLTAGE, MSR_CURRENT, MSR_VOLTAGE, PAS_RESISTOR, PAS_CAPACITOR,
                   PAS_INDUCTOR, SRC_VCVS, SRC_VCCS, SRC_CCVS, SRC_CCCS, EL_SHORT, EL_OPEN, EL_SWITCH, SRC_GND]

switch_term_map = {SW_IN: P_NODE,
                   SW_OUT: N_NODE}
