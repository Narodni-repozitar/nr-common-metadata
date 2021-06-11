import pytest
from invenio_jsonschemas import current_jsonschemas
from invenio_records.api import _records_state
from jsonschema import ValidationError


def test_json(app, base_json):
    print("\n\n\n\n\n")
    print("START")
    print(app)
    print(current_jsonschemas.list_schemas())
    _records_state.validate(base_json, "https://nusl.cz/schemas/nr_common/nr-common-v1.0.0.json")


def test_json_2(app, base_json):
    print("\n\n\n\n\n")
    print("START")
    print(app)
    print(current_jsonschemas.list_schemas())
    del base_json["title"]
    with pytest.raises(ValidationError):
        _records_state.validate(base_json,
                                "https://nusl.cz/schemas/nr_common/nr-common-v1.0.0.json")
