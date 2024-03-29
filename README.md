# kurtosis

This repository contains a collection of scripts used for [Variance](http://variance.ch/). It is based on the work of Julien Bourdaillet (julien.bourdaillet@lip6.fr) and Jean-Gabriel Ganascia (jean-gabriel.ganascia@lip6.fr) Please find install instructions [here](install_instructions.md).

## Tag Files
example usage
```
python tag.py tests/Labelle/Informations.xml 
```

## Compare two texts
Example usage
```
python diff.py tests/Labelle/01LaBelle_Ms.txt tests/Labelle/02LaBelle_Mercure.txt
```
The following files will be created in the foder ```tests/Labelle```

| Filename  | Description |
| ------------- | ------------- |
| ```diff_table.html```  | html differences table  |
| ```diff_table_improved.html``` | improved html differences table (work in progress)  |
| ```csv_output.csv``` | csv formatted difference tables  |


Other example usages:
```
python diff.py tests/Labelle/01LaBelle_Ms.txt tests/Labelle/02LaBelle_Mercure.txt --lg_pivot 8 --ratio 10 --seuil 80 
python diff.py tests/Labelle/01LaBelle_Ms.txt tests/Labelle/02LaBelle_Mercure.txt --lg_pivot 8 --ratio 10 --seuil 80 --author "Charles, Perrault, 1628, 1703"
python diff.py tests/Labelle/01LaBelle_Ms.txt tests/Labelle/02LaBelle_Mercure.txt --lg_pivot 8 --ratio 10 --seuil 80 --author "Charles, Perrault, 1628, 1703" --title "La Belle au bois dormant"
python diff.py tests/BdS/BdS1835edition.txt tests/BdS/BdS_1842edition.txt
```

## Compare Sequentially Texts
Put texts that needs to be compared sequentially in a directory. Comparaison will be done based on lexical order on filenames ending with .txt
```
python bulk-diff.py sample/Labelle --lg_pivot 8 --ratio 10 --seuil 80  
python bulk-diff.py sample/Labelle --lg_pivot 8 --ratio 10 --seuil 80  --author "Charles, Perrault, 1628, 1703"
python bulk-diff.py sample/Labelle --lg_pivot 8 --ratio 10 --seuil 80  --author "Charles, Perrault, 1628, 1703" --title "La Belle au bois dormant"
```

