odoo.define('custom_studio.reportNewComponentsRegistry', function (require) {
"use strict";

var core = require('web.core');
var Registry = require('web.Registry');
var reportNewComponents = require('custom_studio.reportNewComponents');

var _lt = core._lt;

var registry = new Registry();

registry
    .add(_lt('Block'), [
        reportNewComponents.BlockText,
        reportNewComponents.BlockField,
        reportNewComponents.BlockTitle,
        reportNewComponents.LabelledField,
        reportNewComponents.Image,
        reportNewComponents.BlockAddress,
    ])
    .add(_lt('Inline'), [
        reportNewComponents.InlineText,
        reportNewComponents.InlineField,
    ])
    .add(_lt('Table'), [
        reportNewComponents.BlockTable,
        reportNewComponents.TableColumnField,
        reportNewComponents.TableCellText,
        reportNewComponents.TableCellField,
        reportNewComponents.TableBlockTotal,
    ])
    .add(_lt('Column'), [
        reportNewComponents.ColumnHalfText,
        reportNewComponents.ColumnThirdText,
    ]);

return registry;

});
