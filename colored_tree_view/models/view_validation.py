# -*- coding: utf-8 -*-
import logging
import os

from odoo import tools
from lxml import etree

_logger = logging.getLogger(__name__)

_view_validators_cache = {}


def get_tree_view_validator():
    """ Return a validator for the tree views, or None. """
    if 'tree' not in _view_validators_cache:
        with tools.file_open(os.path.join('colored_tree_view', 'rng', 'tree_view.rng')) as f_rng:
            try:
                relax_ng_doc = etree.parse(f_rng)
                _view_validators_cache['tree'] = etree.RelaxNG(relax_ng_doc)
            except Exception as ex:
                _logger.exception(f'Failed to load RelaxNG XML schema for tree views validation {ex}')
                _view_validators_cache['tree'] = None

    return _view_validators_cache['tree']


def is_valid_tree_view(arch):
    validator = get_tree_view_validator()
    if validator and not validator.validate(arch):
        result = True
        for error in validator.error_log:
            _logger.error(tools.ustr(error))
            result = False
        return result
    return True
