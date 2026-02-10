Produit : Deskea Evaluate - Module complémentaire Analyse de sentiments
Version : 1.0
Date : Décembre 2025
Statut : 
draft for review
 
@Sébastien MONNIER @Elaraby ARKNI @Mohamed IDBAAZI @Pierre-Alain Thiout @Khalid Sbai Elotmani @Oualid BELKASRI @ayoub errkhis @Bamhaouch Fatimazahra @imane.elgouch 

Résumé Exécutif
Contexte
Personas
Périmètre Produit
Moteur d’analyse
Tableau de Bord / Reporting
Filtrage & Segmentation
Fonctions Administratives
Capacités d'Export
Exigences fonctionnelles
Traitement des données
EF-1 : Moteur d’analyse sentiment
EF-2 : Catégorisation thématique - Hors MVP
EF-3 : Nuage de Mots Thématique
EF-4 : Timeline Évolution
EF-5 : Vue Liste Verbatims
EF-6 : Vue Détail Verbatim
EF-7 : Matrice de priorisation Hors MVP- a implementer quand avec la taxonomie
EF-8 : Système de filtrage
Fonctions administratives
EF-9 : Interface gestion taxonomie - Hors MVP
EF-10 : Contrôle d’accès basé sur rôles
Export et partage
EF-11 Export Excel
EF-12 Génération Rapport PDF
Questions & hypothèses
Questions
Hypothèses
Annexes
Annexe A : Glossaire
Tickets JIRA
 

Résumé Exécutif
Vision Produit

Transformer les données de conversations clients en insights actionnables en capturant, analysant et visualisant automatiquement le sentiment client sur l'ensemble des points de contact. Permettre aux Responsables Qualité, Directeurs de l'Expérience Client et Managers d'identifier de manière proactive les points de friction et les opportunités d'amélioration du service.

Objectifs business

Revenus : Lancement d'un module complémentaire Voice of Customer  générant un ARR incrémental depuis la base clients existante Deskea Evaluate

Positionnement marché : Établir Deskea comme plateforme d'analyse CX complète au-delà du monitoring qualité (QMA)

Valeur client : Réduire le time-to-insight de plusieurs semaines (analyse manuelle) à quelques minutes (tableaux de bord automatisés - reporting quotidien)

Avantage concurrentiel : Taxonomies spécifiques par industrie en fonction du client (transport, automobile, retail, assurance) vs. outils VoC génériques

Contexte
Problématique

État Actuel :

Solution et reporting déployé depuis plusieurs années pour TUI, basée sur service NLP https://treport.tersea.com/#/site/TUIGROUP/views/AnalyseVerbatim/AnalysedeVerbatims?:iid=2

Premiere version d’un module VOC, basé sur LLM, implémenté pour DPD mais non utilisé (demande de l’ancien management de DPD)

État Cible :
Voice of Customer automatisée et en temps réel, faisant émerger tendances, drivers de sentiment et actions prioritaires sans intervention manuelle.

Personas
Persona 1 : Responsable Qualité (Principal)

Objectifs : Identifier les problèmes qualité systémiques, suivre les initiatives d'amélioration, reporter à la direction

Pain Points : Noyé dans les données conversationnelles, résolution de problèmes réactive, difficile de prouver le ROI des initiatives qualité

Maturité Tech : Moyenne - à l'aise avec les dashboards, besoin de filtres intuitifs

Persona 2 : Directeur CX

Objectifs : Améliorations stratégiques de l'expérience client, aligner l'organisation sur les priorités client

Pain Points : Sources de données déconnectées, décisions anecdotiques vs. data-driven, génération lente d'insights

Maturité Tech : Élevée - veut des analytics avancées, exports pour présentations exécutives

Persona 3 : Manager de Site / Projet

Objectifs : Excellence opérationnelle, coaching d'équipe, satisfaction client au niveau local

Pain Points : Rapports corporate génériques non actionnables pour leur site, besoin d'insights localisés

Maturité Tech : Faible-Moyenne - besoin de vues simples, filtrées sur leur périmètre

Périmètre Produit
green circle Inclus dans le Périmètre - Phase 1 (MVP)

Moteur d’analyse
Analyse automatique du sentiment (Positif/Neutre/Négatif) sur toutes les conversations transcrites et emails

Extraction et catégorisation thématique via taxonomie configurable

Traitement batch aligné avec les cycles d'évaluation Deskea Evaluate existants

Tableau de Bord / Reporting
Visualisation nuage de mots : Fréquence thématique + heatmap sentiment (gradient vert/rouge)

Graphique Évolution Tendance : Volume mensuel + score satisfaction global (%)

Liste Verbatims : Retours clients filtrables avec tags sentiment

Vue détail Verbatim : Contexte conversation complet, métadonnées, mise en évidence mots-clés

Matrice de Priorisation : Analyse quadrant Impact × Fréquence pour priorisation thèmes

Filtrage & Segmentation
Filtres temporels 

Hiérarchie organisationnelle (niveaux Projet/Opération/Equipe)

