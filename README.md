## GLS

Implementation of the Generalised Lomb Scargle periodogram(GLS;[Zehcmeister & Kurster 2009](https://ui.adsabs.harvard.edu/abs/2009A%26A...496..577Z/abstract))in C++, with wrapper in python.

### Installation

The C++ code in the `cpp/` folder has to be compiled as a shared library.

In many platforms, this should work:

```g++ -O2 -fPIC -shared GLSperiodogram.cpp -o GLSperiodogram.so```
