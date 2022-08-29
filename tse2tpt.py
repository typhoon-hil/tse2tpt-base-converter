from .json_deserializer import JSONDeserializer

def load_json(json_file):
    model_handle = JSONDeserializer(json_file)
    model_handle.load_bytes_from_file()
    model = model_handle.get_model().model_partitions.get("hil0")
    return model

def start_conversion(input_json_path, output_format_module, simulation_parameters=None):
    """ Convert the input JSON to the new format defined by output_format_module."""

    # Deserialize the JSON file
    tse_model = load_json(input_json_path)

    # Convert the TSE model to the new format (import the function in the output module's __init__.py)
    new_format = output_format_module.convert(tse_model, input_json_path, simulation_parameters)

    # Generate output files from the new format (import the function in the output module's __init__.py)
    debug = output_format_module.generate_output_files(new_format)

    return debug
