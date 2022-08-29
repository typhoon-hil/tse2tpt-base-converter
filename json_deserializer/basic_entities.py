from .abstract import Parentable, Nameable
from .constants import KIND_PE


class Node(Parentable, Nameable):
    """
    Models a node, which is a logical entity which encompasses
    all terminals which are directly connected.
    """
    def __init__(self, parent, name=None, terminals=None):
        """
        Initialize node.

        Args:
            parent(object): Parent of this object.
            terminals(iterable): Collection of terminals.
        """
        super().__init__(parent=parent, name=name)
        self._terminals = set()
        self.terminals = terminals

    @property
    def terminals(self):
        return {t for t in self._terminals}

    @terminals.setter
    def terminals(self, terminals):
        self._terminals = set()
        if terminals is not None:
            for terminal in terminals:
                self._terminals.add(terminal)

    def add_terminal(self, terminal):
        """
        Add terminal to this node, terminal node is updated to point
        to this node object.

        Args:
            terminal(Terminal): Terminal object to add.

        Returns:
            None
        """
        self._terminals.add(terminal)
        terminal.node = self

    def add_terminals(self, terminals):
        """
        Add terminals to this node.
        All terminals ``node`` attribute  will be updated to point
        to this node.

        Args:
            terminals(iterable): Iterable of terminals to add.

        Returns:
            None
        """
        for term in terminals:
            self.add_terminal(term)

    def remove_terminals(self, terminals):
        """
        Remove provided terminals from this node.

        Args:
            terminals(iterable): Iterable of terminals.

        Raises:
            KeyError exception if one or more provided terminals
            are not present in this node.

        Returns:
            None
        """
        for term in terminals:
            self.remove_terminal(term)

    def remove_terminal(self, terminal):
        """
        Remove provided terminal from this node.

        Args:
            terminal(Terminal): Terminal object to remove.

        Raises:
            KeyError exception if provided terminal is not
            present in this node.

        Returns:
            None
        """
        self._terminals.remove(terminal)


class Terminal(Parentable, Nameable):
    """ Models component terminal. """
    def __init__(self, parent, name, kind=KIND_PE, node=None):
        """
        Initialize a terminal.

        Args:
            parent(object): Parent of this object.
            name(str): Terminal name.
            kind(int): Terminal kind.
            node(Node): Node object which contains this terminal.
        """
        super().__init__(parent=parent, name=name)

        self.kind = kind
        self.node = node

    @property
    def fqn(self):
        if self.parent and hasattr(self.parent, "fqn"):
            return "{0}.{1}".format(self.parent.fqn, self.name)
        else:
            return self.name


class Property(Parentable, Nameable):
    """ Models a property (on component or mask). """
    def __init__(self, parent, name, value):
        """
        Initialize a property.

        Args:
            parent(object): Parent of this object.
            name(str): Property name.
            value(object): Property value.
        """
        super().__init__(parent=parent, name=name)

        self.value = value


class PropertyContainer(Parentable):
    """ Extract shared functionality for storing properties. """
    def __init__(self, parent, props=None, *args, **kwargs):
        """
        Initialize object.

        Args:
            parent(object): Parent of this object.
            props(iterable): Iterable of properties to add initially.
        """
        super().__init__(parent=parent, *args, **kwargs)

        self._prop_set = set()

        if props:
            self.add_properties(props)

    @property
    def properties(self):
        """ Return view to properties in dict form. """
        return {p.name: p for p in self._prop_set}

    def add_property(self, prop):
        """
        Add property.

        Args:
            prop(Property): Property object.

        Returns:
            None
        """
        prop.parent = self
        self._prop_set.add(prop)

    def add_properties(self, props):
        """
        Add multiple properties.

        Args:
            props(iterable): Iterable over properties.

        Returns:
            None
        """
        for prop in props:
            self.add_property(prop)

    def remove_property(self, prop):
        """
        Remove a single property from this property container.

        Args:
            prop(Property): Property object.

        Raises:
            KeyError exception if prvoded prop is not present.

        Returns:
            None
        """
        self._prop_set.remove(prop)

    def remove_properties(self, props):
        """ Remove multiple properties """
        for prop in props:
            self.remove_property(prop)


class Component(Nameable, PropertyContainer):
    """ Models a component. """
    def __init__(self, parent, name, comp_type, composite=None,
                 properties=None, terminals=None, parent_comp=None):
        """
        Initialize a component.

        Args:
            parent(object): Parent of this object.
            name(str): Component name.
            comp_type(str): Component type name.
            parent_comp(Component): Parent component.
            composite(bool): Indicate if component is a composite one.
            parent(Component): Parent of this component.
            properties(iterable): Iterable over properties.
            terminals(iterable): Component terminals.
        """
        super().__init__(props=properties, parent=parent, name=name)

        self.comp_type = comp_type
        self.parent_comp = parent_comp
        self.composite = composite if composite is not None else False

        self._terminals = set()
        if terminals:
            self.add_terminals(terminals)

    def __str__(self):
        return "Component '{0}'".format(self.fqn)

    @property
    def atomic(self):
        return not self.composite

    @property
    def fqn(self):
        if self.parent_comp:
            return "{0}.{1}".format(self.parent_comp.fqn, self.name)
        else:
            return self.name

    @property
    def parent_fqn(self):
        if self.parent_comp:
            return self.parent_comp.fqn
        else:
            return ""

    def add_terminal(self, terminal):
        terminal.parent = self
        self._terminals.add(terminal)

    def add_terminals(self, terminals):
        for term in terminals:
            self.add_terminal(term)

    @property
    def terminals(self):
        """ Returns a view to terminals in dict form. """
        return {t.name: t for t in self._terminals}
