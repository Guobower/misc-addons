# -*- coding: utf-8 -*-
# Copyright 2017-2018 Naglis Jonaitis
# License AGPL-3 or later (https://www.gnu.org/licenses/agpl).


class OpenProjectConnectorError(Exception):
    '''Base class for exceptions raised in OpenProject Connector module.'''


class OpenProjectAPIError(OpenProjectConnectorError):
    '''Base exception for errors received from the OpenProject API.'''


class OpenProjectAPIPermissionError(OpenProjectAPIError):
    '''
    Exception which is raised in case of insufficient permissions for the
    OpenProject sync user.
    '''


class OpenProjectWebhookDataError(OpenProjectConnectorError):
    '''Raised in case OpenProject webhook event data in invalid.'''
