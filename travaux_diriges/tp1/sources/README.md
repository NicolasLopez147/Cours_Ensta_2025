
# TD1

`pandoc -s --toc README.md --css=./github-pandoc.css -o README.html`

## lscpu

*lscpu donne des infos utiles sur le processeur : nb core, taille de cache :*

```
Coller ici les infos *utiles* de lscpu.
```


## Produit matrice-matrice

### Effet de la taille de la matrice

  n            | MFlops
---------------|--------
1022           | 386.248
1023           | 464.709
1024 (origine) | 76.6536
1025           | 412.784
1026           | 416.255

*Expliquer les résultats.*


### Permutation des boucles

*Expliquer comment est compilé le code (ligne de make ou de gcc) : on aura besoin de savoir l'optim, les paramètres, etc. Par exemple :*

`make TestProduct.exe && ./TestProduct.exe 1024`


  ordre           | time    | MFlop (n=1024) | MFlops(n=2048)
------------------|---------|----------------|----------------
i,j,k (origine)   | 2.73764 | 782.476        | 520.090 
j,i,k             | 2.95654 | 720.576        | 245.841
i,k,j             | 6.98764 | 254.098        | 146.098
k,i,j             | 7.09382 | 302.435        | 131.346
j,k,i             | 0.54353 | 5635.78        | 3423.54
k,j,i             | 0.47675 | 4567.24        | 3061.43


*Discuter les résultats.*



### OMP sur la meilleure boucle

`make TestProduct.exe && OMP_NUM_THREADS=8 ./TestProduct.exe 1024`

  OMP_NUM         | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)
------------------|---------|----------------|----------------|---------------
1                 |3201.56  | 3164.07        | 3651.56        | 3129.61
2                 |3114.28  | 3083.02        | 3255.77        | 3133.93
3                 |3053.2   | 3055.3         | 3543.26        | 3104.41
4                 |3092.77  | 3085.39        | 3655.36        | 3311.06
5                 |3291.53  | 3022.27        | 2951.37        | 3120.37
6                 |3119.89  | 3196.96        | 3453.13        | 3118.32
7                 |3017.8   | 3050.93        | 3430.18        | 3062.92
8                 |3120.95  | 3017.75        | 3520.16        | 3296.93

*Tracer les courbes de speedup (pour chaque valeur de n), discuter les résultats.*



### Produit par blocs

`make TestProduct.exe && ./TestProduct.exe 1024`

  szBlock         | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)
------------------|---------|----------------|----------------|---------------
origine (=max)    |
32                |
64                |
128               |
256               |
512               |
1024              |

*Discuter les résultats.*



### Bloc + OMP


  szBlock      | OMP_NUM | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)|
---------------|---------|---------|----------------|----------------|---------------|
1024           |  1      |         |                |                |               |
1024           |  8      |         |                |                |               |
512            |  1      |         |                |                |               |
512            |  8      |         |                |                |               |

*Discuter les résultats.*


### Comparaison avec BLAS, Eigen et numpy

*Comparer les performances avec un calcul similaire utilisant les bibliothèques d'algèbre linéaire BLAS, Eigen et/ou numpy.*


# Tips

```
	env
	OMP_NUM_THREADS=4 ./produitMatriceMatrice.exe
```

```
    $ for i in $(seq 1 4); do elap=$(OMP_NUM_THREADS=$i ./TestProductOmp.exe|grep "Temps CPU"|cut -d " " -f 7); echo -e "$i\t$elap"; done > timers.out
```