Dimensions spécifiques industrie (Filtres Métadatas en fonction du client)

Filtres sentiment: Détracteurs/Passifs/Promoteurs

Recherche textuelle dans verbatims

Fonctions Administratives
Constructeur Taxonomie : Créer/éditer/supprimer thèmes et sous-thèmes

Accès basé sur rôles : Super Admin (config globale), Admin (niveau organisation), Admin Local (niveau equipes)

Capacités d'Export
Export Excel (données verbatim brutes + statistiques agrégées)

Génération rapport PDF

red circle Hors périmètre - Phase 1 

Calcul et intégration score NPS (pas d’enquête NPS en entrée)

Système d'alerting/notifications automatisées (priorité basse pour MVP)

Analytics streaming temps réel (traitement batch suffisant initialement)

Analyse sentiment multilingue (français uniquement pour MVP)

Accès API pour systèmes externes

Fonctionnalités collaboration (commentaires, annotations, partage)

Analytics prédictives

Roadmap Future (Phase 2+)

Intégration NPS avec corrélation verbatims si fourni pas le client (Renault, DPD,…)

Alerting proactif sur dégradation sentiment, en relation avec le module de notification en cours de développement

Support de canaux additionnels: chat, réseaux sociaux, enquêtes

Niveaux tonalité avancés (sous-catégories Enchanté/Frustré/En colère)

Insights et recommandations générés par IA

Exigences fonctionnelles
Traitement des données
EF-1 : Moteur d’analyse sentiment
Description : Classifier automatiquement chaque verbatim (transcription conversation ou email) avec polarité sentiment.

Critères d’acceptation :

Système traite toutes conversations dans file Deskea Evaluate

Chaque verbatim assigné label Positif/Neutre/Négatif

Considérations techniques :

Décision requise : Utiliser modèle NLP existant rapport TUI vs. upgrade vers LLM moderne (Claude, Gemini,…)

Équipe Dev : Conduire spike technique pour comparaison précision, coût, time to market entre approches 
https://tersea.atlassian.net/browse/ASSIST-2618Can't find link 

Recommandation : Benchmark sur échantillon 100 conversations avant décision architecture

EF-2 : Catégorisation thématique - Hors MVP
Description : Extraire et assigner thèmes conversation basés sur taxonomie configurable.

Critères d'Acceptation :

Système map verbatims vers 1-N thèmes (classification multi-label)

Hiérarchie thème supporte 3 niveaux (Thème > Sous-thème > Détail) / aujourd’hui on peut avoir uniquement 1 grille VOC avec 1 niveau

Seuil confiance configurable par taxonomie (défaut : 70%)

Interface de reporting

Concept Dashboard VOC


 

EF-3 : Nuage de Mots Thématique
Description : Représentation visuelle prévalence thème et sentiment.

Critères d’acceptation :

Taille mot proportionnelle à fréquence

radient couleur : Vert (>70% positif) → Jaune (40-70%) → Rouge (<40% positif)

Tooltip survol affiche : Nom thème, Compte occurrences, % Positif, % Négatif

Clic vers liste verbatims filtrée pour item sélectionné

Design responsive

Concept Nuage thématique


EF-4 : Timeline Évolution
Description : Graphique double axe montrant volume et tendances satisfaction.

Critères d’acceptation :

Graphique barres : Volume verbatims traités mensuel/hebdomadaire

Overlay graphique ligne : Score satisfaction global (% positif vs. total)

Axe X : Périodes temps (minimum historique 12 mois)

Tooltips interactifs avec valeurs exactes

Concept Evolution VOC


 

EF-5 : Vue Liste Verbatims
Description : Table retours clients avec fonction Recherche et triable.

Critères d’acceptation :

Colonnes : Date, Extrait (150 premiers caractères), Badge sentiment, Tags thème, Source (appel/email)

Pagination : 50 éléments par page

