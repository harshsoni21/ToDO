from pathlib import Path
import os
import json
import jsonschema
from jsonschema.validators import validate
from jsonmerge import SchemaError
from ToDO.AppLogging import app_logger


# ==================== Helper Functions =============================

def todo_api_schema_validation(api_info, request_type):
    config_path = os.path.join(Path(__file__).resolve().parent.parent.parent, 'config')
    api_schema = os.path.join(config_path, 'api_schema.json')

    config_dic = json.load(open(api_schema))
    workload_api_schema = config_dic[request_type]

    try:
        validate(instance=api_info, schema=workload_api_schema)
    except SchemaError as e:
        app_logger.debug(f"There is an error with the schema, request_type={request_type}, Error={e}")
        return False
    except jsonschema.exceptions.ValidationError as err:
        app_logger.error(f"Rest Api JsonSchema, request_type={request_type}, Error=={err}")
        return False

    return True