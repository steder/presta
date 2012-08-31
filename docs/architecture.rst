.. Attempts to describe the design of Presta

Architecture
--------------------------------------

Goal
===============================

The goal of Presta is to act a hub for all sorts of data flowing within a business and its partners.

Specifically, Presta listens for events occurring throughout your business and reacts to those
events by running one or more jobs to update data in internal and partner systems.  Typically jobs
do not have real time requirements (no user is waiting for a response) but are instead batch processes
that run and complete asynchronously.

Examples of the kinds of data flow we're attempting to handle include:

 - synchronization of product catalog and inventory between an internal catalog and a 3rd party catalog (`Amazon MWS`_)
 - periodic report generation (payments, returns)
 - updating a search index
 - pushing orders to manufacturing partners
 - periodically polling third parties for order status (shipping information, tracking numbers)

_`Amazon MWS`: https://developer.amazonservices.com

Flow Diagram
===================================

The following diagram shows some potential data flows through and around Presta.

.. graphviz::

  digraph presta_flow {
    "threadless-python" -> "presta" [label="user profile change"];
     "presta" -> "presta (periodic)";
     "presta" -> "cafepress" [label="send orders"];
     "presta" -> "cafepress" [label="retrieve shipment info"];
     "presta" -> "uncommon" [label="send orders"];
     "presta" -> "uncommon" [label="retrieve shipment info"];
     "presta-periodic" -> "amazon-mws" [label="retrieve reports: settlement, returns, orders"];
     "presta-periodic" -> "nextopia" [label="update site search index"];
     "threadless-php" -> "presta" [label="stock level change"];
     "threadless-php" -> "presta" -> "amazon-mws" [label="new product"];
     "threadless-php" -> "presta" -> "amazon-mws" [label="product price change"];
  }

System Diagram
===================================

.. graphviz::

  digraph presta_systems {
    "threadless-php" -> "presta-api" [label="catalog event"];
    "threadless-python" -> "presta-api" [label="community event"];
    "presta-api" -> "mongodb" [label="retrieve job results"];
    "presta-api" -> "rabbitmq" [label="submit job to queue"]
    "presta-periodic" -> "rabbitmq" [label="submit scheduled job to queue"];
    "rabbitmq" -> "celeryd";
    "celeryd" -> "celery-worker-1" [label="dispatch to workers"];
    "celery-worker-1" -> "mongodb" [label="store job results"];
    "celeryd" -> "celery-worker-2" -> "mongodb";
    "celery-worker-2" -> "Partner Systems";
    "threadless-api" -> "presta-api" [label="retrieve data for external use"];
  }
