# Résultats du laboratoire — 14 septembre 2026

Le laboratoire étudie la constante de platitude en dimension trois, la largeur
entière des corps convexes creux et la géométrie de leurs contacts avec le
réseau. Les résultats ci-dessous sont vérifiés en interne avec assistance IA.
La conjecture Flt(3)=2+√2 reste ouverte ; aucune nouvelle borne globale ni
nouveauté mathématique établie n'est revendiquée.

## Résultats certifiés

- Reproduction exacte du tétraèdre de Codenotti–Santos, de largeur 2+√2 :
  absence de point entier intérieur, largeur complète et symétries.
- Réduction structurelle à 63 configurations nécessaires de contacts au-dessus
  de (11/7)(1+2/√3), représentées dans neuf gabarits. Ce n'est pas une
  classification des corps réalisant ces contacts à grande largeur.
- Deux bornes analytiques pour les tétraèdres contenant les configurations
  de déterminants 10 et 13 ; trois exclusions supplémentaires pour des
  contacts prescrits dans les intérieurs relatifs des facettes, de
  déterminants 5, 7 et 8. Il reste 58 configurations nécessaires au seuil
  2+√2. Les dernières exclusions reposent sur 67 réfutations vérifiées
  par le logiciel indépendant Ethos ; cela ne constitue pas une revue humaine.

## Dernière avancée méthodologique

Un témoin creux exact de la seconde classe de déterminant cinq possède des
largeurs supérieures à 17/5 dans les deux directions étudiées. Son minimum
entier de K-K, 211637/541875, satisfait même le seuil nécessaire ACMS exact,
et les contraintes de volume considérées sont satisfaites. Sa largeur
entière complète n'est pourtant qu'environ 2,449, atteinte dans la direction Z.

Ce témoin prouve que la subdivision du seul modèle à deux directions ne peut
aboutir à l'exclusion recherchée avec ces contraintes. La campagne est figée
à 953 requêtes, avec 259 boîtes en attente. Ces explorations partielles ne
sont pas comptées comme de nouvelles preuves d'exclusion. La suite doit
ajouter les largeurs manquantes du modèle complet à quinze directions.

Un lemme auxiliaire établit aussi que largeur(K,u)/volume(K) ne dépasse pas
largeur(P,u)/volume(P) pour deux tétraèdres pleins emboîtés P⊂K. Sa preuve
élémentaire et son contrôle symbolique sont fournis, sans revendication de
priorité.

- [Résultats et preuves détaillés](../README.md)
- [Témoin exact et vérification exhaustive](../proofs/DET5_FULL_GAUGE_RETAINED_WITNESS.md)
- [Validation de la copie publique](../PUBLIC_VALIDATION.md)
- [Prochaines étapes](../NEXT.md)

La publication concerne ce dépôt GitHub. Aucun article n'a été soumis à une
revue ou à arXiv, et aucune validation humaine externe n'est revendiquée.
