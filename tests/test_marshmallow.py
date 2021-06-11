from datetime import datetime

import pytest
from marshmallow import ValidationError

from nr_common.marshmallow import CommonMetadataSchemaV2


def test_required_fields(app, db, taxonomy_tree, base_json, base_json_dereferenced):
    schema = CommonMetadataSchemaV2()
    json = base_json
    result = schema.load(json)
    assert result == base_json_dereferenced


class TestAbstract:
    def test_abstract_load_1(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        abstract_ = {
            "cs": "Testovací abstrakt",
            "en": "Test abstract"
        }
        base_json["abstract"] = abstract_
        base_json_dereferenced["abstract"] = abstract_
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_abstract_load_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        abstract_ = [{
            "cs": "Testovací abstrakt",
            "en": "Test abstract"
        }]
        base_json["abstract"] = abstract_
        base_json_dereferenced["abstract"] = abstract_
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)

    def test_abstract_load_3(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        abstract_ = {
            "cs": "Testovací abstrakt",
            "zz": "Test abstract"
        }
        base_json["abstract"] = abstract_
        base_json_dereferenced["abstract"] = abstract_
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)

    def test_abstract_load_4(self, db, taxonomy_tree, base_json, base_json_dereferenced):
        abstract_ = {
            "blbost": "Testovací abstrakt",
            "en": "Test abstract"
        }
        base_json["abstract"] = abstract_
        base_json_dereferenced["abstract"] = abstract_
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)


class TestAccessibility:
    def test_accessibility(self, db, taxonomy_tree, base_json, base_json_dereferenced):
        acc_ = {
            "cs": "Dostupné kdesi blabla",
            "en": "Avallable at blabla"
        }
        base_json["accessibility"] = acc_
        base_json_dereferenced["accessibility"] = acc_
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_accessibility_2(self, db, taxonomy_tree, base_json, base_json_dereferenced):
        acc_ = [
            {
                "value": "Dostupné kdesi blabla",
                "lang": "cz"
            },
            {
                "value": "Avallable at blabla",
                "lang": "en"
            }
        ]
        base_json["accessibility"] = acc_
        base_json_dereferenced["accessibility"] = acc_
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)


class TestAccessRights:
    def test_access_rights_1(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        ar = {
        }
        base_json["accessRights"] = ar
        base_json_dereferenced["accessRights"] = ar
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)

    def test_access_rights_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        ar = [{
        }]
        base_json["accessRights"] = ar
        base_json_dereferenced["accessRights"] = ar
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)

    def test_access_rights_3(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        ar = [{
            "links": {
                "self": "bla"
            }
        }]
        base_json["accessRights"] = ar
        base_json_dereferenced["accessRights"] = ar
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValueError):
            schema.load(base_json)


class TestCreator:
    def test_creator(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = [{
            "name": "Daniel Kopecký",
            "ORCID": "125456",
            "scopusID": "125456",
            "researcherID": "125456",
            "czenasAutID": "125456",
            "institutionalID": "vscht123456"
        }]
        field = "creator"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_creator_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        """
        Unknown field
        """
        content = [{
            "name": "Daniel Kopecký",
            "randomID": "123456"
        }]
        field = "creator"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)

    def test_creator_3(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        """
        Wrong data type
        """
        content = {
            "name": "Daniel Kopecký",
        }
        field = "creator"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)

    def test_creator_4(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        """
        Missing required field
        """
        content = [{
            "ORCID": "12455"
        }]
        field = "creator"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)


