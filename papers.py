#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = 'Joshua Liben and Kristina Mitova'

# imports one per line
import re
import datetime
import json


def valid_passport_format(passport_number):
    """
    Checks whether a passport number is five sets of five alpha-number characters separated by dashes
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


def valid_formats(individual):
    """
    Checks whether certain entry formats are valid.

    :param individual: The name of the JSON object for one individual person.
    :return: Whether the formats are valid.
    """
    return valid_passport_format(individual["passport"]) and \
        (valid_date_format(individual["birth_date"]))


def quarantine(individual, countries):
    """
    Checks whether a person needs to be quarantined.

    :param individual: The name of the JSON object for one individual person.
    :param countries: The name of the JSON object containing a list of countries.
    :return: A boolean indicating whether a person needs to be quarantined.
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
    Checks whether an entry has all required items.

    :param individual: The name of the JSON object for one individual person.
    :return: A boolean indicating whether all required entries are present.
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
        elif not valid_date_format(individual["birth_date"]):
            raise ValueError("Birthdate is incorrect format.")
    else:
        return False
    if "passport" in individual:
        if len(individual["passport"]) == 0:
            return False
    else:
        return False
    if "home" in individual:
        if "country" in individual["home"]:
            if len(individual["home"]['country']) == 0:
                return False
        else:
            return False
    else:
        return False
    if "from" in individual:
        if "country" in individual["from"]:
            if len(individual["from"]['country']) == 0:
                return False
        else:
            return False
    else:
        return False
    if "entry_reason" in individual:
        if len(individual["entry_reason"]) == 0:
            return False
    else:
        return False
    return True


def check_visa(individual, countries, visa_type):
    """
    Checks whether a visa is valid.

    :param individual: The name of the JSON object for one individual person.
    :param countries: The name of the JSON object containing a list of countries.
    :param visa_type: A string indicating whether the visa is visit or transit.
    :return: A boolean indicating whether the visa is valid or not.
    """

    if individual["entry_reason"].lower() == visa_type:
        home_country = individual["home"]["country"]
        if countries[home_country]["visitor_visa_required"] == "1":
            if "visa" in individual:
                if "date" in individual["visa"]:
                    if valid_date_format(individual["visa"]["date"]):
                        # Parse date into list of 3 strings for Year, Month, Day.
                        visa_date = individual["visa"]["date"].split("-")
                        # Convert list of strings into date object.
                        visa_date = datetime.date(int(visa_date[0]),
                                                  int(visa_date[1]), int(visa_date[2]))
                        # Compare number of days between the visa date and today.
                        num_days = (datetime.date.today() - visa_date).days
                        if num_days >= 365*2:
                            return False
                    else:
                        raise ValueError("Date is not in Correct format")
                else:
                    return False
            else:
                return False
    return True


def check_watchlist(individual, watchlist):
    """
    Checks to see is someone is on the watchlist.

    :param individual: The name of the JSON object for one individual person.
    :param watchlist: The name of the JSON object for a watchlist
    :return: Whether the person is in the watchlist.
    """
    first_name = individual["first_name"].lower()
    last_name = individual["last_name"].lower()
    passport_number = individual["passport"].lower()

    for person in watchlist:
        if first_name == person["first_name"].lower() and \
                last_name == person["last_name"].lower():
            return True
        if passport_number == person["passport"].lower():
            return True
    return False


def check_returning_traveller(individual):
    """
    Checks if a person has the home country KAN returning to Kanadia.

    :param individual: The name of the JSON object for one individual person.
    :return:  A boolean indicating whether a person has the
    home country KAN returning to Kan.
    """
    return individual["entry_reason"].lower() == "returning" and\
        individual["home"]["country"].lower() == "kan"


def decide(input_file, watchlist_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains cases to decide
    :param watchlist_file: The name of a JSON formatted file that contains names and passport numbers on a watchlist
    :param countries_file: The name of a JSON formatted file that contains country data, such as whether
        an entry or transit visa is required, and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are: "Accept", "Reject", "Secondary", and "Quarantine"
    """

    try:
        with open(input_file) as file_reader:
            file_contents = file_reader.read()
            json_people = json.loads(file_contents)
    except FileNotFoundError:
        raise FileNotFoundError("Cannot find file: " + input_file)

    try:
        with open(watchlist_file) as file_reader:
            file_contents = file_reader.read()
            json_watchlist = json.loads(file_contents)
    except FileNotFoundError:
        raise FileNotFoundError("Cannot find file: " + watchlist_file)

    try:
        with open(countries_file) as file_reader:
            file_contents = file_reader.read()
            json_countries = json.loads(file_contents)
    except FileNotFoundError:
        raise FileNotFoundError("Cannot find file: " + countries_file)

    results = []
    for person in json_people:
        if entry_complete(person) and valid_formats(person):
            quarantined = quarantine(person, json_countries)
            valid_visitor_visa = check_visa(person, json_countries, "visit")
            valid_transit_visa = check_visa(person, json_countries, "transit")
            on_watchlist = check_watchlist(person, json_watchlist)
            returning_traveller = check_returning_traveller(person)

            if quarantined:
                results.append("Quarantine")
            elif not valid_transit_visa or \
                    not valid_visitor_visa:
                results.append("Reject")
            elif on_watchlist:
                results.append("Secondary")
            elif returning_traveller:
                results.append("Accept")
            else:
                results.append("Accept")
        else:
            results.append("Reject")
    return results