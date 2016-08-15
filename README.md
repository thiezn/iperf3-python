pyperf - Python interface to iperf3 using the iperf3 introduced API libiperf

url: https://readthedocs

travisCI build status button

## Description

pyperf provides a wrapper around the excellent iperf3 library. iperf3 is a complete rewrite of the original iperf implementation. more information at https://bla

iperf3 introduces an API called libiperf that allows you to easily interact with iperf3 from other languages. This library provides a python wrapper around libiperf for easy integration into your own python scripts. 

## Quickstart

  pip install pyperf

### Server
```
server = PyPerf()
server.run()
```

### Client
```
client = PyPerf(role='c')
client.verbose = True
client.duration = 10
client.run()
```

## External Dependencies

iperf3 version?? 
libiperf.0  (should come with iperf3)
