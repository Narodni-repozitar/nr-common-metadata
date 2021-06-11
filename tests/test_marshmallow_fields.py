import pytest
from marshmallow import Schema, ValidationError

from nr_common.marshmallow.fields import NRDate, ISBN, ISSN, DOI, RIV, Year, OAI, \
    DateRange, DateString


# NRDate tests
@pytest.mark.parametrize("test_input,expected",
                         [("2019-12-31", "2019-12-31"), ("2019-12", "2019-12"), ("2019", "2019"),
                          ("2018-12-31 / 2019-12-31", "2018-12-31 / 2019-12-31"),
                          ("2018-12 / 2019-12", "2018-12 / 2019-12"),
                          ("p2019", "2019"), ("c2019", "2019"), ("cop2019", "2019"),
                          ("[2019]", "2019"), ("©2019", "2019"), ("℗2019", "2019"),
                          ("2018-2019", "2018 / 2019"), ("copyright2019", "2019"),
                          ("fonogram2019", "2019"), ("2018 - 2019", "2018 / 2019")
                          ])
def test_NRDate(test_input, expected):
    class TestSchema(Schema):
        date = NRDate(required=True)

    data = {
        "date": test_input
    }
    schema = TestSchema()
    res = schema.load(data)
    assert res["date"] == expected


def test_NRDate_2():
    class TestSchema(Schema):
        date = NRDate(required=True)

    data = {
        "date": "2019 2018 2020"
    }
    schema = TestSchema()
    with pytest.raises(ValidationError):
        res = schema.load(data)


def test_NRDate_3():
    class TestSchema(Schema):
        date = NRDate(required=True)

    data = {
        "date": "2021-07-08"
    }
    schema = TestSchema()
    with pytest.raises(ValidationError):
        res = schema.load(data)


# DateRange tests
@pytest.mark.parametrize("test_input,expected",
                         [("2019-12-31", "2019-12-31"),
                          ("2018-12-31 / 2019-12-31", "2018-12-31/2019-12-31"),
                          ("2018-12-31/2019-12-31", "2018-12-31/2019-12-31"),
                          ])
def test_DateRange(test_input, expected):
    class TestSchema(Schema):
        date = DateRange(required=True)

    data = {
        "date": test_input
    }
    schema = TestSchema()
    res = schema.load(data)
    assert res["date"] == expected


@pytest.mark.parametrize("test_input",
                         ["2019-12",
                          "2018.12.31 / 2019.12.31",
                          "2018-12/2019-12",
                          "2021-12-21"
                          ])
def test_DateRange_2(test_input):
    class TestSchema(Schema):
        date = DateRange(required=True)

    data = {
        "date": test_input
    }
    schema = TestSchema()
    with pytest.raises(ValidationError):
        schema.load(data)


# ISBN
@pytest.mark.parametrize("test_input,expected",
                         [
                             ("978-1-56619-909-4", "978-1-56619-909-4"),
                             ("9781566199094", "978-1-56619-909-4"),
                             ("1-56619-909-3", "1-56619-909-3"),
                             ("1566199093", "1-56619-909-3"),
                         ])
def test_ISBN(test_input, expected):
    class TestSchema(Schema):
        isbn = ISBN(required=True)

    data = {
        "isbn": test_input
    }
    schema = TestSchema()
    res = schema.load(data)
    assert res["isbn"] == expected


def test_ISBN_2():
    class TestSchema(Schema):
        isbn = ISBN(required=True)

    data = {
        "isbn": "978-1-56619-909-7"  # wrong control sum
    }
    schema = TestSchema()
    with pytest.raises(ValidationError):
        schema.load(data)


def test_ISBN_3():
    class TestSchema(Schema):
        isbn = ISBN(required=True)

    data = {
        "isbn": "978-1-56619-909-4 a 1-56619-909-3"
    }
    schema = TestSchema()
    with pytest.raises(ValidationError):
        schema.load(data)


