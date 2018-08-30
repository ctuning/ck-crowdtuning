[![logo](https://github.com/ctuning/ck-guide-images/blob/master/logo-powered-by-ck.png)](http://cKnowledge.org)
[![logo](https://github.com/ctuning/ck-guide-images/blob/master/logo-validated-by-the-community-simple.png)](http://cTuning.org)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

This is a stable Collective Knowledge repository to enable
customizable experiment crowdsourcing across diverse Linux, Windows,
MacOS and Android-based platforms provided by volunteers
(such as mobile devices/IoT, data centers and supercomputers).

![logo](https://github.com/ctuning/ck-guide-images/blob/master/image-pipelines.png)

We have several public experimental scenarios include universal,
customizable, multi-dimensional, multi-objective 
[DNN crowd-benchmarking](http://cKnowledge.org/ai) 
and [compiler crowd-tuning](http://github.com/ctuning/ck-autotuning).

See continuously aggregated public results results and
unexpected behavior in the [CK live repository](http://cKnowledge.org/repo)!

Also check out our related Android apps to let you participate in our experiment crowdsourcing using
spare Android mobile phones, tables and other devices:
* [collaborative deep learning optimization app](http://cKnowledge.org/android-apps.html)
* [compiler tuning using small kernels](http://cKnowledge.org/android-apps.html)
* [CK crowd-scenarios](https://github.com/ctuning/ck-crowd-scenarios)

Further details are available at [CK wiki](https://github.com/ctuning/ck/wiki),
[open research challenges wiki](https://github.com/ctuning/ck/wiki/Enabling-open-science)
and [reproducible and CK-powered AI/SW/HW co-design competitions at ACM/IEEE conferences](http://cKnowledge.org/request).

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

Authors
=======
* [Grigori Fursin](http://fursin.net/research.html), dividiti/cTuning foundation

License
=======
* BSD, 3-clause

Prerequisites
=============
* [Collective Knowledge Framework](http://github.com/ctuning/ck)
* [Compilers for your target machine (Linux, Windows, MacOS, Android)](https://github.com/ctuning/ck/wiki/Compiler-autotuning#Installing_compilers)

Usage
=====

See [CK Getting Started Guide](https://github.com/ctuning/ck/wiki/Crowdsource_Experiments) 
and the section on [Experiment Crowdsourcing](https://github.com/ctuning/ck/wiki/Crowdsourcing-optimization)

You can also participate in crowd-benchmarking and crowd-tuning 
using your Android mobile device using the following apps:
* [small workloads](http://cKnowledge.org/android-apps.html)
* [large workloads including DNN libs such as Caffe](http://cKnowledge.org/android-apps.html)


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

Publications
============

The concepts have been described in the following publications:

```
@inproceedings{ck-date16,
    title = {{Collective Knowledge}: towards {R\&D} sustainability},
    author = {Fursin, Grigori and Lokhmotov, Anton and Plowman, Ed},
    booktitle = {Proceedings of the Conference on Design, Automation and Test in Europe (DATE'16)},
    year = {2016},
    month = {March},
    url = {https://www.researchgate.net/publication/304010295_Collective_Knowledge_Towards_RD_Sustainability}
}

@inproceedings{cm:29db2248aba45e59:cd11e3a188574d80,
    title = {{Collective Mind, Part II}: Towards Performance- and Cost-Aware Software Engineering as a Natural Science},
    author = {Fursin, Grigori and Memon, Abdul and Guillon, Christophe and Lokhmotov, Anton},
    booktitle = {18th International Workshop on Compilers for Parallel Computing (CPC'15)},
    year = {2015},
    url = {https://arxiv.org/abs/1506.06256},
    month = {January}
}

@inproceedings{Fur2009,
  author =    {Grigori Fursin},
  title =     {{Collective Tuning Initiative}: automating and accelerating development and optimization of computing systems},
  booktitle = {Proceedings of the GCC Developers' Summit},
  year =      {2009},
  month =     {June},
  location =  {Montreal, Canada},
  keys =      {http://www.gccsummit.org/2009}
  url  =      {https://scholar.google.com/citations?view_op=view_citation&hl=en&user=IwcnpkwAAAAJ&cstart=20&citation_for_view=IwcnpkwAAAAJ:8k81kl-MbHgC}
}
```

* http://arxiv.org/abs/1506.06256
* http://hal.inria.fr/hal-01054763
* https://hal.inria.fr/inria-00436029
* http://arxiv.org/abs/1407.4075
* https://scholar.google.com/citations?view_op=view_citation&hl=en&user=IwcnpkwAAAAJ&citation_for_view=IwcnpkwAAAAJ:LkGwnXOMwfcC

Feedback
========

If you have problems, questions or suggestions, do not hesitate to get in touch
via the following mailing lists:
* https://groups.google.com/forum/#!forum/collective-knowledge
* https://groups.google.com/forum/#!forum/ctuning-discussions