Tri par : Date (défaut plus récent d'abord), Sentiment, Thème

Clic ligne déploie vue détail verbatim complète

Concept Liste des Verbatims VOC


EF-6 : Vue Détail Verbatim
Description : Contexte conversation complet avec métadonnées enrichies.

Critères d’acceptation :

Affichage transcription complète

Mise en évidence mots-clés (thèmes en gras, phrases sentiment colorées)

Panneau métadonnées : Date/heure, Durée, ID Agent, ID Client (si connu), Site centre d'appels

Items assignés avec scores confiance

Concept Détails d’un Verbatim


 

EF-7 : Matrice de priorisation Hors MVP- a implementer quand avec la taxonomie
Description : Matrice 2×2 positionnant thèmes par impact et fréquence.

Critères d’acceptation :

Axe X : Fréquence (% total verbatims mentionnant thème)

Axe Y : Impact (différentiel satisfaction : % positif dans thème vs. baseline globale)

Quadrants étiquetés :

Haut-Droite : "Priorités" (Haute fréquence + Impact négatif)

Haut-Gauche : "Signaux Émergents" (Basse fréquence + Impact négatif)

Bas-Droite : "Forces" (Haute fréquence + Impact positif)

Bas-Gauche : "Neutre/Faible Impact"

Couleur bulle = gradient sentiment (vert à rouge)

Clic bulle filtre dashboard sur ce thème

Calcul de l’impact

"Impact = % satisfaction thème - % satisfaction globale"

4 Quadrants avec Actions :

🔴 Priorités : Fréquence ≥10%, Impact <0% → Correction urgente

🟠 Signaux Émergents : Fréquence <10%, Impact <0% → Surveillance

🟢 Forces : Fréquence ≥10%, Impact ≥0% → Maintenir/Valoriser

⚪ Neutre : Fréquence <10%, Impact ≥0% → Surveillance passive

Concept Matrice de priorisation ( Warning les courleurs ne sont pas bonnes dans le wireframes)


 

EF-8 : Système de filtrage
Description : Filtrage multi-dimensionnel sur tous composants dashboard.

Critères d'Acceptation :

✓ Catégories filtres :

Date / Canal / Projet / Equipe

Sentiment : Toggles Positif/Neutre/Négatif

Thème : Multi-select depuis arbre taxonomie A voir si on filtre avec une liste d’items

Recherche Texte : Recherche full-text dans verbatims

Bouton "Effacer tous les filtres"

Comptes filtres mis à jour temps réel (ex : "Négatif : 1 234 résultats")

Fonctions administratives
EF-9 : Interface gestion taxonomie - Hors MVP
Description : Configuration self-service des catégories thématiques.

Critères d’acceptation :

Vue arbre hiérarchie taxonomie

Opérations CRUD : Ajouter thème, Éditer nom/description, Supprimer (avec confirmation), Réordonner (drag-and-drop)

Attributs thème :

Nom (max 50 caractères)

Description (max 500 caractères)

Mots-clés/triggers pour auto-classification (optionnel)

Toggle Actif/Inactif

Thème parent (pour hiérarchie)

Concept Admin Taxonomies VOC


 

EF-10 : Contrôle d’accès basé sur rôles
Description : Permissions hiérarchiques pour accès données et configuration.

Critères d’acceptation :

Super Admin : Accès complet + configuration taxonomie, toutes les organisations

Admin : Accès complet + configuration taxonomie, pour organisation liée

Admin Local  : Accès complet + configuration taxonomie, pour équipe(s) liée(s)

Manager : Accès reporting complet en fonction de ses équipe(s) (pas de configuration taxonomie)

Export et partage
MVP - voir si Tableau par défaut

EF-11 Export Excel
Description : Export données structurées pour analyse offline.

EF-12 Génération Rapport PDF
Description : Résumé exécutif pour communication stakeholders.

Notes Architecture Technique

Décision Moteur NLP (Spike Requis) 

Contexte : Rapport TUI existant utilise modèle NLP legacy. LLMs modernes (Claude, Gemini,…) offrent précision supérieure mais coût/latence plus élevés.

https://tersea.atlassian.net/browse/ASSIST-2618Can't find link 

Objectifs Spike :

Benchmark précision classification sentiment

Analyse coût : Coût traitement par verbatim à l'échelle (100K/mois)

Complexité intégration : Fiabilité API, rate limits, gestion erreurs

Critères Décision :

Si amélioration précision >15% ET augmentation coût <30% : Adopter LLM moderne

Si précision similaire OU coût prohibitif : Améliorer modèle TUI existant

Approche hybride : Utiliser LLM pour cas complexes (scores confiance faibles depuis modèle TUI)

Pipeline de Données



Transcription/Email → BD Deskea Evaluate → File Traitement VoC
                                                      ↓
                               ┌──────────────────────┴
                               ↓                                              
                        Analyse Sentiment                          
                          (Moteur NLP / LLM)                           
                               ↓                                              
                               └──────────────────────┬
                                                      ↓
                                        Base de Données Analytics VoC
                                                      ↓
                                          API Dashboard & Exports
Questions & hypothèses
Questions
Temps réel vs. batch : Des clients nécessitent-ils latence <1 heure pour insights ? (Hypothèse : batch suffisant pour MVP)

Intégrations custom : Clients auront-ils besoin accès API pour extraire données VoC dans outils BI externes ? (Pas pour MVP, évaluer demande post-lancement)

Hypothèses
Clients ont qualité transcription 80%+ (prérequis pour analyse sentiment précise)

Infrastructure Deskea Evaluate existante scale aux volumes données VoC (pas de refonte majeure BD nécessaire)

Clients acceptent latence 24 heures pour nouveaux verbatims apparaissant dans dashboards (modèle traitement batch)

Utilisateurs admin à l'aise avec gestion taxonomie self-service (pas de services professionnels requis)

Annexes
Annexe A : Glossaire
Verbatim : Unité individuelle de feedback client (transcription appel téléphonique ou email)

Sentiment : Classification Positif/Neutre/Négatif du ton émotionnel verbatim

Thème : Catégorie taxonomique représentant sujet conversation (ex : "Délai livraison")

Tonalité : Synonyme de sentiment dans contexte VoC