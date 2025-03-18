# Packet-Snitcher

# Projet de Simulation et Détection d'Anomalies Réseau

## Description

Ce projet propose une application web de simulation de flux réseau basée sur les données du dataset KDD Cup 99, ainsi qu'un module de détection d'anomalies utilisant le machine learning. L'ensemble de la solution est intégrée dans un environnement conteneurisé avec une API permettant l'interaction entre les différents composants.

## Fonctionnalités

### Interface de Simulation

Visualisation en temps réel ou en mode playback des connexions réseau issues du dataset KDD Cup 99.

Affichage dynamique des flux avec possibilité de filtrage, zoom et consultation des détails des événements.

## Agent de Détection d’Anomalies

Analyse en temps réel des connexions simulées.

Détection des comportements anormaux à l’aide d’un modèle de machine learning.

Génération d’alertes avec des indicateurs tels que score de probabilité et classification.

Journalisation et traçabilité des événements détectés.

## Intégration et Déploiement

API (REST ou autre) pour la communication entre l’interface de simulation et l’agent de détection.

Déploiement conteneurisé avec Docker.

Intégration continue et bonnes pratiques DevOps.


