import json
from src.models import YAMLModel, JSONModel, JSONModel2
import yaml
import sys


def yaml_to_json(yaml_filepath, json_filepath):
    """
        Parameters
        ----------
        yaml_filepath : str
            The path of file which'd be processed
        json_filepath : str
            The output filepath for result JSON file
    """
    #parse_file, parse_raw

    try:
        f = open(yaml_filepath, 'r')
        yaml_data = yaml.load(f)
        f.close()
        yaml_mod = YAMLModel.parse_obj(yaml_data)

        json_mod = JSONModel2.parse_obj(yaml_mod.dict())

        with open(json_filepath, 'w') as outputfile:
            json_data = json_mod.dict()
            b = json.dumps(json_data, indent=4)
            outputfile.write(b)
            outputfile.close()

    except Exception as exc:
        print('Error msg: ', exc)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(sys.argv)
        raise Exception(f"Got wrong number of parameters ({len(sys.argv)})!")
    input_yaml_path = sys.argv[1]
    output_json_path = sys.argv[2] if len(sys.argv) > 2 else f"./{input_yaml_path.replace('.yaml', '')}_output.json"

    print(yaml_to_json(input_yaml_path, output_json_path))
