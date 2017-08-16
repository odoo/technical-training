# Odoo 10.0 - Technical Training

This repository contains training material for learning Odoo 10. The training is divided in modules of roughly half a day. It will follow a problem-based learning approach. The learnees will handle ill-structured problems supervised framed by a teacher. That means that each problem has multiple solutions and therefore is not constrained to a single topic. Each module focuses on a given topic but with a similar approach.

Each module provides some reference material, and proposes problems for the learnees to solve on the topic at hand.
It is therefore a hands-on, practical approach to the development of Odoo modules. Each module is independent with requirement depending on skills and knowledge that may be learned from previous modules. The problems proposed in those modules have an existing starting situation but that are contextualised around a couple of [use cases](docs/use-case.md).

## Organisation

We consciously decided to give a training that will have "less content" with a better learning experience which is to lead the learnees to autonomy in their work with Odoo and acquire long term skills. "*True learning is based on discovery guided by mentoring rather than the transmission of knowledge*" (John Dewey). The problem-based approach we chose requires the learnees to first start with a problem without pregiven theory to create a better craddle for new skills to be learned. The teacher will be there to coach and guide the learnee through that process without forcing it. Emphasis will be put on interaction with other learnee as they solve the problems. 

### Practical details

* The work will be done with a virtual machine that can be run with [Virtual Box](https://www.virtualbox.org/). The virtual to be ran can be downloaded here for the [technical training](http://download.odoo.com/internal/VM-techtraining.zip) and the [Odoo System Administration](http://download.odoo.com/internal/sysadmin-training-vms.zip) respectively.
* Per module, which takes around half a day, groups of 2 will be created to solve the problem (2 persons per computer). The groups will be switched after every single module. Not all problem per module have to be solved (it varies on the level of the given group).
* At the end of a module, debriefing session will be given based on the questions and solutions that came from the process of solving the problems. The learnees will have to verbalize what they have learned with interaction with the rest of the group and feedback from the teacher.
* In addition to the modules, the learnees will be required to provide 2 questions in the morning about Odoo based on the previous day for discussion in the morning as a way of putting everyone back in the right state ready to attack the next modules.

#### [Introduction presentation](https://docs.google.com/a/odoo.com/presentation/d/1O2hd-jNtZN93-hhi_KFKgRVw90Yfdow6Su7YHF6oc_s/edit?usp=sharing)

## Base Requirements

This training uses Git for its repository, and Github as its platform.
Start with module [Git and Github](00-git) if you never used them.

The language [Python](https://www.python.org/) is a requirement for almost all modules.


## Modules

1. [Models, Fields and Relations](01-models)
1. [Computed Fields, Onchange and Constraints](02-fields)
1. [Basic Views](03-views)
1. [Model Inheritance](04-model-inheritance)
1. [View Inheritance](05-view-inheritance)
1. [Business Flow](06-business-flow)
1. [Access Rights](08-access-right)
1. [Play with the ORM](09-orm)
1. [Reports](10-reports)


## Advanced Modules

1. [Mail Integration](25-mail-integration)
1. [Kanban Views and Dashboards](26-kanban-dashboard)
1. [Advanced Widgets](27-widgets)
1. [Modify Business Flows](19-modify-business-flow)


## Odoo System Administration

* [Training Material](99-sysadmin)
