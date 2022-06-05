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
$ conda env create -f environment.yml

....

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

Verify diff tool works using "La Belle au bois dormant".
```
python diff.py tests/Labelle/01LaBelle_Ms.txt tests/Labelle/02LaBelle_Mercure.txt --lg_pivot 7 --ratio 15 --seuil 50
```

