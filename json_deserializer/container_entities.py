# from json_deserializer import Component
from .abstract import Parentable, Nameable


class ModelPartition(Parentable, Nameable):
    """
        Models part of the model including components and connections between them.
    """

    def __init__(self, parent, name, parent_components=None, components=None, nodes=None):
        """
        Initialize an object.
        """
        super().__init__(parent=parent, name=name)

        self._comp_dict = {}
        self._par_comp_dict = {}
        self._node_set = set()

        if parent_components:
            self.add_parent_components(parent_components)

        if components:
            self.add_components(components)

        if nodes:
            self.add_nodes(nodes)

    def add_component(self, component):
        component.parent = self
        self._comp_dict[component.fqn] = component

    def add_components(self, components):
        for comp in components:
            self.add_component(comp)

    def add_parent_component(self, parent_component):
        parent_component.parent = self
        self._par_comp_dict[parent_component.fqn] = parent_component

    def add_parent_components(self, parent_components):
        for comp in parent_components:
            self.add_parent_component(comp)

    def remove_component_by_fqn(self, component_fqn):
        del self._comp_dict[component_fqn]

    @property
    def components(self):
        return self._comp_dict.values()

    @property
    def parent_components(self):
        return self._par_comp_dict.values()

    @property
    def components_by_fqn(self):
        return self._comp_dict

    def get_components_by_type(self, comp_type):
        return (component for component in self.components
                if component.comp_type == comp_type)

    def add_node(self, node):
        self._node_set.add(node)
        node.parent = self

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    @property
    def nodes(self):
        return {n for n in self._node_set}

    def insert_component_parallel(self, new_comp, existing_comp):
        """
        Insert component ``new_comp`` parallel to the ``existing_comp``
        component like this:

                   --------new_comp------------
                  |                            |
        ... ------o--------existing_comp-------o--- ...

        Args:
            new_comp(Component): Component to insert.
            existing_comp(Component): Component around which to insert
                source component.

        Returns:
            None
        """
        self.add_component(new_comp)

        new_term_p = new_comp.terminals["p_node"]
        new_term_n = new_comp.terminals["n_node"]

        # Remove new component from existing nodes.
        new_term_p_node = new_term_p.node
        new_term_n_node = new_term_n.node

        if new_term_p_node and new_term_p in new_term_p_node:
            new_term_p_node.remove_terminal(new_term_p)
            new_term_p.node = None

        if new_term_n_node and new_term_n in new_term_n_node:
            new_term_n_node.remove_terminal(new_term_n)
            new_term_n.node = None

        # Update nodes and new component terminal connection to it.
        existing_p_node = existing_comp.terminals["p_node"].node
        existing_n_node = existing_comp.terminals["n_node"].node
        existing_p_node.add_terminal(new_term_p)
        existing_n_node.add_terminal(new_term_n)

    def insert_component_antiparallel(self, new_comp, existing_comp):
        """
        Insert component ``new_comp`` parallel to the ``existing_comp``
        component like this:

                   --------new_comp------------
                  |                            |
        ... ------o--------existing_comp-------o--- ...

        But in this antiparallel case n terminal of new component is connected with p terminal of existing component and
        vise versa

        Args:
            new_comp(Component): Component to insert.
            existing_comp(Component): Component around which to insert
                source component.

        Returns:
            None
        """
        self.add_component(new_comp)

        new_term_p = new_comp.terminals["p_node"]
        new_term_n = new_comp.terminals["n_node"]

        # Remove new component from existing nodes.
        new_term_p_node = new_term_p.node
        new_term_n_node = new_term_n.node

        if new_term_p_node and new_term_p in new_term_p_node:
            new_term_p_node.remove_terminal(new_term_p)
            new_term_p.node = None

        if new_term_n_node and new_term_n in new_term_n_node:
            new_term_n_node.remove_terminal(new_term_n)
            new_term_n.node = None

        # Update nodes and new component terminal connection to it.
        existing_p_node = existing_comp.terminals["p_node"].node
        existing_n_node = existing_comp.terminals["n_node"].node
        existing_p_node.add_terminal(new_term_n)
        existing_n_node.add_terminal(new_term_p)

    def replace_component(self, new_comp, old_comp):
        """
        This method replaces an existing component with the provided new one.
            - gets the nodes where old componente was connected
            - removes the old component
            - adds a new component
            - adds the terminals of new component to the nodes

        """
        # Get the existing nodes for p and n ports
        existing_p_node = old_comp.terminals["p_node"].node
        existing_n_node = old_comp.terminals["n_node"].node

        # Disconnect old component
        for old_term_name, old_term in old_comp.terminals.items():
            # remove old component terminal from node
            aux_node = old_term.node
            aux_node.remove_terminal(old_term)
            # remove node from old component terminal
            old_term.node = None

        # Remove old component
        del self._comp_dict[old_comp.fqn]  # remove old component from components

        # Add the new component
        self.add_component(new_comp)
        # Get the terminals of new component
        new_term_p = new_comp.terminals["p_node"]
        new_term_n = new_comp.terminals["n_node"]

        # Remove new component from existing nodes. if there are
        new_term_p_node = new_term_p.node
        new_term_n_node = new_term_n.node

        if new_term_p_node and new_term_p in new_term_p_node:
            new_term_p_node.remove_terminal(new_term_p)
            new_term_p.node = None

        if new_term_n_node and new_term_n in new_term_n_node:
            new_term_n_node.remove_terminal(new_term_n)
            new_term_n.node = None

        # Update nodes and new component terminal connection to it.
        existing_p_node.add_terminal(new_term_p)
        existing_n_node.add_terminal(new_term_n)

    def unwire_component_leave_nodes(self, comp):
        """
        Removes component terminals from the nodes they're connected to.
        Args:
            comp(Component): component whose terminals are removed.
        Returns:
        """
        p_node = comp.terminals["p_node"].node
        p_node.remove_terminal(comp.terminals["p_node"])
        n_node = comp.terminals["n_node"].node
        n_node.remove_terminal(comp.terminals["n_node"])

    def unwire_component_merge_nodes(self, comp):
        """
        Merges nodes of p and n terminals into a new one and removes the remaining node from the nodes set.
        Args:
            comp (Component): component whose nodes will be merged.
        Returns:
            terminals(iterable) - Saves info about component's terminals before merging of the nodes.
                Keys: p_node, n_node.
                Each value is a list of dictionaries which correspond to components connected to the node
                at p_node/n_node component terminal, excluding the component's own p_node/n_node terminal.
                Their keys are: comp_fqn - connecting component's FQN (string)
                                comp_type - connecting component's type (string)
                                node_type - connecting component's terminal type: "p_node" or "n_node" (string)
        """

        terminals = {"p_node": None, "n_node": None}
        terminal_types = terminals.keys()

        for terminal_type in terminal_types:
            terminal_comps = []
            for terminal in comp.terminals[terminal_type].node.terminals:
                if terminal not in comp.terminals.values():
                    terminal_comps.append({"comp_fqn": terminal.parent.fqn,
                                           "comp_type": terminal.parent.comp_type,
                                           "node_type": terminal.name})
            terminals[terminal_type] = terminal_comps

        new_node = comp.terminals["p_node"].node
        new_node.remove_terminal(comp.terminals["p_node"])  # remove p_node from new_node
        other_node = comp.terminals["n_node"].node
        other_node.remove_terminal(comp.terminals["n_node"])  # remove n_node from the other_node

        new_node.add_terminals(other_node.terminals)  # once the component terminals have been removed,
        # the nodes can be merged

        self._node_set.remove(other_node)
        comp.terminals["n_node"].node = comp.terminals["p_node"].node
        return terminals

    def remove_node(self, node):
        """
        Removes the node object from the collection of nodes.
        This method doesn't remove the node object from components terminals.
        Args:
            node(object): Node to be removed
        """
        self._node_set.remove(node)


class Model(Nameable):
    """ Models a top level container. """

    def __init__(self, name,
                 model_partitions=None):
        """
        Initialize an object.

        Args:
            name (str): Model name.
            model_partitions(iterable): Collection of model partitions.
        """
        super().__init__(name=name)

        self._model_partitions = set()
        if model_partitions:
            self.add_model_partitions(model_partitions)

    def add_model_partition(self, model_partition):
        self._model_partitions.add(model_partition)
        model_partition.parent = self

    def add_model_partitions(self, model_partitions):
        for model_partition in model_partitions:
            self.add_model_partition(model_partition)

    @property
    def model_partitions(self):
        return {model_part.name: model_part for model_part in self._model_partitions}