class TestContributor:
    def test_contributor_1(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = [{
            "name": "Daniel Kopecký",
            "ORCID": "125456",
            "scopusID": "125456",
            "researcherID": "125456",
            "czenasAutID": "125456",
            "institutionalID": "vscht123456",
            "role": [
                {
                    "links": {
                        "self": "http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/supervisor"
                    }
                }
            ]
        }]
        field = "contributor"
        base_json[field] = content
        base_json_dereferenced[field] = content
        base_json_dereferenced[field][0]["role"] = [{
            'dataCiteCode': 'Supervisor',
            'level': 1,
            'is_ancestor': False,
            'links': {
                'self':
                    'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/supervisor'
            },
            'title': {
                'cs': 'supervizor', 'en': 'supervisor'
            }
        }]
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_contributor_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        """
        Wrong datatype
        """
        content = {
            "name": "Daniel Kopecký",
            "ORCID": "125456",
            "scopusID": "125456",
            "researcherID": "125456",
            "czenasAutID": "125456",
            "institutionalID": "vscht123456",
            "role": [
                {
                    "links": {
                        "self": "http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/supervisor"
                    }
                }
            ]
        }
        field = "contributor"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)

    def test_contributor_3(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        """
        Missing required field (role)
        """
        content = [{
            "name": "Daniel Kopecký",
            "ORCID": "125456",
            "scopusID": "125456",
            "researcherID": "125456",
            "czenasAutID": "125456",
            "institutionalID": "vscht123456",
        }]
        field = "contributor"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)

    def test_contributor_4(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        """
        Missing required field (name)
        """
        content = {
            "role": [
                {
                    "links": {
                        "self": "http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/supervisor"
                    }
                }
            ]
        }
        field = "contributor"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)


