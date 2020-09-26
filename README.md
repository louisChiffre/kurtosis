# kurtosis

This repository contains a collection of scripts used for [Variance](http://variance.ch/). Please find install instructions [here](install_instructions.md)

## Tag Files
example usage
```
python tag.py tests/Labelle/Informations.xml 
```

## Compare two texts
example usage
```
python diff.py tests/Labelle/01LaBelle_Ms.txt tests/Labelle/02LaBelle_Mercure.txt
python diff.py tests/Labelle/01LaBelle_Ms.txt tests/Labelle/02LaBelle_Mercure.txt --lg_pivot 8 --ratio 10 --seuil 80 
python diff.py tests/Labelle/01LaBelle_Ms.txt tests/Labelle/02LaBelle_Mercure.txt --lg_pivot 8 --ratio 10 --seuil 80 --author "Charles, Perrault, 1628, 1703"
python diff.py tests/Labelle/01LaBelle_Ms.txt tests/Labelle/02LaBelle_Mercure.txt --lg_pivot 8 --ratio 10 --seuil 80 --author "Charles, Perrault, 1628, 1703" --title "La Belle au bois dormant"
```

## Compare Sequentially Texts
Put texts that needs to be compared sequentially in a directory. Comparaison will be done based on lexical order on filenames ending with .txt
```
python bulk-diff.py sample/Labelle --lg_pivot 8 --ratio 10 --seuil 80  
python bulk-diff.py sample/Labelle --lg_pivot 8 --ratio 10 --seuil 80  --author "Charles, Perrault, 1628, 1703"
python bulk-diff.py sample/Labelle --lg_pivot 8 --ratio 10 --seuil 80  --author "Charles, Perrault, 1628, 1703" --title "La Belle au bois dormant"
```

