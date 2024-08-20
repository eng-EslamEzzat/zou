try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from flask import make_response
from slugify import slugify


def build_xml_response(xml_content, file_name="export"):
    """
    Construct a Flask response that returns content of a csv a file.
    """
    file_name = build_xml_file_name(file_name)
    response_body = xml_content
    xml_response = make_response(response_body)
    xml_response = build_xml_headers(xml_response, file_name)

    return xml_response


def build_xml_file_name(file_name):
    """
    Add application name as prefix of the file name.
    """
    return "kitsu_%s" % slugify(file_name, separator="_")


def build_xml_headers(xml_response, file_name):
    """
    Build HTTP response headers needed to return CSV content as a file.
    """
    xml_response.headers["Content-Disposition"] = (
        "attachment; filename=%s.xml" % file_name
    )
    xml_response.headers["Content-type"] = "application/xml"
    return xml_response
