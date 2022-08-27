# -*- coding: utf-8 -*-

import collections
import logging

from odoo import models, api
from odoo.exceptions import ValidationError
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
            has_to_raise_validation = True
            for view in self:
                if view.type != 'tree':
                    continue

                has_to_raise_validation = False

                view_arch = etree.fromstring(view.arch.encode('utf-8'))
                view._valid_inheritance(view_arch)
                view_def = view.read_combined(['arch'])
                view_arch_utf8 = view_def['arch']
                view_doc = etree.fromstring(view_arch_utf8)
                self._check_groups_validity(view_doc, view.name)
                # verify that all fields used are valid, etc.
                try:
                    self.postprocess_and_fields(view.model, view_doc, view.id)
                except ValueError as e:
                    raise ValidationError("%s\n\n%s" % (_("Error while validating view"), tools.ustr(e)))

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

            if has_to_raise_validation:
                raise ex
