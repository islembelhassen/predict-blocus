# Projet MLOps - Prédiction du risque de blocus étudiant

## Objectif

Calculer un score de risque de blocus (%) pour une université à partir de plusieurs sources de données.

Interprétation :

- 0-30 % : risque faible
- 30-60 % : risque moyen
- 60-85 % : risque élevé
- > 85 % : blocus très probable / quasi confirmé

---

# Sources V1 du projet

| # | Source | Lien |
|---|---|---|
| 1 | X / Twitter | https://x.com |
| 2 | Telegram Info Blocage France | https://t.me/s/infoblocagefrance1 |
| 3 | Telegram Gilets Jaunes Gen Z | https://t.me/s/GiletsJaunesGenZ |
| 4 | Sites officiels des universités | universite-paris-saclay.fr, sorbonne-universite.fr, univ-rennes.fr |
| 5 | UNEF | https://www.unef.fr |
| 6 | Union Étudiante | https://unionetudiante.fr |
| 7 | France24 | https://www.france24.com/fr |
| 8 | Google News | https://news.google.com |

---

# Architecture finale recommandée

```text
Sources (8)

Telegram
Twitter/X
Google News
UNEF
Union Étudiante
Sites Universités
France24
Le Monde Campus (source optionnelle V2)

        │
        ▼

Scrapy + Telethon
        │
        ▼

Airflow
        │
        ▼

PostgreSQL
        │
        ▼

spaCy
(NLP + extraction)
        │
        ▼

Feature Engineering
        │
        ▼

XGBoost
        │
        ▼

MLflow
        │
        ▼

FastAPI
        │
        ▼

Streamlit Dashboard
```

---

# Stack technique retenue

- Python 3.12
- Scrapy
- BeautifulSoup
- Telethon
- Apache Airflow
- PostgreSQL
- DuckDB
- spaCy
- XGBoost
- MLflow
- FastAPI
- Docker
- Streamlit

---

# Schéma simplifié du dataset

```text
date
university
telegram_mentions
twitter_mentions
news_articles_count
unef_posts
union_etudiante_posts
university_alerts
sentiment_score
risk_score
```

---

# Sortie du modèle

```json
{
  "date": "2026-11-25",
  "university": "Rennes 2",
  "risk_score": 87.4,
  "status": "Très probable"
}
```
