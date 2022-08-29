from types import TracebackType
from ..json_deserializer import Node, Terminal, Property, Component, Model, ModelPartition
import numpy as np
import itertools as it
import functools as fn
import json


class JSONDeserializer:
    """ Deserializer for JSON file exported from Typhoon Schematic Editor"""

    def __init__(self, json_file_path: str):
        """
            Initialize an object.
            :param json_file_path: Path to model that contains Model description.
        """

        self.file_path = json_file_path
        self.obj_bytes = None

    def load_bytes_from_file(self):
        """
            Loads bytes from .json file
            :return: None
        """

        try:
            with open(self.file_path, "r") as handle:
                content = handle.read()
                self.obj_bytes = content.encode("utf-8")
        except:
            raise ModelDeserializationError(ModelDeserializationError.CANT_READ_FROM_MDL_FILE,
                                            file_path=self.file_path)

    def get_model(self):
        """
            Reconstruct model graph from JSON bytes.
            :return: Model
        """
        obj_hook = fn.partial(json_obj_hook, terminal_ids={}, component_ids={})

        try:
            model = json.loads(self.obj_bytes, object_hook=obj_hook)
            return model
        except:
            raise ModelDeserializationError(ModelDeserializationError.CANT_DESERIALIZE_DATA)


class ModelDeserializationError(Exception):
    """
    Raised in case of error during model deserialization.
    """

    CANT_READ_FROM_MDL_FILE = "Cant read from model file"
    CANT_DESERIALIZE_DATA = "Unable to deserialize data."

    def __init__(self, error_type, file_path=None):
        self.error_type = error_type
        self._file_path = file_path

    @property
    def error_string(self):
        error_string = self.error_type
        if self.error_type == ModelDeserializationError.CANT_READ_FROM_MDL_FILE:
            error_string += ": File not found or program have no permision to read from given file: {0}".format(
                self._file_path)

        return error_string


def json_obj_hook(obj: dict, terminal_ids={}, component_ids={}):
    """
    Function used to help JSON loads() to make correct types of objects.

    Args:
        obj(dict): Dict object provided by json loads() function.
        terminal_ids(dict): Memo for terminal ids.
        component_ids(dict): Memo for component ids.
    Returns:
        Concrete object based on provided dictionary.
    """
    if obj and "_cls" in obj:
        obj_cls = obj["_cls"]

        if obj_cls == "Property":
            return Property(
                parent=None,
                name=obj["name"],
                value=obj["value"])
        elif obj_cls == "Component":
            # Add mask properties
            all_properties = obj["properties"]
            if obj.get("masks"):
                all_properties.extend(obj["masks"][0].get("properties"))

            component = Component(parent=None,
                                  name=obj["name"],
                                  comp_type=obj["comp_type"],
                                  composite=obj["composite"],
                                  properties=all_properties,
                                  terminals=obj["terminals"],
                                  parent_comp=obj["parent_comp_id"])
            component_ids[obj["id"]] = component

            return component
        elif obj_cls == "Terminal":
            terminal = Terminal(
                parent=None, name=obj["name"], kind=obj["kind"])
            terminal_ids[obj["id"]] = terminal

            return terminal

        elif obj_cls == "Model":

            # Resolve nodes terminals
            for model_part in obj["dev_partitions"]:
                for node in model_part.nodes:
                    term_ids = node.terminals
                    node.terminals = set()

                    terms = (terminal_ids[term_id] for term_id in term_ids)
                    node.add_terminals(terms)

            return Model(name=obj["name"],
                         model_partitions=obj["dev_partitions"])

        elif obj_cls == "DevPartition":
            #
            # Resolve parents first  leaf components and parent
            # component themselves.
            #
            components = obj["components"]
            parent_components = obj["parent_components"]

            for comp in it.chain(components, parent_components):
                comp_parent_id = comp.parent_comp
                try:
                    comp.parent_comp = component_ids[comp_parent_id]
                except KeyError:
                    pass

            return ModelPartition(
                parent=None,
                name=obj["name"],
                parent_components=parent_components,
                components=components,
                nodes=obj["nodes"])
        elif obj_cls == "Node":
            terminal_ids = obj["terminals"]
            node = Node(parent=None, terminals=None, name=obj["id"])
            node._terminals = terminal_ids

            return node
        elif obj_cls == "set":
            return set(obj["value"])
        elif obj_cls == "ndarray":
            return np.array(obj["value"])
        elif obj_cls in {"int8", "int16", "int32", "int64", "uint8", "uint16",
                         "uint32", "uint64"}:
            try:
                np_type = getattr(np, obj_cls)
                real_value = np_type(obj["value"])
            except AttributeError:
                real_value = obj["value"]
            return real_value
        elif obj_cls == "complex":
            parts = obj["value"]
            return complex(parts[0], parts[1])
        elif obj_cls == "range":
            range_descr = obj["value"]
            return range(range_descr[0], range_descr[1], range_descr[2])

    return obj
