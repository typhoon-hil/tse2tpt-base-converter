from .json_deserializer import Component, ModelPartition

def connected_components(comp_handle: Component, comp_type="all"):
    """ Return all components of comp_type that are directly connected to the provided component """

    connected_components_set = set()
    comp_terminals = comp_handle.terminals
    for terminal_name, terminal_handle in comp_terminals.items():
        terminal_node_handle = terminal_handle.node
        # Get all terminals connected to this node
        all_connected_terminals = terminal_node_handle.terminals
        # Get the parents (components) of each of the terminals
        for connected_terminal in all_connected_terminals:
            connected_comp = connected_terminal.parent
            if not connected_comp == comp_handle:
                if comp_type == "all":
                    connected_components_set.add(connected_comp)
                elif comp_type == connected_comp.comp_type:
                    connected_components_set.add(connected_comp)

    return connected_components_set


def connected_terminals(comp_1: Component, comp_2: Component,
                        comp1_terminals=False, comp2_terminals=False, handle_mode=False):
    """ Find connected terminals between two components.
        May specify the list of terminals to be checked for each component.
        handle_mode returns the handle instead of the name of the terminals."""

    connected_terminals_dict = {}

    comp_1_terminals = comp_1.terminals
    comp_2_terminals = comp_2.terminals
    for terminal_name_1, terminal_handle_1 in comp_1_terminals.items():
        terminal_node_handle_1 = terminal_handle_1.node
        if not comp1_terminals or terminal_name_1 in comp1_terminals:
            terminals_2_list = []
            for terminal_name_2, terminal_handle_2 in comp_2_terminals.items():
                terminal_node_handle_2 = terminal_handle_2.node
                if not comp2_terminals or terminal_name_2 in comp2_terminals:
                    if terminal_node_handle_2 == terminal_node_handle_1:
                        if handle_mode:
                            # Return terminal handles
                            terminals_2_list.append(terminal_handle_2)
                            connected_terminals_dict.update({terminal_handle_1: terminals_2_list})
                        else:
                            # Return terminal names
                            terminals_2_list.append(terminal_name_2)
                            connected_terminals_dict.update({terminal_name_1: terminals_2_list})

    return connected_terminals_dict


def get_all_component_names(tse_model: ModelPartition):
    componenent_names = []
    tse_model.components
