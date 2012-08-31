.. Just another readme...

Presta
----------------------------------

About
==================================

The Presta valve is a (sometimes Threadless) valve commonly found in high pressure road style bicycle inner tubes.

The Presta project is a service for collecting and controlling the flow of data between multiple partners under high pressure.

Development Setup
=================================

There's a single script that we'll attempt [*]_ to get you setup::

  $ ./bin/mise_en_place

Of course if the above script breaks you get to keep both pieces.

In the somewhat likely event of breakage you might try doing things
manually this way::

  $ brew install graphviz # only needed for documentation
  $ brew install mongodb
  $ brew install rabbitmq

Of course you may need to specify your package manager of choice.

I'll include the full set of ubuntu packages here as soon as I get a
chance to test things out on ubuntu.

Next you'll need some ruby and python things.

The ruby tools we're interested in are just bundler and foreman.

Assuming you can run ``gem`` without ``sudo`` you'll be able to just
do::

  $ gem install bundler
  $ bundle install

Next up we'll install our Python packages (Again we're assuming you
have the ability to run ``pip`` without ``sudo``)::

  $ pip install --requirements requirements_dev.txt

Last but not least you'll want to go ahead and configure RabbitMQ::

  $ rabbitmq-server -detach
  $ rabbitmqctl add_user myuser mypassword
  $ rabbitmqctl add_vhost myvhost
  $ rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"
  $ rabbitmqctl stop

After all this monkeying around you should finally be ready to start
everything up::

  $ foreman start

Documentation
=================================

Generate and view the documentation by doing::

  $ cd docs
  $ make html
  $ open build/index.html

.. [*] The script has only been tested on Mac OS X 10.7.4 with Xcode
       4.3 and Homebrew.  At a pair minimum I'd like the script to
       work on Ubuntu as well.  Adding an Ubuntu, MacPorts and/or a Fink version
       should be pretty easy.  Add another package manager, find the
       package names for that pm, maybe tweak the gem/pip commands to
       use sudo and that should be it.
