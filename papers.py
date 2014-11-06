#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import re
import datetime
import json

def quarantine(individual, countries):
    """
    :param people:
    :param countries:
    :return: Boolean
    """
    coming_from = individual["from"]["country"]
    if len(countries[coming_from]["medical_advisory"]) > 0:
        return True

    if "via" in individual:
        coming_via = individual["via"]["country"]
        if len(countries[coming_via]["medical_advisory"]) > 0:
            return True

    return False

def entry_complete(individual):
    """
    :param individual:
    :return:
    """
    if "first_name" in individual:
        if len(individual["first_name"]) == 0:
            return False
    else:
        return False
    if "last_name" in individual:
        if len(individual["last_name"]) == 0:
            return False
    else:
        return False
    if "birth_date" in individual:
        if len(individual["birth_date"]) == 0:
            return False
    else:
        return False
    if "passport" in individual:
        if len(individual["passport"]) == 0:
            return False
    else:
        return False
    if "home" in individual:
        if len(individual["home"]['country']) == 0:
            return False
    else:
        return False
    if "from" in individual:
        if len(individual["from"]['country']) == 0:
            return False
    else:
        return False
    if "entry_reason" in individual:
        if len(individual["entry_reason"]) == 0:
            return False
    else:
        return False

def visitor_visa(individual, countries):
    """
    :param individual:
    :param countries:
    :return: False only if something is wrong. True, if everything is ok.
    """
    if individual["entry_reason"] == "visit":
        home_country = individual["home"]["country"]
        if countries[home_country]["visitor_visa_required"]:
            if "visa" in individual:
                visa_date = individual["visa"]["date"]
                visa_date = visa_date.split("-")
                visa_date = datetime.date(int(visa_date[0]), int(visa_date[1]), int(visa_date[2]))
                num_days = (datetime.date.today() - visa_date).days
                if num_days >= 365*2:
                    return False
            else:
                return False
    return True

def transit_visa(individual, countries):
    """
    :param individual:
    :param countries:
    :return: False only if something is wrong. True, if everything is ok.
    """
    if individual["entry_reason"] == "transit":
        home_country = individual["home"]["country"]
        if countries[home_country]["transit_visa_required"]:
            if "visa" in individual:
                visa_date = individual["visa"]["date"]
                visa_date = visa_date.split("-")
                visa_date = datetime.date(int(visa_date[0]), int(visa_date[1]), int(visa_date[2]))
                num_days = (datetime.date.today() - visa_date).days
                if num_days >= 365*2:
                    return False
            else:
                return False
    return True



def decide(input_file, watchlist_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains cases to decide
    :param watchlist_file: The name of a JSON formatted file that contains names and passport numbers on a watchlist
    :param countries_file: The name of a JSON formatted file that contains country data, such as whether
        an entry or transit visa is required, and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are: "Accept", "Reject", "Secondary", and "Quarantine"
    """
    with open(input_file) as file_reader:
        file_contents = file_reader.read()
        json_people = json.loads(file_contents)

    with open(watchlist_file) as file_reader:
        file_contents = file_reader.read()
        json_watchlist = json.loads(file_contents)

    with open(countries_file) as file_reader:
        file_contents = file_reader.read()
        json_countries = json.loads(file_contents)

        results = []
        for person in json_people:
            #     the quarantine function is called here.
            quarantine_status = quarantine(person,json_countries)
            #   the incomplete function is called here.
            entry_record_is_complete = entry_complete(person)
            #   the visitor visa functions is called here.
            valid_visitor_visa = visitor_visa(person, json_countries)
            #   the transit visa functions is called here.
            valid_transit_visa = transit_visa(person, json_countries)
            


    return ["Reject"]

decide("example_entries.json", "watchlist.json", "countries.json")

def valid_passport_format(passport_number):
    """
    Checks whether a pasport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_format = re.compile('.{5}-.{5}-.{5}-.{5}-.{5}')

    if passport_format.match(passport_number):
        return True
    else:
        return False


def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False
