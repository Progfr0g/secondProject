import pytest
import os.path
from src.main import yaml_to_json

def test_yaml_to_json():

    input_yaml_path = "../src/sample.yaml"
    output_json_path = f"./{input_yaml_path.replace('.yaml', '')}_output.json"

    if os.path.isfile(output_json_path):
        os.remove(output_json_path)

    yaml_to_json(input_yaml_path, output_json_path)

    assert os.path.isfile(output_json_path) == True, "the result file was not created"