Code sur les ATmega
====

Quelques notes sont regroupées ci-dessous.

## Pins

* 15 (datasheet ATmel) == 9 (Arduino) : Led R
* 16 (datasheet ATmel) == 10 (Arduino) : Led G
* 17 (datasheet ATmel) == 11 (Arduino) : Led B

## Paquets serial

Un paquet serial a la forme suivante (4 bytes) :

```
synchro (= 1) | fonction | compteur
 1bit         |  1 bit   |  6 bits
```

```
synchro (= 0) | couleurR
 1bit         |  7 bits
```

```
synchro (= 0) | couleurG
 1bit         |  7 bits
```

```
synchro (= 0) | couleurB
 1bit         |  7 bits
```

## Fonctions

* `0b0` : Switch immédiat
* `0b1` : Broadcast (traite le paquet et le forward quand même avec compteur nul)

## Divers

* serialEvent est appelée automatiquement à la fin de loop() si des données sont dispos sur le RX.
* Lors de l'arrivée d'un header, `serial_i = compteur`.
* `serial_i décrit l'état
    * `-1` => attente de header
    * `0` => en attente des données à traiter pour la led rouge
    * `1` => en attente des données à traiter pour la led bleue
    * `2` => en attente des données à traiter pour la led verte
* Pas besoin d'appel à pinMode avant un analogWrite.
