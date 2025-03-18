# Projet de Simulation et Détection d'Anomalies Réseau (Packet-Snitcher)

## Description

Ce projet propose une application web de simulation de flux réseau basée sur les données du dataset KDD Cup 99, ainsi qu'un module de détection d'anomalies utilisant le machine learning. L'ensemble de la solution est intégrée dans un environnement conteneurisé avec une API permettant l'interaction entre les différents composants.

## Fonctionnalités

### Interface de Simulation

* Visualisation en temps réel ou en mode playback des connexions réseau issues du dataset KDD Cup 99.

* Affichage dynamique des flux avec possibilité de filtrage, zoom et consultation des détails des événements.

## Agent de Détection d’Anomalies

* Analyse en temps réel des connexions simulées.

* Détection des comportements anormaux à l’aide d’un modèle de machine learning.

* Génération d’alertes avec des indicateurs tels que score de probabilité et classification.

* Journalisation et traçabilité des événements détectés.

## Intégration et Déploiement

* API (REST ou autre) pour la communication entre l’interface de simulation et l’agent de détection.

* Déploiement conteneurisé avec Docker.

* Intégration continue et bonnes pratiques DevOps.



## Lancement & Installation

Cloner le projet 

```bash
  git clone https://github.com/JeanPhilippeCaetano/Packet-Snitcher.git
```

Se déplacer dans le dossier cloné :

```bash
cd Packet-Snitcher/
```

Lancer le docker-compose :

```bash
docker-compose up --build
```

Aller sur le site localement :
http://localhost:8501/

Aller sur le site hébergé : http://hackatonsnitch.ddns.net/ ou http://4.251.8.2:8501/ 