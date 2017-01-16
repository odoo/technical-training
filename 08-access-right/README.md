# Access Rights

## Goal

The goal of this module is to learn how to handle security restrictions. The
learner will be able to

* restrict the access to specific model, data, fields
* hide part of the views or menus
* run priviledge code

## Requirements

* [Models, Fields and Relations](../01-models)
* [Basic Views](../03-views)

## Problem 1: Trust No One

The paranoid king sees ennemies everywhere wanting to steal his crown.
He keeps much information about the state of the realm (economy, army, citizen)
and while it needs to share some with his advisors, he does not want once to
have too much knowledge that could be a threat to his throne.

Consider who should be able to access and/or modify which information and add
some restrictions on different levels.


## Resources

### Reference

* [Security in Odoo](https://www.odoo.com/documentation/10.0/reference/security.html)
* [View attribute `group`](https://www.odoo.com/documentation/10.0/reference/views.html)

### Code Sample

* [Model restrictions](https://github.com/odoo/odoo/blob/8033467be6062e46e81d9250a0be2162d5c13cc9/addons/crm/security/ir.model.access.csv)
* [Record restrictions](https://github.com/odoo/odoo/blob/8033467be6062e46e81d9250a0be2162d5c13cc9/addons/crm/security/crm_security.xml#L27)
* [Field restrictions](https://github.com/odoo/odoo/blob/8033467be6062e46e81d9250a0be2162d5c13cc9/addons/base_gengo/models/res_company.py#L10)
* [View restrictions](https://github.com/odoo/odoo/blob/8033467be6062e46e81d9250a0be2162d5c13cc9/addons/account/views/account_invoice_view.xml#L45)
