#!/usr/bin/env python

__author__ = "Massimo Iannuzzi"
__copyright__ = "Copyright 2021 Walgreen Co."
__maintainer__ = "DBA TEAM"
__email__ = ""

# Application messages
# PARSE EXCEPTION
ERROR_PARAMETER_NOT_FOUND = lambda message: "Missing parameter {}".format(message)
ERROR_FILE_NOT_FOUND = lambda message: "File {} not found".format(message)
ERROR_FILE_NAME_INVALID = lambda message: "Invalid json file name :{}".format(message)
ERROR_FILE_NAME_WRONG = "The name of the json file must not start with numbers and must not contain one of the characters '-$&!#.\n Rename the file and import it again."

