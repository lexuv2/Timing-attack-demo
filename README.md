# Implementacja ataku czasowego na funckje porównywania

Bardzo łatwo przez nieuwagę jest zaimplementować niebezpieczną funkcję porównującą, która jest podatna na ataki czasowe (zliczanie czasu wykonania).
Przykładowa funkcja w języku c++:
```cpp
bool compare(const std::string& a, const std::string& b) {
    if (a.size() != b.size()) {
        return false;
    }
    for (size_t i = 0; i < a.size(); i++) {
        if (a[i] != b[i]) {
            return false;
        }
    }
    return true;
}
```
Funkcja ta porównuje dwa napisy znak po znaku. Jeśli dwa napisy są różnej długości, to zwraca `false`. W przeciwnym wypadku porównuje znaki na kolejnych pozycjach. Jeśli na którejś pozycji znaki się różnią, to zwraca `false`, bez przejścia przez resztę napisu. Ilośc instruki wykonanych przez procesor będzie się różnić w zależności od tego czy funkcja wcześniej zakończyła sprawdzanie. Dzięki temu można estymować jaka częśc napisu jest jest taka sama.

W pliku `exploit.ipynb` jest przykładowa implementacja ataku czasowego na taką funkcję. Skrypt trzeba uruchomić w środowisku jupyter notebook. 

Fodler `samples` zawiera przykładowe pliki do testowania używające różnych implementacji funkcji porównujących.
Niektóre są całkowicie niewrażliwe na takie ataki, a niektóre np. tylko częściowo i pozwalają poznać długość napisu.

Dodatkowo w folderze `samples` znajdują się trzy pliki `keygen`,`hangover` i `virtual.1` które są bardziej złożonymi przykładami ataków czasowych. `hangover` jest przykładem z zadania z PINGctf, które może być rozwiązane tym sposobem. `virtual.1` pokazuje w jaki sposób informacje o czasie wykonania mogą być pomocne przy inżynierii wstecznej.

#### Links
https://crypto.stanford.edu/~dabo/papers/ssl-timing.pdf

https://security.stackexchange.com/questions/83660/simple-string-comparisons-not-secure-against-timing-attacks

https://dba.stackexchange.com/questions/285739/prevent-timing-attacks-in-postgres

https://lirias.kuleuven.be/retrieve/389086

https://github.com/agl/ctgrind
