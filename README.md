Status
======
This is an unstable, heavily evolving repository 
please, do not use it until official announcement.

Description
===========
This repository is based on CK machine-learning based autotuning.
It crowdsources experiments (using optimization knobs exposed
via CK such as OpenCL, compiler flag, CUDA, etc)
across many machines while building a realistic,
large and representative training set. 

This is a continuation of Grigori Fursin's original postdoctoral
proposal for the MILEPOST project in 2005, i.e. crowdsource
training of a machine-learning based compiler across
any shared computational resource such as mobile phones
(supported by the non-profit cTuning foundation since 2008).

Publications
============
* http://bit.ly/ck-date16
* http://hal.inria.fr/hal-01054763
* https://hal.inria.fr/inria-00436029
* http://arxiv.org/abs/1407.4075

Authors
=======
* Grigori Fursin, cTuning foundation (France) / dividiti (UK)

License
=======
* BSD, 3-clause

Prerequisites
=============
* Collective Knowledge Framework: http://github.com/ctuning/ck

Installation
============

> ck pull repo:ck-crowdtuning

Modules with actions
====================

scenario.compiler.flags - collective experiment: compiler flag tuning

  * crowdtune - crowd-tune compiler flags (on-going)
