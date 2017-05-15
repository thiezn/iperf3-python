.. :changelog:

Release History
---------------

0.1.4 (2017-05-15)
++++++++++++++++++
- Fixed server json_output=False feature

0.1.3 (2017-05-15)
++++++++++++++++++
- Added UDP support (thanks to @fciaccia)
- Added bandwidth parameter
- json_output = False will now print testresults to screen

0.1.2 (2016-09-22)
++++++++++++++++++
- Improved zerocopy setter validation
- Fix for incorrect return of reverse flag (thanks to @fciaccia)

0.1.1 (2016-09-12)
++++++++++++++++++

- Added reverse test parameter (thanks to @cvicente)
- Updated travis build to test against iperf3 versions 3.0.6 through 3.1.3

0.1.0 (2016-08-18)
++++++++++++++++++

**main functionality available**

- introduced TestResult class providing easy access into test results
- updated client and server examples
- minor documentation tweaks

0.0.1 (2016-08-18)
++++++++++++++++++

**Initial Release**

- Client and Server classes around iperf3's libiperf.so.0 API
- Documentation on readthedocs
- py.tests
- blood
- sweat
- a lot of tears
