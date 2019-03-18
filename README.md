# Odoo 12.0 - Technical Training
=======
# Access Rights

## Goal

The goal of this module is to learn how to handle security restrictions. The
learner will be able to

* restrict the access to specific model, data, fields
* hide part of the views or menus
* run priviledge code

## Requirements

* [Models, Fields and Relations](https://github.com/odoo/technical-training/tree/12.0-01-models)
* [Basic Views](https://github.com/odoo/technical-training/tree/12.0-03-views)


## Problem 1: Citadel (openacademy)

The future maesters before getting any chains will require to pass a lot of classes, as they can register to session on their own, they must be able to access the information about the course and session. They can access the information about the maesters as well but the citadel. The citadel has drastic rules about students accessing information about other students. A long time ago, the maesters sent a student to the wall as an example after accessing information about a southern student. This includes who attends which session.

The archmaesters creates the courses and assign the maester responsible. The maesters can manage only their courses and like every assignment of every maester in Westeros, they cannot unassign themself from the course. Some older students can supervise some session for some maesters. Obviously the students just obey and apply but the maesters can modify the session.

## Problem 2: Trust No One

The paranoid king sees ennemies everywhere wanting to steal his crown.
He keeps much information about the state of the realm (economy, army, citizen)
and while it needs to share some with his advisors, he does not want once to
have too much knowledge that could be a threat to his throne.

Consider who should be able to access and/or modify which information and add
some restrictions on different levels.

## Resources

### Reference

* [Security in Odoo](https://www.odoo.com/documentation/12.0/reference/security.html)
* [View attribute `group`](https://www.odoo.com/documentation/12.0/reference/views.html)

### Code Sample

* [Model restrictions](https://github.com/odoo/odoo/blob/8033467be6062e46e81d9250a0be2162d5c13cc9/addons/crm/security/ir.model.access.csv)
* [Record restrictions](https://github.com/odoo/odoo/blob/8033467be6062e46e81d9250a0be2162d5c13cc9/addons/crm/security/crm_security.xml#L27)
* [Other record restrictions](https://github.com/odoo/odoo/blob/10.0/addons/sales_team/security/sales_team_security.xml#L36)
* [Field restrictions](https://github.com/odoo/odoo/blob/8033467be6062e46e81d9250a0be2162d5c13cc9/addons/base_gengo/models/res_company.py#L10)
* [View restrictions](https://github.com/odoo/odoo/blob/8033467be6062e46e81d9250a0be2162d5c13cc9/addons/account/views/account_invoice_view.xml#L45)
