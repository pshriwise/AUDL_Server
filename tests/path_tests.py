#!/usr/bin/python 


import AUDLclasses
import path_data
import unittest

def test_empty():

    path = "" 

    result = path_data.path_parse(path)

    assert ( None != result), "None was returned from parse_path"
    assert ('' ==  result), "Expected an empty string. Instead path_parse returned %s" % result


def test_triple_path():

    path = "teams/224002/game"
  
    result = path_data.path_parse(path)

    assert ( None != result), "None was returned from parse_path"
    assert len(result) == 3, "Expected a list of length three. Instead list is length %i" % len(result)


def test_invalid_path_direction():

    path_ents = ["Gibberish"]

    result = path_data.direct_path(path_ents)

    assert ''  == result, "Path data did not return empty string as expected. Instead it returned %s" % result
