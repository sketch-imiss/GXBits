## GXBits: A Compact and Accurate Sketch for Estimating A Large Range of Set Difference Cardinalities
![version](https://img.shields.io/badge/version-v1-green)
![python](https://img.shields.io/badge/python-3.9-blue)
![mmh3](https://img.shields.io/badge/mmh3-3.0.0-red)

This repository contains our implementation of state-of-the-art methods and GXBits for estimating set
difference cardinalities. In comparison with existing methods such as 
[Odd Sketch](https://dl.acm.org/doi/10.1145/2566486.2568017),
[Tug-of-War Sketch](https://www.sciencedirect.com/science/article/pii/S0022000097915452),
and [HyperLogLog Sketch](http://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf),
our proposed GXBits is more accurate and memory-efficient, which builds a bit array for each set to embed
its corresponding elements and estimates the set difference cardinality between two sets based on the joint
of their sketches. Each bit in the array is updated following the geometric distribution and the update probability
varies across different bits. Afterwards, given a random initial value, our GXBits utilizes the Newton-Raphson
methods to further optimize the estimated set difference cardinalities.

### Datasets

The detailed process of generating synthetic datasets is included in [loader.py](loader.py), which can be used to
generate two kinds of synthetic datasets:

* Balanced Synthetic Dataset: the cardinalities of any two sets are equal to each other.
* Skewed Synthetic Dataset: the cardinalities of any two sets are difference from each other.

In addition to synthetic datasets, our GXBits can also be used for real-world datasets. In our experiments, [four
online social network datasets](http://socialnetworks.mpi-sws.mpg.de/data-imc2007.html) are used to evaluate 
the performance:

|Dataset          |#Sets          |Max-Cardinality           |Total-Cardinality
|-----------------|:-------------:|:------------------------:|-----------------|
|Youtube          |570,774        |28,644                    |4,945,382        |
|Flickr           |1,441,431      |26,185                    |22,613,980       |
|Orkut            |2,997,376      |31,949                    |223,534,301      |
|LiveJournal      |4,590,650      |9,186                     |76,937,805       |

### Baseline Methods

|Method            |Data Structure                       |Shortcomings                             |Reference
|------------------|:-----------------------------------:|:---------------------------------------:|----------------------|
|Odd Sketch        |bit array                            |limited estimation range                 |[odd.py](odd.py)      |
|Tug-of-War Sketch |counter array                        |high computational costs and memory usage|[tow.py](tow.py)      |
|HyperLogLog Sketch|counter array                        |high computational costs and memory usage|[hll.py](hll.py)      |
|GXBits            |bit array with geometric distribution|/                                        |[gxbits.py](gxbits.py)|

### Requirements

* Python >= 3.9
* mmh3 >= 3.0.0 (use the command "pip install mmh3")


