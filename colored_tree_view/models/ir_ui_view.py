# -*- coding: utf-8 -*-

import collections
import logging

from odoo import models, api
from lxml import etree
from .view_validation import is_valid_tree_view

_logger = logging.getLogger(__name__)

_validators = collections.defaultdict(list)


class View(models.Model):
    _inherit = 'ir.ui.view'

    # Edit base methods
    #
    @api.constrains('arch_db')
    def _check_xml(self):
        try:
            super(View, self)._check_xml()
        except Exception as ex:
            should_raise_validation = True
            for view in self:
                try:
                    if view.type != 'tree':
                        continue

                    should_raise_validation = False

                    view_arch = etree.fromstring(view.arch.encode('utf-8'))
                    view._valid_inheritance(view_arch)
                    view_def = view.read_combined(['arch'])
                    view_arch_utf8 = view_def['arch']
                    view_doc = etree.fromstring(view_arch_utf8)
                    # verify that all fields used are valid, etc.
                    view.postprocess_and_fields(view_doc, validate=True)
                    # RNG-based validation is not possible anymore with 7.0 forms
                    view_docs = [view_doc]
                    if view_docs[0].tag == 'data':
                        # A <data> element is a wrapper for multiple root nodes
                        view_docs = view_docs[0]

                    for view_arch in view_docs:
                        if view_arch.tag != 'tree':
                            continue

                        check = is_valid_tree_view(view_arch)
                        if not check:
                            raise ex
                except ValueError:
                    raise ex
            else:
                raise ex
