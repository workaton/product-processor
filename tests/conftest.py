import json
from pathlib import Path
from typing import Callable, Sequence
from unittest.mock import Mock

from app.geolocation import ObsStationLocator
from ngitws.typing import JsonType
import pytest


SAMPLE_DIR = Path(__file__).resolve().parent.joinpath('fixtures', 'sample_files')


def compare_text(t1: str, t2: str) -> bool:
    """Compare two text strings.

    :return:
        True if a match
    """
    if not t1 and not t2:
        return True
    if t1 == '*' or t2 == '*':
        return True
    return (t1 or '').strip() == (t2 or '').strip()


def compare_xml(xml_tree_1, xml_tree_2, excludes: Sequence = None) -> bool:
    """Compare two xml etrees.

    :param xml_tree_1: the first tree
    :param xml_tree_2: the second tree
    :param excludes: list of string of attributes to exclude from comparison
    :return:
        True if both files match
    """
    if excludes is None:
        excludes = []

    if xml_tree_1.tag != xml_tree_2.tag:
        print('Tags do not match: %s and %s' % (xml_tree_1.tag, xml_tree_2.tag))
        return False
    for name, value in xml_tree_1.attrib.items():
        if name not in excludes:
            if xml_tree_2.attrib.get(name) != value:
                print('Attributes do not match: %s=%r, %s=%r'
                      % (name, value, name, xml_tree_2.attrib.get(name)))
                return False
    for name in xml_tree_2.attrib.keys():
        if name not in excludes:
            if name not in xml_tree_1.attrib:
                print('xml_tree_2 has an attribute xml_tree_1 is missing: %s'
                      % name)
                return False
    if not compare_text(xml_tree_1.text, xml_tree_2.text):
        print('text: %r != %r' % (xml_tree_1.text, xml_tree_2.text))
        return False
    if not compare_text(xml_tree_1.tail, xml_tree_2.tail):
        print('tail: %r != %r' % (xml_tree_1.tail, xml_tree_2.tail))
        return False
    cl1 = list(xml_tree_1)
    cl2 = list(xml_tree_2)
    if len(cl1) != len(cl2):
        print('children length differs, %i != %i'
              % (len(cl1), len(cl2)))
        return False
    i = 0
    for c1, c2 in zip(cl1, cl2):
        i += 1
        if c1.tag not in excludes:
            if not compare_xml(c1, c2, excludes):
                print('children %i do not match: %s'
                      % (i, c1.tag))
                return False
    return True


def get_sample_file_path(filename: str) -> Path:
    """Return a Path to the requested file."""
    path = SAMPLE_DIR.joinpath(filename)
    if not path.is_file():
        raise FileNotFoundError(f'The sample file {filename} was not found in {SAMPLE_DIR}')

    return path


def read_sample_binary_file(filename: str) -> bytes:
    """Return the contents of a binary file as a byte string."""
    with get_sample_file_path(filename).open('rb') as sample_file:
        return sample_file.read()


def read_sample_json_file(filename: str) -> JsonType:
    """Return the contents of a JSON file as a JsonType."""
    with get_sample_file_path(filename).open('r') as sample_file:
        return json.load(sample_file)


def read_sample_text_file(filename: str) -> str:
    """Return the contents of a text file as a unicode string."""
    with get_sample_file_path(filename).open('r') as sample_file:
        return sample_file.read()


@pytest.fixture
def obs_locator() -> ObsStationLocator:
    locator = Mock(ObsStationLocator)
    locator.get.return_value = 'Test Station||0.0 0.0 0'
    return locator


@pytest.fixture
def sample_binary_file() -> Callable[[str], bytes]:
    """Return a fixture function to load a binary file."""
    return read_sample_binary_file


@pytest.fixture
def sample_json_file() -> Callable[[str], JsonType]:
    """Return a fixture function to load a JSON file."""
    return read_sample_json_file


@pytest.fixture
def sample_text_file() -> Callable[[str], str]:
    """Return a fixture function to load a text file."""
    return read_sample_text_file
