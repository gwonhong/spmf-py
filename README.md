# spmf-py
Python Wrapper for SPMF 🐍 🎁

## Information
The [SPMF](http://www.philippe-fournier-viger.com/spmf) [[1](https://github.com/gwonhong/spmf-py#bibliography)] data mining Java library usable in Python.  

Essentially, this module calls the Java command line tool of SPMF, passes the user arguments to it, and parses the output.  

In theory, all algorithms featured in SPMF are callable. Nothing is hardcoded, the desired algorithm and its parameters need to be perused in the [SPMF documentation](http://www.philippe-fournier-viger.com/spmf/index.php?link=documentation.php).

## Installation
~~[`pip install spmf`](https://pypi.org/project/spmf/)~~
Since this is the fork version of python spmf package, you should 
1. clone this repo
2. pip install path/to/cloned

## Usage
Example:  
```python
from spmf import Spmf

spmf = Spmf("PrefixSpan", input_type="file", \
            input_filename="contextPrefixSpan.txt", \
            arguments=[0.7, 5])
spmf.run()
result = spmf.parse_output()
print(len(result))
```

Output:
```
>.../spmf/spmf.jar
=============  PREFIXSPAN 0.99-2016 - STATISTICS =============
 Total time ~ 8 ms
 Frequent sequences count : 14
 Max memory (mb) : 10.241966247558594
 minsup = 3 sequences.
 Pattern count : 14
===================================================


14
(4, ['1'])
(4, ['1', '2'])
(4, ['1', '3'])
(3, ['1', '3', '2'])
(3, ['1', '3', '3'])
(4, ['2'])
(3, ['2', '3'])
(4, ['3'])
(3, ['3', '2'])
(3, ['3', '3'])
(3, ['4'])
(3, ['4', '3'])
(3, ['5'])
(3, ['6'])
```

The usage is similar to the one described in the SPMF [documentation](http://www.philippe-fournier-viger.com/spmf/index.php?link=documentation.php).  
For all Python parameters, see the [Spmf class](https://github.com/gwonhong/spmf-py/blob/master/spmf/__init__.py).  

### SPMF Arguments
The `arguments` parameter are the arguments that are passed to SPMF and depend on the chosen algorithm. SPMF handles optional parameters as an ordered list. As there are no named parameters for the algorithms, if e.g. only the first and the last parameter of an algorithm are to be used, the ones in between must be filled with `""` blank strings.  
For advanced usage examples, see [`examples`](https://github.com/gwonhong/spmf-py/tree/master/examples).

### SPMF Executable
Download it from the [SPMF Website](http://www.philippe-fournier-viger.com/spmf/index.php?link=download.php).  
It is assumed that the SPMF binary `spmf.jar` is located in the same directory as `spmf-py`. If it is not, either symlink it, or use the `spmf_bin_location_dir` parameter.

### Input Formats
Either use an input file as specified by SPMF, or use one of the in-line formats as seen in [`examples`](https://github.com/gwonhong/spmf-py/tree/master/examples).

### Memory
The maxmimum memory can be increased in the constructor via `Spmf(memory=n)`,
where `n` is megabyte, see SPMF's
[FAQ](http://www.philippe-fournier-viger.com/spmf/index.php?link=FAQ.php#memory).

## Background
Why? If you're in a Python pipeline, like a Jupyter Notebook, it might be cumbersome to use Java as an intermediate step. Using `spmf-py` you can stay in your pipeline as though Java is never used at all.

## Bibliography
```
Fournier-Viger, P., Lin, C.W., Gomariz, A., Gueniche, T., Soltani, A., Deng, Z., Lam, H. T. (2016).  
The SPMF Open-Source Data Mining Library Version 2.  
Proc. 19th European Conference on Principles of Data Mining and Knowledge Discovery (PKDD 2016) Part III, Springer LNCS 9853,  pp. 36-40.
```

## Disclaimer

Use at your own risk. This repo is not/barely maintained. Use SPMF itself for more robust results.

This module has been tested for a fraction of the algorithms offered in SPMF.
Calling them and writing to the output file should be possible for all.
Output parsing however should work for those that have outputs like the sequential pattern mining algorithms.
It was not tested with other types, some adaption of the output parsing might be necessary.

If something is not working, submit an issue or create a PR yourself!