# ISSN
@pytest.mark.parametrize("test_input,expected",
                         [
                             ("2049-3630", "2049-3630"),
                             ("20493630", "2049-3630"),
                         ])
def test_ISSN(test_input, expected):
    class TestSchema(Schema):
        issn = ISSN(required=True)

    data = {
        "issn": test_input
    }
    schema = TestSchema()
    res = schema.load(data)
    assert res["issn"] == expected


def test_ISSN_2():
    class TestSchema(Schema):
        issn = ISSN(required=True)

    data = {
        "issn": "2049-3631"
    }
    schema = TestSchema()
    with pytest.raises(ValidationError):
        schema.load(data)


def test_ISSN_3():
    class TestSchema(Schema):
        issn = ISSN(required=True)

    data = {
        "issn": "2049-36311"
    }
    schema = TestSchema()
    with pytest.raises(ValidationError):
        schema.load(data)


def test_ISSN_4():
    class TestSchema(Schema):
        issn = ISSN(required=True)

    data = {
        "issn": "2049a3631"
    }
    schema = TestSchema()
    with pytest.raises(ValidationError):
        schema.load(data)


# DOI
@pytest.mark.parametrize("test_input,expected",
                         [
                             ("10.1093/ajae/aaq063", "10.1093/ajae/aaq063"),
                             ("10.1371/journal.pgen.1001111", "10.1371/journal.pgen.1001111"),
                             ("http://dx.doi.org/10.1093/ajae/aaq063",
                              "http://dx.doi.org/10.1093/ajae/aaq063"),
                         ])
def test_DOI(test_input, expected):
    class TestSchema(Schema):
        doi = DOI(required=True)

    data = {
        "doi": test_input
    }
    schema = TestSchema()
    res = schema.load(data)
    assert res["doi"] == expected


def test_DOI_2():
    class TestSchema(Schema):
        doi = DOI(required=True)

    data = {
        "doi": "9.1371/journal.pgen.1001111"
    }
    schema = TestSchema()
    with pytest.raises(ValidationError):
        schema.load(data)


# RIV
@pytest.mark.parametrize("test_input,expected",
                         [
                             ("RIV/61389021:_____/94:52940054", "RIV/61389021:_____/94:52940054"),
                             ("RIV/46747885:24210/19:00006817", "RIV/46747885:24210/19:00006817"),
                             ("RIV/61384399:31130/11:00038804", "RIV/61384399:31130/11:00038804"),
                             ("RIV/60461373:22340/07:00019312", "RIV/60461373:22340/07:00019312"),
                             ("RIV/61989592:15410/17:73580861", "RIV/61989592:15410/17:73580861"),
                             ("RIV/60461373:22310/16:43902210", "RIV/60461373:22310/16:43902210"),
                         ])
def test_RIV(test_input, expected):
    class TestSchema(Schema):
        riv = RIV(required=True)

    data = {
        "riv": test_input
    }
    schema = TestSchema()
    res = schema.load(data)
    assert res["riv"] == expected


def test_RIV_2():
    class TestSchema(Schema):
        riv = RIV(required=True)

    data = {
        "riv": "RIV/60461373:22310/16:439022104"
    }
    schema = TestSchema()
    with pytest.raises(ValidationError):
        schema.load(data)


def test_RIV_3():
    class TestSchema(Schema):
        riv = RIV(required=True)

    data = {
        "riv": "RIV/60461373:22310/167:43902210"
    }
    schema = TestSchema()
    with pytest.raises(ValidationError):
        schema.load(data)


def test_RIV_4():
    class TestSchema(Schema):
        riv = RIV(required=True)

    data = {
        "riv": "60461373:22310/16:43902210"
    }
    schema = TestSchema()
    with pytest.raises(ValidationError):
        schema.load(data)


def test_RIV_5():
    class TestSchema(Schema):
        riv = RIV(required=True)

    data = {
        "riv": "RIV/6046137322310/16:43902210"
    }
    schema = TestSchema()
    with pytest.raises(ValidationError):
        schema.load(data)


