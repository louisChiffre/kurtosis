# Install Instructions

Retrieve the source code by opening a terminal window. Change to directory to your working directory of your choice and clone the source code
```
$ cd your-directory
```

Retrieve the source code
```
$ git clone https://github.com/louisChiffre/kurtosis.git
Cloning into 'kurtosis'...
remote: Counting objects: 182, done.
remote: Compressing objects: 100% (128/128), done.
remote: Total 182 (delta 82), reused 147 (delta 49), pack-reused 0
Receiving objects: 100% (182/182), 572.00 KiB | 0 bytes/s, done.
Resolving deltas: 100% (82/82), done.
Checking connectivity... done.
```
Change directory to the source directory

```
$ cd kurtosis
```


To simplify install of external packages, setup conda on your machine. 

First follow instructions here https://conda.io/projects/conda/en/latest/user-guide/install/macos.html

Then create a python 2.7 environment named medite.
```
$ conda create --name medite python=2.7
Solving environment: done

## Package Plan ##

  environment location: /Users/laurent/miniconda3/envs/medite

  added / updated specs: 
    - python=2.7


The following NEW packages will be INSTALLED:

    ca-certificates: 2018.03.07-0           
    certifi:         2018.4.16-py27_0       
    libcxx:          4.0.1-h579ed51_0       
    libcxxabi:       4.0.1-hebd6815_0       
    libedit:         3.1.20170329-hb402a30_2
    libffi:          3.2.1-h475c297_4       
    ncurses:         6.1-h0a44026_0         
    openssl:         1.0.2o-h26aff7b_0      
    pip:             10.0.1-py27_0          
    python:          2.7.15-h138c1fe_0      
    readline:        7.0-hc1231fa_4         
    setuptools:      39.2.0-py27_0          
    sqlite:          3.24.0-ha441bb4_0      
    tk:              8.6.7-h35a86e2_3       
    wheel:           0.31.1-py27_0          
    zlib:            1.2.11-hf3cbc9b_2      

Proceed ([y]/n)? y

Preparing transaction: done
Verifying transaction: done
Executing transaction: done
#
# To activate this environment, use
#
#     $ conda activate medite
#
# To deactivate an active environment, use
#
#     $ conda deactivate


```

Activate the environment 
```
$ conda activate medite
(medite)$ 
```

Install pandas, qt and click python libaries.
```
$ conda install -c anaconda pyqt=4.11.4 click pandas
Solving environment: done

## Package Plan ##

  environment location: /Users/laurent/miniconda3/envs/medite

  added / updated specs: 
    - click
    - pandas
    - pyqt=4.11.4


The following packages will be downloaded:

    package                    |            build
    ---------------------------|-----------------
    numpy-1.14.5               |   py27h9bb19eb_3          94 KB  anaconda
    certifi-2018.4.16          |           py27_0         142 KB  anaconda
    mkl-2018.0.3               |                1       149.2 MB  anaconda
    mkl_random-1.0.1           |   py27h78cc56f_0         355 KB  anaconda
    pandas-0.23.1              |   py27h1702cab_0        11.1 MB  anaconda
    numpy-base-1.14.5          |   py27ha9ae307_3         4.0 MB  anaconda
    ca-certificates-2018.03.07 |                0         124 KB  anaconda
    mkl_fft-1.0.1              |   py27h917ab60_0         130 KB  anaconda
    python-dateutil-2.7.3      |           py27_0         258 KB  anaconda
    click-6.7                  |   py27h2b86a94_0         103 KB  anaconda
    intel-openmp-2018.0.3      |                0        1004 KB  anaconda
    openssl-1.0.2o             |       h26aff7b_0         3.4 MB  anaconda
    libgfortran-3.0.1          |       h93005f0_2         495 KB  anaconda
    blas-1.0                   |              mkl           5 KB  anaconda
    pytz-2018.5                |           py27_0         230 KB  anaconda
    six-1.11.0                 |   py27h7252ba3_1          21 KB  anaconda
    ------------------------------------------------------------
                                           Total:       170.6 MB

The following NEW packages will be INSTALLED:

    blas:            1.0-mkl               anaconda
    click:           6.7-py27h2b86a94_0    anaconda
    freetype:        2.9.1-hb4e5f40_0      anaconda
    intel-openmp:    2018.0.3-0            anaconda
    libgfortran:     3.0.1-h93005f0_2      anaconda
    libpng:          1.6.34-he12f830_0     anaconda
    mkl:             2018.0.3-1            anaconda
    mkl_fft:         1.0.1-py27h917ab60_0  anaconda
    mkl_random:      1.0.1-py27h78cc56f_0  anaconda
    numpy:           1.14.5-py27h9bb19eb_3 anaconda
    numpy-base:      1.14.5-py27ha9ae307_3 anaconda
    pandas:          0.23.1-py27h1702cab_0 anaconda
    pyqt:            4.11.4-py27_4         anaconda
    python-dateutil: 2.7.3-py27_0          anaconda
    pytz:            2018.5-py27_0         anaconda
    qt:              4.8.7-4               anaconda
    sip:             4.18-py27_0           anaconda
    six:             1.11.0-py27h7252ba3_1 anaconda

The following packages will be UPDATED:

    ca-certificates: 2018.03.07-0                   --> 2018.03.07-0      anaconda
    certifi:         2018.4.16-py27_0               --> 2018.4.16-py27_0  anaconda
    openssl:         1.0.2o-h26aff7b_0              --> 1.0.2o-h26aff7b_0 anaconda

Proceed ([y]/n)? y


Downloading and Extracting Packages
numpy-1.14.5         |   94 KB | ############################################################################################################################################################################## | 100% 
certifi-2018.4.16    |  142 KB | ############################################################################################################################################################################## | 100% 
mkl-2018.0.3         | 149.2 MB | ############################################################################################################################################################################# | 100% 
mkl_random-1.0.1     |  355 KB | ############################################################################################################################################################################## | 100% 
pandas-0.23.1        | 11.1 MB | ############################################################################################################################################################################## | 100% 
numpy-base-1.14.5    |  4.0 MB | ############################################################################################################################################################################## | 100% 
ca-certificates-2018 |  124 KB | ############################################################################################################################################################################## | 100% 
mkl_fft-1.0.1        |  130 KB | ############################################################################################################################################################################## | 100% 
python-dateutil-2.7. |  258 KB | ############################################################################################################################################################################## | 100% 
click-6.7            |  103 KB | ############################################################################################################################################################################## | 100% 
intel-openmp-2018.0. | 1004 KB | ############################################################################################################################################################################## | 100% 
openssl-1.0.2o       |  3.4 MB | ############################################################################################################################################################################## | 100% 
libgfortran-3.0.1    |  495 KB | ############################################################################################################################################################################## | 100% 
blas-1.0             |    5 KB | ############################################################################################################################################################################## | 100% 
pytz-2018.5          |  230 KB | ############################################################################################################################################################################## | 100% 
six-1.11.0           |   21 KB | ############################################################################################################################################################################## | 100% 
Preparing transaction: done
Verifying transaction: done
Executing transaction: done

```

Verify diff tool works using "La Belle au bois dormant".
```
python diff.py tests/Labelle/01LaBelle_Ms.txt tests/Labelle/02LaBelle_Mercure.txt --lg_pivot 7 --ratio 15 --seuil 50
```

