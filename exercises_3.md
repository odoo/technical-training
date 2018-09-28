![Odoo Logo](https://odoocdn.com/openerp_website/static/src/img/assets/png/odoo_logo_small.png)

# Odoo JS - Module 3 - Creating a new view

## Content

- [Introduction](#introduction)
- Tasks
    - [3.1 Hello world view](#31-hello-world-view)
    - [3.2 Fetching data](#32-fetching-data)
    - [3.3 Use an external library (leaflet)](#33-use-an-external-library-leaflet)
    - [3.4.1 Connect renderer with proper data](#341-connect-renderer-with-proper-data)
    - [3.4.2 Render the template (hard)](#342-render-the-template-hard)
    - [3.5 Make sure data is synchronized with search view](#35-make-sure-data-is-synchronized-with-search-view)
    - [3.6 Switch to the form view when clicking on marker](#36-switch-to-the-form-view-when-clicking-on-marker)
    - [3.7 Implement custom control panel buttons](#37-implement-custom-control-panel-buttons)

## Introduction

The tasks in this module are sequentially dependant. The goal of this module is
to learn how to create a new view, from scratch (but with an external library
to fetch and display maps!).

The marketing department wants to be able to look at the customer data,
displayed on a map view, to be able to better target them. So, we will create a
new view type.

The `arch` field should look like this:

```xml
    <awesome_map latitude="some_field" longitude="some_other_field">
      <field name="field1"/>
      <field name="field2"/>
      <template>
        <t t-name="map-popup">
          <div>... <t t-esc="record.field1"/>
          </div>
        </t>
      </template>
    </awesome_map>
```

In this code, the latitude and longitude attributes should describe a float field.
The template tag is a small qweb template, which should be rendered on a marker
at the corresponding record location.  The field tags determine which fields
should be fetched.

We will use the [Leaflet library](https://leafletjs.com/).

## 3.1 Hello world view

#### Goals

- understand how to add a new view type in python
- understand initial plumbing for a view
- use view registry

#### Task Description

- start with the initial code from `awesome_map`
- install the `awesome_map` module
- read it and understand what each file is doing
- select an icon to display in the view switcher for the map view
- modify the renderer to display a message 'hello world'

#### Resources

* [View architecture](https://www.odoo.com/documentation/12.0/reference/javascript_reference.html#views)
* [Creating a new view from scratch](https://www.odoo.com/documentation/12.0/reference/javascript_cheatsheet.html#creating-a-new-view-from-scratch)


## 3.2 Fetching data

#### Goals

- work with the `AbstractModel` api
- fetch data
- understand `AbstractView` api

#### Task Description

We need data to display! We need to load data in the MapModel.

- first, geolocalize a few customers
- parse arch in the MapView class, extract latitude and longitude fields and
  give them to the model
- load data for the current `context/domain/groupby`, read latitude/longitude
  and other fields
- display in the renderer a JSON.stringified version of the data loaded by the
  model, to check that the data is properly transmitted to the renderer.

#### Resources

* [`AbstractModel` API](https://github.com/odoo/odoo/blob/57decbbed6d3d8899b09a58361ae9b30d39a9c03/addons/web/static/src/js/views/abstract_model.js)


## 3.3 Use an external library (leaflet)

#### Goals

- start integrating a library
- lazy load assets
- understand main entry point of `AbstractRenderer`

#### Task Description

- add `Leaflet` css/js assets to the dependency handling of the `MapView` (lazy
  loading)
- implement a basic render method in the `renderer`, which displays a map view.

#### Resources

- [Leaflet library](https://leafletjs.com/)
- [AbstractRenderer](https://github.com/odoo/odoo/blob/57decbbed6d3d8899b09a58361ae9b30d39a9c03/addons/web/static/src/js/views/abstract_renderer.js)
- [AbstractRenderer on_attach_callback hook](https://github.com/odoo/odoo/blob/57decbbed6d3d8899b09a58361ae9b30d39a9c03/addons/web/static/src/js/views/abstract_renderer.js#L42)


## 3.4.1 Connect renderer with proper data

#### Goals

- display current data in the map view

#### Task Description

- Use the `Leaflet` API to add markers to each data point currently loaded


## 3.4.2 Render the template (hard)

#### Goals

- render record information for each data point in the map

#### Task Description

- render the proper template for each data point in a popup

Note: you'll have to create your own `Qweb` instance to render the template. You
can use the `KanbanRenderer` as an example.

#### Resources

- [`KanbanRenderer` - qweb instance](https://github.com/odoo/odoo/blob/57decbbed6d3d8899b09a58361ae9b30d39a9c03/addons/web/static/src/js/views/kanban/kanban_renderer.js#L106)


## 3.5 Make sure data is synchronized with search view

#### Goals

- understand the flow of control with search view
- understand main entry points in AbstractController (update)

#### Task Description

- change the search view and see that the map view is not updated
- make it work, by implementing the proper method

#### Resources

- [`AbstractController` API](https://github.com/odoo/odoo/blob/57decbbed6d3d8899b09a58361ae9b30d39a9c03/addons/web/static/src/js/views/abstract_controller.js)


## 3.6 Switch to the form view when clicking on marker

#### Goals

- learn how to switch to a form view for a specific record id

#### Task Description

- add an event handler in the proper place
- when clicking on a pin, it should switch to a form view


## 3.7 Implement custom control panel buttons

#### Goals

- add buttons to the control panel

#### Task Description

- add two custom buttons in the control panel, clicking on them should zoom in
  or out of the map view


