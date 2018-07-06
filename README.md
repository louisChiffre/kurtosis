# kurtosis

Collection of scripts related to [Variance]

## Tag Files
example usage
```
python tag.py --filename samples/LaBelle/Informations.xml
```

## Compare two texts
example usage
```
python diff.py tests/Labelle/01LaBelle_Ms.txt tests/Labelle/02LaBelle_Mercure.txt
python diff.py tests/Labelle/01LaBelle_Ms.txt tests/Labelle/02LaBelle_Mercure.txt --lg_pivot 8 --ratio 10 --seuil 80 
```

## Compare Sequentially Texts
Put texts that needs to be compared sequentially in a directory. Comparaison will be done sequentially based on lexical order on filenames ending with .txt
```
python bulk-diff.py sample/Labelle --lg_pivot 8 --ratio 10 --seuil 80  
```

