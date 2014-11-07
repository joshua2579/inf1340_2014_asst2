#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import pytest
from papers import decide


def test_basic():
    assert decide("test_returning_citizen.json", "watchlist.json", "countries.json") == ["Accept", "Accept"]
    assert decide("test_watchlist.json", "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_quarantine.json", "watchlist.json", "countries.json") == ["Quarantine"]


def test_files():
    with pytest.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "", "countries.json")
    with pytest.raises(FileNotFoundError):
        decide("", "watchlist.json", "countries.json")
    with pytest.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "watchlist.json", "")

def test_missing_entry():
    assert decide("test_missing_fname.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_missing_lname.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_missing_bdate.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_missing_homec.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_missing_fromc.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_missing_passport.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_missing_entry_reason.json", "watchlist.json", "countries.json") == ["Reject"]

def test_empty_entry():
    assert decide("test_empty_fname.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_empty_lname.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_empty_bdate.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_empty_homec.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_empty_fromc.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_empty_passport.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_empty_entry_reason.json", "watchlist.json", "countries.json") == ["Reject"]


# add functions for other tests