def test_RIV_6():
    class TestSchema(Schema):
        riv = RIV(required=True)

    data = {
        "riv": "RIV/60461373:2231016:43902210"
    }
    schema = TestSchema()
    with pytest.raises(ValidationError):
        schema.load(data)


# YEAR
@pytest.mark.parametrize("test_input,expected",
                         [
                             ("1700", "1700"),
                             ("2020", "2020"),
                             ("1991", "1991"),
                             (" 1991 ", "1991"),
                             (1991, "1991"),
                         ])
def test_year(test_input, expected):
    class TestSchema(Schema):
        year = Year(required=True)

    data = {
        "year": test_input
    }
    schema = TestSchema()
    res = schema.load(data)
    assert res["year"] == expected


def test_year_2():
    class TestSchema(Schema):
        year = Year(required=True)

    data = {
        "year": "1699"
    }
    schema = TestSchema()
    with pytest.raises(ValidationError):
        schema.load(data)


def test_year_3():
    class TestSchema(Schema):
        year = Year(required=True)

    data = {
        "year": "2100"
    }
    schema = TestSchema()
    with pytest.raises(ValidationError):
        schema.load(data)


# DateString
@pytest.mark.parametrize("test_input,expected",
                         [
                             ("1700-01-01", "1700-01-01"),
                             ("2020-05-01", "2020-05-01"),
                             ("1991-07-01", "1991-07-01"),
                             (" 1991-07-01 ", "1991-07-01"),
                         ])
def test_date_string(test_input, expected):
    class TestSchema(Schema):
        date = DateString(required=True)

    data = {
        "date": test_input
    }
    schema = TestSchema()
    res = schema.load(data)
    assert res["date"] == expected


def test_date_string_2():
    class TestSchema(Schema):
        date = DateString(required=True)

    data = {
        "date": "1699-01-01"
    }
    schema = TestSchema()
    with pytest.raises(ValidationError):
        schema.load(data)


def test_date_string_3():
    class TestSchema(Schema):
        date = DateString(required=True)

    data = {
        "date": "2100-01-01"
    }
    schema = TestSchema()
    with pytest.raises(ValidationError):
        schema.load(data)


def test_date_string_4():
    class TestSchema(Schema):
        date = DateString(required=True)

    data = {
        "date": "1995"
    }
    schema = TestSchema()
    with pytest.raises(ValidationError):
        schema.load(data)


# OAI
@pytest.mark.parametrize("test_input,expected",
                         [
                             ("oai:arXiv.org:hep-th/9901001", "oai:arXiv.org:hep-th/9901001"),
                             ("oai:foo.org:some-local-id-53", "oai:foo.org:some-local-id-53"),
                             ("oai:FOO.ORG:some-local-id-53", "oai:FOO.ORG:some-local-id-53"),
                             ("oai:foo.org:some-local-id-54", "oai:foo.org:some-local-id-54"),
                             ("oai:foo.org:Some-Local-Id-54", "oai:foo.org:Some-Local-Id-54"),
                             ("oai:wibble.org:ab%20cd", "oai:wibble.org:ab%20cd"),
                             ("oai:wibble.org:ab?cd", "oai:wibble.org:ab?cd"),
                         ])
def test_oai(test_input, expected):
    class TestSchema(Schema):
        oai = OAI(required=True)

    data = {
        "oai": test_input
    }
    schema = TestSchema()
    res = schema.load(data)
    assert res["oai"] == expected


@pytest.mark.parametrize("test_input",
                         [
                             "something:arXiv.org:hep-th/9901001",
                             "oai:999:abc123",
                             "oai:wibble:abc123",
                             # "oai:wibble.org:ab cd",
                             # "oai:wibble.org:ab#cd",
                             # "oai:wibble.org:ab<cd",
                         ])
def test_oai_2(test_input):
    class TestSchema(Schema):
        oai = OAI(required=True)

    data = {
        "oai": test_input
    }
    schema = TestSchema()
    with pytest.raises(ValidationError):
        schema.load(data)
