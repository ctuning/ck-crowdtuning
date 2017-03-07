Status
======
This is a stable Collective Knowledge repository to enable
customizable experiment crowdsourcing across Linux, Windows,
Android and MacOS-based platforms provided by volunteers
(such as mobile devices and data centers).

We have several public experimental scenarios include universal,
customizable, multi-dimensional, multi-objective 
GCC/LLVM crowd-tuning. See public crowd-tuning
results in the [CK live repository](http://cknowledge.org/repo)!

See related [Android app](https://play.google.com/store/apps/details?id=openscience.crowdsource.experiments)
to let you participate in our experiment crowdsourcing using
spare Android mobile phones, tables and other devices.

Further details are available at [CK wiki](https://github.com/ctuning/ck/wiki).

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
* http://arxiv.org/abs/1506.06256
* http://bit.ly/ck-date16
* http://arxiv.org/abs/1407.4075
* http://hal.inria.fr/hal-01054763
* https://hal.inria.fr/inria-00436029

Authors
=======
* Grigori Fursin, cTuning foundation (France) / dividiti (UK)

License
=======
* BSD, 3-clause

Prerequisites
=============
* Collective Knowledge Framework: http://github.com/ctuning/ck

Usage
=====

See [CK Getting Started Guide](https://github.com/ctuning/ck/wiki/Crowdsource_Experiments) 
and the section on [Experiment Crowdsourcing](https://github.com/ctuning/ck/wiki/Crowdsourcing-optimization)

You can also participate in crowd-benchmarking and crowd-tuning 
using your Android mobile device using the following apps:
* [small workloads](https://play.google.com/store/apps/details?id=openscience.crowdsource.experiments)
* [large workloads including DNN libs such as Caffe](https://play.google.com/store/apps/details?id=openscience.crowdsource.video.experiments)


Notes
=====
We and the community added various analysis of variation 
of empirical characteristics such as execution time and energy:
min, max, mean, expected values from histogram, normality test, etc.

Users can decide how to calculate improvements based on available statistics
and their requirements. For example, when trying to improve compilers
or hardware, we compare minimal characteristics (execution time, energy, etc),
i.e. the best what we can squeeze from this hardware when there are
no cache effects, contentions, etc. 

Later, we suggest to calculate improvements using expected values -
we noticed that computer systems has "states" (similar to electron energy 
states in physics), hence such improvements will show how a given
program will behave in non-ideal conditions.

Furthermore, when there is more than one expected behavior, i.e.
several states, we suggest to analyze such cases by the community
and find missing experiment features that could explain and separate
such states such as CPU/GPU frequency.

See our papers for more details.

![logo](https://github.com/ctuning/ck-guide-images/blob/master/logo-validated-by-the-community-simple.png)
