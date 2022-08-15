odoo.define('colored_tree_view.ListRenderer', function (require) {
    "use strict"

    let ListRenderer = require('web.ListRenderer');

    let BACKGROUNDS = [
        'background-carmine',
        'background-ghost',
        'background-seed',
        'background-soil',
        'background-olive',
    ]

    ListRenderer.include({
        init: function (parent, state, params) {
            this._super.apply(this, arguments);
            this.rowBackgrounds = _.chain(this.arch.attrs)
                .pick(function (value, key) {
                    return BACKGROUNDS.indexOf(key) >= 0;
                }).mapObject(function (value) {
                    return py.parse(py.tokenize(value));
                }).value();
        },

        /**
         * @override
         * Override to add a style to the row according to a few rules.
         *
         * @private
         * @param {Object} record
         * @returns {jQueryElement} a <tr> element
         */
        _renderRow: function (record) {
            let $tr = this._super.apply(this, arguments);
            this._setBackgroundClasses(record, $tr);
            return $tr;
        },

        /**
         * Each line can be styled according to a few simple rules. The arch
         * description of the list may have one of the background-X attribute with
         * a domain as value.  Then, for each record, we check if the domain matches
         * the record, and add the background-X css class to the element.  This method is
         * concerned with the computation of the list of css classes for a given
         * record.
         *
         * @private
         * @param {Object} record a basic model record
         * @param {jQueryElement} $tr a jquery <tr> element (the row to add decoration)
         */
        _setBackgroundClasses: function (record, $tr) {
            _.each(this.rowBackgrounds, function (expr, backgroundClass) {
                $tr.toggleClass(backgroundClass, py.PY_isTrue(py.evaluate(expr, record.evalContext)));
            });
        },
    });
});