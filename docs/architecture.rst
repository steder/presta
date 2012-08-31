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

System Diagram
===================================

digraph {
  server1 -> server2
}