class TestDateIssued:
    def test_date_issued_1(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = "2020"
        field = "dateIssued"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_date_issued_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = "2020-07"
        field = "dateIssued"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_date_issued_3(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = "2020-07-01"
        field = "dateIssued"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_date_issued_4(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        date = "2020-07-01"
        content = "bla bla %s" % date
        field = "dateIssued"
        base_json[field] = content
        base_json_dereferenced[field] = date
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_date_issued_5(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        date = "2020-07"
        content = "bla bla %s" % date
        field = "dateIssued"
        base_json[field] = content
        base_json_dereferenced[field] = date
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_date_issued_6(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = "2020-13"
        field = "dateIssued"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)

    def test_date_issued_7(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = datetime(2020, 1, 1)
        field = "dateIssued"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)

    def test_date_issued_8(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = ["2020-13"]
        field = "dateIssued"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)

    def test_date_issued_9(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = "201"
        field = "dateIssued"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError, match='Wrong date format'):
            schema.load(base_json)


class TestDateModified:
    def test_date_issued_1(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = "2020"
        field = "dateIssued"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_date_issued_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = "2020-07"
        field = "dateIssued"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_date_issued_3(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = "2020-07-01"
        field = "dateIssued"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_date_issued_4(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        date = "2020-07-01"
        content = "bla bla %s" % date
        field = "dateIssued"
        base_json[field] = content
        base_json_dereferenced[field] = date
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_date_issued_5(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        date = "2020-07"
        content = "bla bla %s" % date
        field = "dateIssued"
        base_json[field] = content
        base_json_dereferenced[field] = date
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_date_issued_6(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = "2020-13"
        field = "dateIssued"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)

    def test_date_issued_7(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = datetime(2020, 1, 1)
        field = "dateIssued"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)

    def test_date_issued_8(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = ["2020-13"]
        field = "dateIssued"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)


class TestResourceType:
    def test_resource_type_1(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = [
            {
                "links": {
                    "self": "http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/bakalarske-prace"
                }
            }
        ]
        field = "resourceType"
        base_json[field] = content
        # base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_resource_type_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = [
            {
                "links": {
                    "self": "http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/bla"
                }
            }
        ]
        field = "resourceType"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)


class TestExtent:
    def test_extent(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = ["128 s."]
        field = "extent"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_extent_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        """
        Wrong data type
        """
        content = 128
        field = "extent"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)


class TestExternalLocation:
    def test_external_location(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = "http://example.com"
        field = "externalLocation"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_external_location_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        """
        Wrong URL format
        """
        content = "www.example.com"
        field = "externalLocation"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)


class TestControlNumber:
    def test_control_number(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = "128"
        field = "control_number"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_control_number_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        """
        Wrong data type
        """
        content = 128
        field = "control_number"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)


class TestRecordIdentifiers:
    def test_record_identifiers(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = {
            "nuslOAI": "oai:invenio.nusl.cz:1",
            "nrcrHandle": "http://hdl.handle.net/20.500.11956/119618",
            "nrcrOAI": "oai:narodni-repozitar.cz:1",
            "originalRecord": "https://dspace.cuni.cz/handle/20.500.11956/119684",
            "originalRecordOAI": "oai:dspace.cuni.cz:20.500.11956/111006",
            "catalogueSysNo": "1"
        }
        field = "recordIdentifiers"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_record_identifiers_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = {
            "nuslOAI": "oai:invenio.nusl.cz:1",
            "nrcrHandle": "http://hdl.handle.net/20.500.11956/119618",
            "nrcrOAI": "oai:narodni-repozitar.cz:1",
            "originalRecord": "https://dspace.cuni.cz/handle/20.500.11956/119684",
            "originalRecordOAI": "oai:dspace.cuni.cz:20.500.11956/111006",
            "catalogueSysNo": "1"
        }
        field = "recordIdentifiers"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_record_identifiers_3(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = {
            "nuslOAI": "oai:invenio.nusl.cz:1",
            "nrcrHandle": "http://hdl.handle.net/20.500.11956/119618",
            "nrcrOAI": "oai:narodni-repozitar.cz:1",
            "originalRecord": 'http://hdl.handle.net/20.500.11956/111006',
            "originalRecordOAI": "oai:dspace.cuni.cz:20.500.11956/111006",
            "catalogueSysNo": "1"
        }
        field = "recordIdentifiers"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced


class TestWorkIdentifiers:
    def test_work_identifiers(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = {
            "isbn": ["978-3-16-148410-0"],
            "issn": ["2049-3630"],
            "doi": "10.1021/acs.jced.6b00139",
            "RIV": "RIV/61388980:_____/13:00392389"
        }
        field = "workIdentifiers"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_work_identifiers_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        """
        Bad ISBN
        """
        content = {
            "isbn": ["978-3-16-148410-7"],
            "issn": ["2049-3630"],
            "doi": "10.1021/acs.jced.6b00139",
            "RIV": "RIV/61388980:_____/13:00392389"
        }
        field = "workIdentifiers"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)

    def test_work_identifiers_3(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        """
        Bad ISSN
        """
        content = {
            "issn": ["2049-363X"],
        }
        field = "workIdentifiers"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)

    def test_work_identifiers_4(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        """
        Bad DOI
        """
        content = {
            "doi": ".102/acs.jced.6b00139",
        }
        field = "workIdentifiers"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)

    def test_work_identifiers_5(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        """
        Bad RIV
        """
        content = {
            "RIV": "RI/61388980:_____/13:00392389"
        }
        field = "workIdentifiers"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)


class TestIsGL:
    def test_is_gl(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = True
        field = "isGL"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_is_gl_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        """
        Bad type
        """
        content = "bla"
        field = "isGL"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)

    def test_is_gl_3(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = 1
        field = "isGL"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_is_gl_4(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = 0
        field = "isGL"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced


class TestLanguage:
    def test_language_1(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = {
            "links": {
                "self": "http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/cze"
            }
        }
        field = "language"
        base_json[field] = content
        # base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_language_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = {
            "links": {
                "self": "http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/bla"
            }
        }
        field = "language"
        base_json[field] = content
        # base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)

    def test_language_3(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = []
        field = "language"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError, match='Language is required field'):
            schema.load(base_json)


class TestNote:
    def test_note_1(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = ["Bla", "spam"]
        field = "note"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_note_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        """
        Bad data type
        """
        content = "Bla"
        field = "note"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)


class TestFundingReference:
    def test_funding_reference_1(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = [
            {
                "projectName": "Project Name 1",
                "fundingProgram": "National repository",
            }
        ]
        field = "fundingReference"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_funding_reference_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = [
            {
                "projectID": "123456789",
                "projectName": "Project Name 1",
                "fundingProgram": "National repository",
                "funder": [
                    {
                        "links": {
                            "self": "http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/ntk"
                        }
                    }
                ]
            }
        ]
        dereferenced_content = [{
            'funder': [{
                'level': 1,
                'funderISVaVaICode': '123456789',
                'is_ancestor': False,
                'links': {
                    'self':
                        'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/ntk'
                },
                'title': {
                    'cs': 'Národní technická knihovna',
                    'en': 'National library of '
                          'technology'
                }
            }],
            'fundingProgram': 'National repository',
            'projectID': '123456789',
            'projectName': 'Project Name 1'
        }]
        field = "fundingReference"
        base_json[field] = content
        base_json_dereferenced[field] = dereferenced_content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_funding_reference_3(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = [
            {
                "projectName": "Project Name 1",
                "fundingProgram": "National repository",
                "funder": [
                    {
                        "links": {
                            "self": "http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/ntk"
                        }
                    }
                ]
            }
        ]
        dereferenced_content = [{
            'funder': [{
                'funderISVaVaICode': '123456789',
                'is_ancestor': False,
                'level': 1,
                'links': {
                    'self':
                        'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/ntk'
                },
                'title': {
                    'cs': 'Národní technická knihovna',
                    'en': 'National library of '
                          'technology'
                }
            }],
            'fundingProgram': 'National repository',
            'projectName': 'Project Name 1'
        }]
        field = "fundingReference"
        base_json[field] = content
        base_json_dereferenced[field] = dereferenced_content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_funding_reference_4(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = [
            {
                "projectID": "123456789",
                "projectName": "Project Name 1",
                "fundingProgram": "National repository",
            }
        ]

        field = "fundingReference"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)


class TestProvider:
    def test_provider_1(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = [
            {
                "links": {
                    "self": 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/61384984'
                }
            },
        ]
        field = "provider"
        base_json[field] = content
        base_json_dereferenced[field] = [{
            'level': 1,
            'address': 'Malostranské náměstí 259/12, '
                       '118 00 Praha 1',
            'aliases': ['AMU'],
            'ico': '61384984',
            'is_ancestor': False,
            'links': {
                'self':
                    'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/61384984'
            },
            'provider': True,
            'related': {'rid': '51000'},
            'title': {
                'cs': 'Akademie múzických umění v Praze',
                'en': 'Academy of Performing Arts in Prague'
            },
            'type': 'veřejná VŠ',
            'url': 'https://www.amu.cz'
        }]
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_provider_1b(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = [
            {
                "links": {
                    "self": 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/61384984'
                }
            },
            {
                "links": {
                    "self": 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/60461373'
                }
            },
        ]
        field = "provider"
        base_json[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)

    def test_provider_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = [
            {
                "links": {
                    "self": 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/bla'
                },
            }
        ]
        field = "provider"
        base_json[field] = content
        base_json_dereferenced[field] = [{
            'address': 'Malostranské náměstí 259/12, '
                       '118 00 Praha 1',
            'aliases': ['AMU'],
            'ico': '61384984',
            'is_ancestor': False,
            'links': {
                'self':
                    'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/61384984'
            },
            'provider': True,
            'related': {'rid': '51000'},
            'title': {
                'cs': 'Akademie múzických umění v Praze',
                'en': 'Academy of Performing Arts in Prague'
            },
            'type': 'veřejná VŠ',
            'url': 'https://www.amu.cz'
        }]
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)


class TestPublicationPlace:
    def test_publication_place(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = {
            "place": "Praha",
            "country": [
                {
                    "links": {
                        "self": "http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/cz"
                    }
                }
            ]
        }
        field = "publicationPlace"
        base_json[field] = content
        base_json_dereferenced[field] = {
            'country': [{
                'code': {
                    'alpha2': 'CZ',
                    'alpha3': 'CZE',
                    'number': '203'
                },
                'level': 1,
                'is_ancestor': False,
                'links': {
                    'self': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/cz'
                },
                'title': {'cs': 'Česko', 'en': 'Czechia'}
            }],
            'place': 'Praha'
        }
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_publication_place_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = {
            "place": "Praha",
            "country": [
                {
                    "links": {
                        "self": "http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/bla"
                    }
                }
            ]
        }
        field = "publicationPlace"
        base_json[field] = content
        base_json_dereferenced[field] = {
            'country': [{
                'code': {
                    'alpha2': 'CZ',
                    'alpha3': 'CZE',
                    'number': '203'
                },
                'is_ancestor': False,
                'links': {
                    'self': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/cz'
                },
                'title': {'cs': 'Česko', 'en': 'Czechia'}
            }],
            'place': 'Praha'
        }
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)


class TestPublisher:
    def test_publisher(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = ["bla", "bla2"]
        field = "publisher"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_publisher_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = "bla"
        field = "publisher"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)


class TestRelatedItem:
    def test_related_item_1(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = [
            {
                "itemTitle": "Some title",
                "itemISBN": ["978-3-16-148410-0"],
                "itemISSN": ["2049-3630"],
                "itemDOI": "10.1021/acs.jced.6b00139",
                "itemURL": "https://example.com",
                "itemYear": "2020",
                "itemVolume": "2",
                "itemIssue": "25",
                "itemStartPage": "15",
                "itemEndPage": "30",
                "itemRelationType": {
                    "links": {
                        "self": 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/isversionof'
                    }
                }
            }
        ]
        field = "relatedItem"
        base_json[field] = content
        base_json_dereferenced[field] = [{
            'itemDOI': '10.1021/acs.jced.6b00139',
            'itemEndPage': '30',
            'itemISBN': ['978-3-16-148410-0'],
            'itemISSN': ['2049-3630'],
            'itemIssue': '25',
            'itemRelationType': [{
                'level': 1,
                'is_ancestor': False,
                'links': {
                    'self':
                        'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/isversionof'
                },
                'title': {
                    'cs': 'jeVerzí',
                    'en': 'isVersionOf'
                }
            }],
            'itemStartPage': '15',
            "itemTitle": "Some title",
            'itemURL': 'https://example.com',
            'itemVolume': '2',
            'itemYear': '2020'
        }]
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_related_item_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = [
            {
                "itemTitle": "Some title",
                "itemISBN": ["978-3-16-148410-0"],
                "itemISSN": ["2049-3630"],
                "itemDOI": "10.1021/acs.jced.6b00139",
                "itemURL": "https://example.com",
                "itemYear": "2020",
                "itemVolume": "2",
                "itemIssue": "25",
                "itemEndPage": "30",
                "itemRelationType": {
                    "links": {
                        "self": 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/isversionof'
                    }
                }
            }
        ]
        field = "relatedItem"
        base_json[field] = content
        base_json_dereferenced[field] = [{
            'itemDOI': '10.1021/acs.jced.6b00139',
            'itemEndPage': '30',
            'itemISBN': ['978-3-16-148410-0'],
            'itemISSN': ['2049-3630'],
            'itemIssue': '25',
            'itemRelationType': [{
                'is_ancestor': False,
                'links': {
                    'self':
                        'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/isversionof'
                },
                'title': {
                    'cs': 'jeVerzí',
                    'en': 'isVersionOf'
                }
            }],
            'itemStartPage': '15',
            'itemTitle': "Some title",
            'itemURL': 'https://example.com',
            'itemVolume': '2',
            'itemYear': '2020'
        }]
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)

    def test_related_item_3(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = [
            {
                "itemTitle": "Some title",
                "itemISBN": ["978-3-16-148410-0"],
                "itemISSN": ["2049-3630"],
                "itemDOI": "10.1021/acs.jced.6b00139",
                "itemURL": "https://example.com",
                "itemYear": "2020",
                "itemVolume": "2",
                "itemIssue": "25",
                "itemRelationType": {
                    "links": {
                        "self": 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/isversionof'
                    }
                }
            }
        ]
        field = "relatedItem"
        base_json[field] = content
        base_json_dereferenced[field] = [{
            'itemDOI': '10.1021/acs.jced.6b00139',
            'itemEndPage': '30',
            'itemISBN': ['978-3-16-148410-0'],
            'itemISSN': ['2049-3630'],
            'itemIssue': '25',
            'itemRelationType': [{
                'is_ancestor': False,
                'links': {
                    'self':
                        'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/isversionof'
                },
                'title': {
                    'cs': 'jeVerzí',
                    'en': 'isVersionOf'
                }
            }],
            'itemStartPage': '15',
            "itemTitle": "Some title",
            'itemURL': 'https://example.com',
            'itemVolume': '2',
            'itemYear': '2020'
        }]
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)

    def test_related_item_4(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = [
            {
                "itemTitle": "Some title",
                "itemISBN": ["978-3-16-148410-0"],
                "itemISSN": ["2049-3630"],
                "itemDOI": "10.1021/acs.jced.6b00139",
                "itemURL": "https://example.com",
                "itemYear": "2020",
                "itemVolume": "2",
                "itemIssue": "25",
                "itemStartPage": "30",
                "itemEndPage": "15",
                "itemRelationType": {
                    "links": {
                        "self": 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/isversionof'
                    }
                }
            }
        ]
        field = "relatedItem"
        base_json[field] = content
        base_json_dereferenced[field] = [{
            'itemDOI': '10.1021/acs.jced.6b00139',
            'itemEndPage': '30',
            'itemISBN': ['978-3-16-148410-0'],
            'itemISSN': ['2049-3630'],
            'itemIssue': '25',
            'itemRelationType': [{
                'is_ancestor': False,
                'links': {
                    'self':
                        'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/isversionof'
                },
                'title': {
                    'cs': 'jeVerzí',
                    'en': 'isVersionOf'
                }
            }],
            'itemStartPage': '15',
            "itemTitle": "Some title",
            'itemURL': 'https://example.com',
            'itemVolume': '2',
            'itemYear': '2020'
        }]
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)


class TestRights:
    def test_rights_1(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = [
            {
                "links": {
                    "self": "http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/copyright"
                }
            }
        ]
        field = "rights"
        base_json[field] = content
        base_json_dereferenced[field] = [{
            'is_ancestor': False,
            'level': 1,
            'links': {
                'self':
                    'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/copyright'
            },
            'title': {
                'cs': 'Dílo je chráněno podle autorského zákona '
                      'č. '
                      '121/2000 Sb.',
                'en': 'This work is protected under the Copyright Act '
                      'No. 121/2000 Coll.'
            }
        }]
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced


class TestSeries:
    def test_series_1(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = [
            {
                "seriesTitle": "Titulek serie",
                "seriesVolume": "číslo serie"
            }
        ]
        field = "series"
        base_json[field] = content
        base_json_dereferenced[field] = [
            {
                "seriesTitle": "Titulek serie",
                "seriesVolume": "číslo serie"
            }
        ]
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced


class TestSubject:
    def test_subject_1(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        del base_json["keywords"]
        del base_json_dereferenced["keywords"]
        content = [
            {
                "links": {
                    "self": "http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/psh3001"
                }
            },
            {
                "links": {
                    "self": "http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/psh3000"
                }
            },
            {
                "links": {
                    "self": "http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/d010420"
                }
            }
        ]
        field = "subject"
        base_json[field] = content
        base_json_dereferenced[field] = [{
            'DateCreated': datetime(2007, 1, 26, 16, 14,
                                    37),
            'DateDateEstablished': '2007-01-26T16:14:37',
            'DateRevised': datetime(2007, 1, 26, 16, 14,
                                    37),
            'is_ancestor': False,
            'level': 1,
            'links': {
                'self':
                    'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/d010420'
            },
            'reletedURI': ['http://www.medvik.cz/link/D010420',
                           'http://id.nlm.nih.gov/mesh/D010420'],
            'title': {'cs': 'pentany', 'en': 'Pentanes'}
        },
            {
                'DateRevised': datetime(2007, 1, 26, 16, 14,
                                        37),
                'level': 1,
                'is_ancestor': False,
                'links': {
                    'self': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/psh3000'
                },
                'reletedURI': ['http://psh.techlib.cz/skos/PSH3000'],
                'title': {
                    'cs': 'turbulentní proudění',
                    'en': 'turbulent flow'
                }
            },
            {
                'DateRevised': datetime(2007, 1, 26, 16, 14,
                                        37),
                'level': 1,
                'is_ancestor': False,
                'links': {
                    'self': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/psh3001'
                },
                'reletedURI': ['http://psh.techlib.cz/skos/PSH3001'],
                'title': {
                    'cs': 'Reynoldsovo číslo', 'en': 'Reynolds number'
                }
            }]
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_subject_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        del base_json["keywords"]
        del base_json_dereferenced["keywords"]
        content = [
            {
                "links": {
                    "self": "http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/psh3001"
                }
            },
            {
                "links": {
                    "self": "http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/psh3000"
                }
            }
        ]
        field = "subject"
        base_json[field] = content
        base_json_dereferenced[field] = [{
            'DateCreated': datetime(2007, 1, 26, 16, 14,
                                    37),
            'DateDateEstablished': '2007-01-26T16:14:37',
            'DateRevised': datetime(2007, 1, 26, 16, 14,
                                    37),
            'is_ancestor': False,
            'links': {
                'self':
                    'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/d010420'
            },
            'reletedURI': ['http://www.medvik.cz/link/D010420',
                           'http://id.nlm.nih.gov/mesh/D010420'],
            'title': {'cs': 'pentany', 'en': 'Pentanes'}
        },
            {
                'DateRevised': datetime(2007, 1, 26, 16, 14,
                                        37),
                'is_ancestor': False,
                'links': {
                    'self': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/psh3000'
                },
                'reletedURI': ['http://psh.techlib.cz/skos/PSH3000'],
                'title': {
                    'cs': 'turbulentní proudění',
                    'en': 'turbulent flow'
                }
            }
        ]
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)


class TestKeywords:
    def test_keywords_1(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        del base_json["keywords"]
        del base_json_dereferenced["keywords"]
        content = []
        field = "keywords"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)

    def test_keywords_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        del base_json["keywords"]
        del base_json_dereferenced["keywords"]
        content = {"error": "Some error"}
        field = "keywords"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError, match="Some error"):
            schema.load(base_json)


class TestTitle:
    def test_title_1(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = [
            {
                "cs": "Titulek",
                "en": "Title"
            },
            {
                "cs": "Titulek2",
                "en": "Title2"
            },
        ]
        field = "title"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_title_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = {
            "cs": "Titulek",
            "en": "Title"
        }
        field = "title"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)


class TestTitleAlternate:
    def test_title_1(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = [
            {
                "cs": "Titulek",
                "en": "Title"
            },
            {
                "cs": "Titulek2",
                "en": "Title2"
            },
        ]
        field = "titleAlternate"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        result = schema.load(base_json)
        assert result == base_json_dereferenced

    def test_title_2(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = {
            "cs": "Titulek",
            "en": "Title"
        }
        field = "title"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            schema.load(base_json)


class TestRulesExceptions:
    def test_rules_exception_1(self, app, db, taxonomy_tree, base_json, base_json_dereferenced):
        content = [
            {
                "path": "/dc/subject",
                "element": "[{'en_US': [{'value': [None]}], 'cs_CZ': [{'value': [None]}]}]",
                "phase": "pre",
                "exception": "bla"
            }
        ]
        field = "rulesExceptions"
        base_json[field] = content
        base_json_dereferenced[field] = content
        schema = CommonMetadataSchemaV2()
        with pytest.raises(ValidationError):
            result = schema.load(base_json)
