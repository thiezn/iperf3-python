.. iperf3 documentation master file, created by
   sphinx-quickstart on Tue Aug 16 09:33:31 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

iperf3 python wrapper
=====================

Release v\ |version|.

iPerf3 is a tool for active measurements of the maximum achievable bandwidth on IP networks. More
information on the iPerf3 utility can be found on their `official website <https://iperf.fr/>`_

The python iperf3 module is a wrapper around the iperf3 utility. It utilises the API libiperf
that comes with the default installation. It allows you to interact with the utility in a nice and
pythonic way.

**warning** This module is not compatible with the original iperf/iperf2 utility which is no longer under active development

.. toctree::
   :maxdepth: 2

   installation
   examples
   modules
