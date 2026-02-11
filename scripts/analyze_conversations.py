# -*- coding: utf-8 -*-
"""
DPD VOC Sentiment Analysis - Deterministic Pipeline
Processes the first 2000 conversations from gramaide.conversations.json
using data-mined keyword sentiment analysis on both summary AND transcript.

Keywords and sentiment indicators are calibrated from real frequency
analysis of 2000 conversation summaries and transcripts.

Usage:
    python scripts/analyze_conversations.py
"""

import json
import os
import re
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, '..')
INPUT_FILE = os.path.join(PROJECT_ROOT, 'sample-data', 'gramaide.conversations.json')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'public', 'mocked-api')
MAX_CONVERSATIONS = 10000


# ─── Sentiment Analysis Engine ───────────────────────────────────────────────

# Weighted negative indicators (word/phrase -> weight)
NEGATIVE_INDICATORS = {
    # Strong negative (weight 3)
    'frustration': 3, 'furieux': 3, 'furieuse': 3, 'scandaleux': 3,
    'inadmissible': 3, "n'importe quoi": 3, 'insulte': 3, 'insulter': 3,
    'inapproprie': 3, 'inacceptable': 3, 'deplorable': 3,
    'mecontentement': 3, 'mecontent': 3, 'mecontente': 3,
    'colere': 3, 'enerve': 3, 'enervee': 3, 'agace': 3,
    'excede': 3, 'excedee': 3, 'exaspere': 3, 'exasperee': 3,
    'vol': 3, 'vole': 3,

    # Medium negative (weight 2)
    'deception': 2, 'decu': 2, 'decue': 2, 'decoit': 2,
    'reclamation': 2, 'litige': 2, 'plainte': 2,
    'retard': 2, 'retards': 2, 'retarde': 2,
    'echoue': 2, 'echec': 2, 'echouee': 2,
    'perdu': 2, 'perte': 2, 'perdue': 2, 'perdus': 2, 'egare': 2,
    'endommage': 2, 'endommagee': 2, 'abime': 2, 'casse': 2, 'defectueux': 2,
    'non livre': 2, 'non recu': 2, 'pas recu': 2, 'pas livre': 2,
    'pas receptionne': 2, 'non receptionne': 2,
    'conteste': 2, 'contestation': 2,
    'probleme recurrent': 2, 'recurrent': 2, 'recurrents': 2,
    'infructueux': 2, 'infructueuse': 2, 'infructueuses': 2,
    'reporte a plusieurs reprises': 2,
    'livraison manquee': 2,
    'erreur': 2,

    # Light negative (weight 1)
    'probleme': 1, 'incident': 1, 'difficulte': 1, 'difficultes': 1,
    'absence': 1, 'absent': 1, 'absente': 1,
    'injoignable': 1,
    'inquietude': 1, 'inquiete': 1, 'inquiet': 1,
    'confusion': 1, 'confus': 1, 'confuse': 1,
    'attente': 1, 'attend depuis': 1,
    'reporte': 1, 'reportee': 1,
    'incomplete': 1, 'incomplet': 1,
    'incorrecte': 1, 'incorrect': 1, 'erronee': 1, 'errone': 1,
    'bloque': 1, 'bloquee': 1,
    'retourne a l\'expediteur': 1,
    'impossible': 1,
}

# Weighted positive indicators
POSITIVE_INDICATORS = {
    # Strong positive (weight 3)
    'satisfait': 3, 'satisfaite': 3, 'satisfaction': 3,
    'remercie': 3, 'remerciement': 3, 'remercier': 3,
    'excellent': 3, 'parfait': 3, 'parfaite': 3,

    # Medium positive (weight 2)
    'resolu': 2, 'resolue': 2, 'resolution': 2,
    'livre avec succes': 2, 'livraison reussie': 2,
    'confirme': 2, 'confirmee': 2, 'confirmation': 2,
    'bien recu': 2, 'bien livre': 2,
    'prise en charge': 2,
    'rassure': 2, 'rassuree': 2,

    # Light positive (weight 1)
    'disponible': 1, 'a confirme': 1,
    'en cours de livraison': 1,
    'organise': 1, 'organisee': 1,
    'clarifie': 1, 'clarification': 1,
    'accepte': 1, 'acceptee': 1,
    'programme': 1, 'programmee': 1,
}

# Neutral/procedural indicators
NEUTRAL_INDICATORS = [
    "s'informer", "demande d'information", "obtenir des informations",
    "statut", "suivi", "verifier", "confirmer",
    "reprogrammer", "reprogrammation", "modifier l'adresse",
    "changement d'adresse", "mise a jour",
]


def normalize_text(text):
    """Normalize French text: lowercase, remove accents for matching."""
    text = text.lower()
    replacements = {
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'à': 'a', 'â': 'a', 'ä': 'a',
        'ù': 'u', 'û': 'u', 'ü': 'u',
        'ô': 'o', 'ö': 'o',
        'î': 'i', 'ï': 'i',
        'ç': 'c', 'œ': 'oe',
    }
    for fr_char, en_char in replacements.items():
        text = text.replace(fr_char, en_char)
    return text


def analyze_sentiment(summary, transcript=''):
    """Analyze sentiment from French summary + transcript. Returns (sentiment, confidence, neg_score, pos_score)."""
    norm_summary = normalize_text(summary)
    norm_transcript = normalize_text(transcript)

    neg_score = 0
    pos_score = 0
    neutral_hits = 0

    # --- Score from SUMMARY (full weight) ---
    for phrase, weight in NEGATIVE_INDICATORS.items():
        count = norm_summary.count(normalize_text(phrase))
        neg_score += count * weight

    for phrase, weight in POSITIVE_INDICATORS.items():
        count = norm_summary.count(normalize_text(phrase))
        pos_score += count * weight

    for phrase in NEUTRAL_INDICATORS:
        if normalize_text(phrase) in norm_summary:
            neutral_hits += 1

    # Special summary patterns
    if re.search(r'exprime?\s+(sa|son)\s+(frustration|mecontentement|colere|deception)', norm_summary):
        neg_score += 4
    if re.search(r'(quatrieme|troisieme|deuxieme|plusieurs)\s+fois', norm_summary):
        neg_score += 2
    if re.search(r'depuis\s+(plusieurs|deux|trois|quatre)\s+(jours|semaines|mois)', norm_summary):
        neg_score += 1
    if 'a plusieurs reprises' in norm_summary:
        neg_score += 2

    # Resolution modifiers in summary
    if re.search(r'(a ete|a confirme|agent a|a informe|a organise|a pris en charge)', norm_summary):
        if neg_score > 0:
            pos_score += 1

    # --- Score from TRANSCRIPT (raw customer voice, data-mined phrases) ---
    if norm_transcript:
        # Transcript negative signals (frequencies from 2000 real conversations)
        transcript_neg = {
            # Strong negative (3) - rare but unambiguous (2-40 occurrences)
            'scandaleux': 3,           # 2x
            'honteux': 3,              # 5x
            'inadmissible': 3,         # 19x
            "n'importe quoi": 3,       # 40x
            'porter plainte': 3,       # 8x
            'degoutee': 3, 'degoute': 3,  # 2x + 4x
            'incompetent': 3,          # 12x
            'cauchemar': 3,            # 2x
            'ras le bol': 3,           # 11x
            'c\'est la honte': 3,

            # Medium negative (2) - moderately frequent signals
            'c\'est pas normal': 2,    # 45x
            'j\'en ai marre': 2,       # 15x
            'incapable': 2,            # 11x
            'je fais comment': 2,      # 36x
            'c\'est nul': 2,           # 6x
            'aucune nouvelle': 2,      # 23x
            'galere': 2,               # 15x
            'catastrophe': 2,          # 7x
            'injoignable': 2,          # 13x
            'c\'est abuser': 2,

            # Light negative (1) - very frequent, weaker signal
            'franchement': 1,          # 98x
            'bloquee': 1,              # 24x
            'bloque': 1,               # 125x (also used in neutral context)
            'pire': 1,                 # 36x
            'pas possible': 0.5,       # 200x (very common, often neutral)
            'souci': 0.5,              # 558x in transcripts (common filler)
        }

        # Transcript positive signals (frequencies from 2000 real conversations)
        transcript_pos = {
            # Strong positive (3) - genuine gratitude
            'c\'est tres gentil': 3,       # 12x
            'vous etes gentil': 3,         # 4x
            'vous etes gentille': 3,       # 3x
            'excellent': 2,                # 33x
            'nickel': 2,                   # 20x
            'genial': 2,                   # 19x

            # Medium positive (1.5) - common but meaningful
            'merci beaucoup': 1.5,         # 543x
            'je vous remercie': 1.5,       # 419x
            'tres bien': 1,                # 439x
            'parfait': 1,                  # 206x
            'super': 1,                    # 197x
            'ca marche': 1,                # 248x

            # Light positive (0.3) - polite closings, not strong sentiment
            'bonne journee': 0.3,          # 563x (routine goodbye)
            'bon courage': 0.3,            # 43x
            'c\'est bon': 0.3,             # 395x (often just acknowledgement)
            # NOTE: 'merci' alone (1670x), 'd'accord' (1375x), 'ok' (1176x),
            # 'au revoir' (1429x) are too frequent/routine to be sentiment signals
        }

        for phrase, weight in transcript_neg.items():
            count = norm_transcript.count(normalize_text(phrase))
            neg_score += count * weight * 0.5  # Half weight from transcript

        for phrase, weight in transcript_pos.items():
            count = norm_transcript.count(normalize_text(phrase))
            pos_score += count * weight * 0.5  # Half weight from transcript

        # Transcript tone patterns
        exclamation_count = transcript.count('!')
        if exclamation_count >= 5:
            neg_score += 1  # Many exclamations suggest agitation

        # Long rants (very long transcript relative to summary = frustrated customer)
        if len(transcript) > 2000 and len(transcript) > len(summary) * 5:
            neg_score += 1

    # Calculate final sentiment
    net_score = pos_score - neg_score

    if net_score >= 2:
        sentiment = 'positive'
        confidence = min(5, 2 + int(pos_score))
    elif net_score <= -2:
        sentiment = 'negative'
        confidence = min(5, 2 + int(neg_score))
    elif neg_score > pos_score and neg_score >= 2:
        sentiment = 'negative'
        confidence = min(5, 1 + int(neg_score))
    elif pos_score > neg_score and pos_score >= 2:
        sentiment = 'positive'
        confidence = min(5, 1 + int(pos_score))
    elif neutral_hits >= 2 or (neg_score <= 1 and pos_score <= 1):
        sentiment = 'neutral'
        confidence = 3
    elif neg_score > pos_score:
        sentiment = 'negative'
        confidence = 2
    else:
        sentiment = 'neutral'
        confidence = 2

    return sentiment, confidence, neg_score, pos_score


# ─── Theme Extraction ────────────────────────────────────────────────────────

THEME_PATTERNS = {
    'Livraison non recue': [
        'non livre', 'pas livre', 'non recu', 'pas recu', 'pas receptionne',
        'non receptionne', 'marque comme livre', 'indique comme livre',
        'colis non livre', 'livraison manquee', 'n\'a pas ete livre',
    ],
    'Retard de livraison': [
        'retard', 'reporte', 'reportee', 'en retard', 'devait etre livre',
        'date de livraison', 'delai', 'attend depuis', 'en attente',
        'pas de nouvelle', 'aucune nouvelle',
    ],
    'Colis endommage': [
        'endommage', 'endommagee', 'abime', 'casse', 'defectueux',
        'defectueuse', 'deteriore', 'deterioree', 'ouvert',
    ],
    'Suivi et Tracking': [
        'suivi', 'tracking', 'numero de suivi', 'statut', 'mise a jour',
        'pas de mise a jour', 'scan', 'information de suivi',
    ],
    'Comportement du livreur': [
        'comportement', 'inapproprie', 'insulte', 'insulter',
        'impoli', 'propos inappropries', 'attitude',
        'n\'a pas attendu', 'n\'a pas sonne', 'pas sonne',
        'refus de monter', 'n\'a pas voulu',
    ],
    'Point relais': [
        'point relais', 'point de retrait', 'relais colis', 'bureau de poste',
        'point relay', 'relais', 'retrait',
    ],
    'Reprogrammation livraison': [
        'reprogramm', 'relivraison', 'nouvelle livraison', 'reprogrammer',
        'nouvelle tentative', 'reporter', 'modifier la date',
        'changement de date', 'prochaine livraison',
    ],
    'Reclamation': [
        'reclamation', 'litige', 'plainte', 'certificat de non-reception',
        'enquete', 'investigation', 'dossier',
    ],
    'Communication et Notifications': [
        'notification', 'sms', 'pas de notification', 'aucune notification',
        'pas ete informe', 'pas recu de notification',
        'pas recu de message', 'pas de nouvelles', 'aucune nouvelle',
        'sans nouvelle', 'pas prevenu', 'contradictoires', 'contradictoire',
        'phishing', 'message suspect',
    ],
    'Adresse incorrecte': [
        'adresse incorrecte', 'adresse erronee', 'mauvaise adresse',
        'erreur d\'adresse', 'adresse incomplete', 'adresse inconnue',
        'changement d\'adresse', 'modifier l\'adresse', 'code postal',
    ],
    'Colis perdu': [
        'perdu', 'perte', 'egare', 'disparu', 'introuvable',
        'retrouv', 'recherch',
    ],
    "Probleme d'acces": [
        'interphone', 'code', 'acces', 'digicode', 'porte',
        'boite aux lettres', 'etage', 'batiment', 'residence',
        'gps', 'localisation',
    ],
    'DPD Pro / B2B': [
        'societe', 'entreprise', 'professionnel',
        'client pro', 'b2b', 'expedition', 'expedier',
        'bordereaux', 'ramasse', 'enlevement', 'collecte',
        'fournisseur', 'magasin', 'boutique en ligne',
    ],
    'Retour de colis': [
        'retour', 'renvoi', 'renvoyer', 'retourne a l\'expediteur',
        'retour expediteur', 'refus', 'refuse',
    ],
}


def extract_themes(summary):
    """Extract up to 3 themes from a conversation summary."""
    norm = normalize_text(summary)
    theme_scores = {}

    for theme, keywords in THEME_PATTERNS.items():
        score = 0
        for kw in keywords:
            count = norm.count(normalize_text(kw))
            score += count
        if score > 0:
            theme_scores[theme] = score

    # Sort by score and return top 3
    sorted_themes = sorted(theme_scores.items(), key=lambda x: x[1], reverse=True)
    return [t[0] for t in sorted_themes[:3]] or ['Service client']


# ─── Keyword Extraction ──────────────────────────────────────────────────────

STOP_WORDS = {
    'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'au', 'aux',
    'et', 'ou', 'mais', 'donc', 'car', 'que', 'qui', 'dont', 'en', 'a',
    'pour', 'par', 'sur', 'avec', 'dans', 'ce', 'cette', 'ces', 'son',
    'sa', 'ses', 'mon', 'ma', 'mes', 'il', 'elle', 'ils', 'elles', 'on',
    'ne', 'pas', 'plus', 'est', 'sont', 'ete', 'avoir', 'etre', 'fait',
    'se', 'si', 'je', 'nous', 'vous', 'leur', 'leurs', 'tout', 'tous',
    'toute', 'toutes', 'apres', 'avant', 'aussi', 'bien', 'comme', 'entre',
    'meme', 'autre', 'autres', 'chez', 'sans', 'sous', 'lors', 'non',
    'oui', 'tres', 'elle', 'lui', 'y', 'avait', 'eu', 'puis', 'pu',
    'etait', 'soit', 'deja', 'encore', 'quand', 'quel', 'quelle',
    'agent', 'client', 'cliente', 'service', 'numero', 'colis', 'contact',
    'contacte', 'dpd', 'france', 'fourni', 'informe', 'informee', 'apres',
    'avoir', 'deux', 'trois', 'premier', 'premiere', 'cas', 'depuis',
    'jour', 'jours', 'fait', 'ainsi', 'suite', 'tandis', 'alors',
}

# Data-driven keyword candidates (mined from 2000 real conversations)
KEYWORD_CANDIDATES = {
    # Core delivery terms (very high frequency in summaries)
    'livraison': 'livraison', 'livre': 'livraison', 'livrer': 'livraison',
    'colis': 'colis',
    'adresse': 'adresse',
    'suivi': 'suivi', 'tracking': 'suivi',

    # Delivery actors (645x livreur, 176x chauffeur, 186x destinataire)
    'livreur': 'livreur', 'chauffeur': 'livreur',
    'destinataire': 'destinataire',
    'expediteur': 'expediteur',

    # Locations (975x agence, 697x relais, 373x domicile, 202x depot)
    'agence': 'agence', 'depot': 'depot',
    'relais': 'point relais', 'point de retrait': 'point relais',
    'domicile': 'domicile',

    # Process terms (230x tentative, 177x reprogrammer, 232x nouvelle livraison)
    'tentative': 'tentative livraison', 'tentatives': 'tentative livraison',
    'reprogramm': 'reprogrammation', 'relivraison': 'reprogrammation',

    # Issues (223x reclamation, 206x retour, 150x retard, 128x erreur)
    'reclamation': 'reclamation', 'litige': 'reclamation',
    'retour': 'retour',
    'retard': 'retard', 'retarde': 'retard',
    'erreur': 'erreur',
    'echec': 'echec livraison',
    'absence': 'absence', 'absent': 'absence',

    # Communication (392x mail, 296x telephone, 172x notification, 137x sms)
    'notification': 'notification', 'sms': 'sms',
    'mail': 'email', 'e-mail': 'email',
    'telephone': 'telephone', 'appel': 'telephone',

    # Tracking & proof (319x statut, 199x confirmation, 75x preuve)
    'statut': 'statut',
    'confirmation': 'confirmation', 'confirme': 'confirmation',
    'preuve': 'preuve livraison',
    'signature': 'signature', 'photo': 'preuve photo',
    'scan': 'scan',

    # Client emotion (206x frustration, 171x mecontentement)
    'frustration': 'frustration', 'mecontentement': 'mecontentement',

    # External partners (293x chronopost, 156x vendeur)
    'chronopost': 'chronopost',
    'amazon': 'amazon',
    'vendeur': 'vendeur',
    'commande': 'commande',

    # Physical delivery details
    'boite aux lettres': 'boite aux lettres',
    'interphone': 'interphone', 'digicode': 'interphone',
    'code': 'code acces',
    'gps': 'gps',
    'poids': 'poids', 'volumineux': 'volumineux',
    'meuble': 'meuble', 'pneu': 'pneus',

    # Schedule terms (346x lundi, 157x samedi, 138x matin, 120x midi)
    'lundi': 'jour ouvre',
    'samedi': 'samedi',
    'matin': 'creneau horaire', 'midi': 'creneau horaire',

    # Key transcript terms (558x souci, 788x probleme)
    'souci': 'souci',
    'probleme': 'probleme',
    'attends': 'attente',
    'galere': 'galere',
}


def extract_keywords(summary, transcript=''):
    """Extract 2-4 relevant keywords from summary + transcript."""
    norm_s = normalize_text(summary)
    norm_t = normalize_text(transcript)
    found = {}

    for trigger, keyword in KEYWORD_CANDIDATES.items():
        norm_trigger = normalize_text(trigger)
        # Summary matches count fully, transcript matches count half
        s_count = norm_s.count(norm_trigger)
        t_count = norm_t.count(norm_trigger)
        total = s_count + t_count * 0.5
        if total > 0:
            found[keyword] = found.get(keyword, 0) + total

    # Sort by frequency and return top 4
    sorted_kw = sorted(found.items(), key=lambda x: x[1], reverse=True)
    return [k[0] for k in sorted_kw[:4]] or ['colis', 'livraison']


# ─── Dashboard Data Generation ──────────────────────────────────────────────

def generate_dashboard_files(conversations, results):
    """Generate all 9 _dpd.json dashboard files."""
    print("\n--- Generating Dashboard Data Files ---")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total = len(results)
    sentiment_counts = Counter()
    theme_sentiment = defaultdict(lambda: {'positive': 0, 'neutral': 0, 'negative': 0, 'total': 0})
    keyword_data = defaultdict(lambda: {'count': 0, 'positive': 0, 'neutral': 0, 'negative': 0})
    monthly_data = defaultdict(lambda: {'volume': 0, 'positive': 0, 'negative': 0, 'neutral': 0})

    site_names = ['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Bordeaux',
                  'Nantes', 'Strasbourg', 'Lille', 'Nice', 'Montpellier',
                  'Rennes', 'Grenoble']
    site_data = defaultdict(lambda: {'total': 0, 'positive': 0, 'neutral': 0, 'negative': 0})

    analyzed_convs = []

    for i, result in enumerate(results):
        sentiment = result['sentiment']
        themes = result['themes']
        keywords = result['keywords']
        confidence = result['confidence']

        sentiment_counts[sentiment] += 1

        # Theme aggregation
        for theme in themes:
            theme_sentiment[theme][sentiment] += 1
            theme_sentiment[theme]['total'] += 1

        # Keyword aggregation
        for kw in keywords:
            keyword_data[kw]['count'] += 1
            keyword_data[kw][sentiment] += 1

        # Timeline: distribute across 12 months (Mar 2025 - Feb 2026)
        bucket = min(int(i * 12 / total), 11)
        month_num = 3 + bucket  # Start from March
        year = 2025 if month_num <= 12 else 2026
        if month_num > 12:
            month_num -= 12
        month_key = '{}-{:02d}'.format(year, month_num)

        monthly_data[month_key]['volume'] += 1
        monthly_data[month_key][sentiment] += 1

        # Site assignment (rotating distribution)
        site = site_names[i % len(site_names)]
        site_data[site]['total'] += 1
        site_data[site][sentiment] += 1

        # Build conversation entry
        conv = conversations[i]
        summary = conv.get('summary', '')
        audio_dur = conv.get('audio_duration', 0)
        dur_min = int(audio_dur // 60) if audio_dur else 0
        dur_sec = int(audio_dur % 60) if audio_dur else 0
        dur_str = '{}:{:02d}'.format(dur_min, dur_sec) if audio_dur else None

        # Date for this conversation
        day = 1 + (i * 3) % 28
        date_str = '{}-{:02d}'.format(month_key, day)

        extract = summary[:200] + ('...' if len(summary) > 200 else '')

        tags = []
        for theme in themes[:2]:
            sent_val = 1.0 if sentiment == 'positive' else (0.0 if sentiment == 'negative' else 0.5)
            tags.append({'label': theme, 'sentiment': sent_val, 'confidence_score': confidence})

        analyzed_convs.append({
            'id': 'conv_{:05d}'.format(i + 1),
            'date': date_str,
            'type': 'call',
            'sentiment': sentiment,
            'extract': extract,
            'themes': themes,
            'fullText': summary[:500],
            'feedbacks': [{
                'feedback_point': extract,
                'text': summary[:400],
                'tags': tags
            }],
            'metadata': {
                'agent_id': 'AGT-{:03d}'.format((i * 7 + 13) % 50 + 1),
                'duration': dur_str,
                'site': site
            }
        })

    pos = sentiment_counts.get('positive', 0)
    neu = sentiment_counts.get('neutral', 0)
    neg = sentiment_counts.get('negative', 0)

    # ─── 1. stats_dpd.json ─────────────────────────────────────────────
    stats = {
        'total': total,
        'positive': pos,
        'neutral': neu,
        'negative': neg,
        'positive_percentage': round(pos / total * 100, 1) if total else 0,
        'neutral_percentage': round(neu / total * 100, 1) if total else 0,
        'negative_percentage': round(neg / total * 100, 1) if total else 0,
    }
    write_json('stats_dpd.json', stats)

    # ─── 2. conversations_dpd.json ─────────────────────────────────────
    write_json('conversations_dpd.json', analyzed_convs)

    # ─── 3. themes_dpd.json ────────────────────────────────────────────
    themes_list = []
    for theme, sent in sorted(theme_sentiment.items(), key=lambda x: x[1]['total'], reverse=True):
        t = sent['total']
        if t < 2:
            continue
        themes_list.append({
            'theme': theme,
            'count': t,
            'sentiment': {
                'positive': sent['positive'],
                'neutral': sent['neutral'],
                'negative': sent['negative']
            },
            'percentage': {
                'positive': round(sent['positive'] / t * 100) if t else 0,
                'neutral': round(sent['neutral'] / t * 100) if t else 0,
                'negative': round(sent['negative'] / t * 100) if t else 0,
            }
        })
    write_json('themes_dpd.json', themes_list)

    # ─── 4. word-cloud_dpd.json ────────────────────────────────────────
    wc_list = []
    for term, data in sorted(keyword_data.items(), key=lambda x: x[1]['count'], reverse=True):
        if data['count'] < 2:
            continue
        wc_list.append({
            'value': term,
            'count': data['count'],
            'sentiment': {
                'positive': data['positive'],
                'neutral': data['neutral'],
                'negative': data['negative']
            }
        })
    write_json('word-cloud_dpd.json', wc_list[:50])

    # ─── 5. timeline_dpd.json ──────────────────────────────────────────
    timeline = []
    for month_key in sorted(monthly_data.keys()):
        d = monthly_data[month_key]
        vol = d['volume']
        if vol == 0:
            continue
        # Satisfaction = (positive + 0.5*neutral) / total * 100
        sat = round(((d['positive'] + d['neutral'] * 0.5) / vol) * 100, 1)
        timeline.append({'month': month_key, 'volume': vol, 'satisfaction': sat})
    write_json('timeline_dpd.json', timeline)

    # ─── 6. kpis_dpd.json ─────────────────────────────────────────────
    top_neg_theme = None
    top_neg_count = 0
    for theme, sent in theme_sentiment.items():
        if sent['negative'] > top_neg_count:
            top_neg_count = sent['negative']
            top_neg_theme = theme

    sat_score = round((pos + neu * 0.5) / total * 100) if total else 0

    kpis = {
        'verbatims_traites': {
            'value': total,
            'trend': 0, 'trend_direction': 'stable',
            'label': 'VERBATIMS TRAITES', 'comparison': 'Analyse de {} conversations DPD'.format(total)
        },
        'score_satisfaction': {
            'value': sat_score, 'unit': '%',
            'trend': 0, 'trend_direction': 'stable',
            'label': 'SCORE SATISFACTION', 'comparison': 'Donnees reelles production'
        },
        'promoteurs': {
            'value': pos,
            'percentage': round(pos / total * 100) if total else 0,
            'label': 'PROMOTEURS'
        },
        'passifs': {
            'value': neu,
            'percentage': round(neu / total * 100) if total else 0,
            'label': 'PASSIFS'
        },
        'detracteurs': {
            'value': neg,
            'percentage': round(neg / total * 100) if total else 0,
            'label': 'DETRACTEURS'
        },
        'theme_prioritaire': {
            'theme': top_neg_theme or 'N/A',
            'mentions': theme_sentiment.get(top_neg_theme, {}).get('total', 0) if top_neg_theme else 0,
            'negative_percentage': round(
                top_neg_count / theme_sentiment.get(top_neg_theme, {}).get('total', 1) * 100
            ) if top_neg_theme else 0,
            'impact': -round(top_neg_count / total * 100) if total else 0,
            'label': 'THEME PRIORITAIRE #1'
        }
    }
    write_json('kpis_dpd.json', kpis)

    # ─── 7. prioritization-matrix_dpd.json ─────────────────────────────
    pmatrix = {
        'global_satisfaction_baseline': sat_score,
        'total_verbatims': total,
        'themes': []
    }
    for theme, sent in sorted(theme_sentiment.items(), key=lambda x: x[1]['total'], reverse=True):
        t = sent['total']
        if t < 3:
            continue
        freq = round(t / total * 100, 1) if total else 0
        neg_pct = round(sent['negative'] / t * 100) if t else 0
        pos_pct = round(sent['positive'] / t * 100) if t else 0
        impact = round((sent['positive'] - sent['negative']) / t * 20) if t else 0

        # Quadrant assignment matching chart layout:
        #   X=frequency (threshold 10%), Y=impact (threshold 0)
        #   high freq + neg impact  → priorities (fix first!)
        #   high freq + pos impact  → strengths  (keep it up)
        #   low freq  + neg impact  → emerging   (watch for growth)
        #   low freq  + pos impact  → neutral    (not a concern)
        if freq >= 10 and impact < 0:
            quadrant = 'priorities'
        elif freq >= 10 and impact >= 0:
            quadrant = 'strengths'
        elif freq < 10 and impact < 0:
            quadrant = 'emerging'
        else:
            quadrant = 'neutral'

        pmatrix['themes'].append({
            'label': theme, 'frequency': freq, 'impact': impact,
            'mentions': t, 'negative_pct': neg_pct, 'positive_pct': pos_pct,
            'quadrant': quadrant
        })
    write_json('prioritization-matrix_dpd.json', pmatrix)

    # ─── 8. channel-comparison_dpd.json ────────────────────────────────
    # Split by call duration: short (<3min) vs long (>=3min)
    short_r, long_r = [], []
    for i, r in enumerate(results):
        dur = conversations[i].get('audio_duration', 0) or 0
        if dur < 180:
            short_r.append(r)
        else:
            long_r.append(r)

    def chan_stats(lst):
        t = len(lst)
        p = sum(1 for r in lst if r['sentiment'] == 'positive')
        ne = sum(1 for r in lst if r['sentiment'] == 'neutral')
        ng = sum(1 for r in lst if r['sentiment'] == 'negative')
        return {
            'total': t, 'positive': p, 'neutral': ne, 'negative': ng,
            'positive_percentage': round(p / t * 100, 1) if t else 0,
            'neutral_percentage': round(ne / t * 100, 1) if t else 0,
            'negative_percentage': round(ng / t * 100, 1) if t else 0,
            'satisfaction_score': round(p / t * 100, 1) if t else 0
        }

    cs = chan_stats(short_r)
    cl = chan_stats(long_r)
    diff = round(abs(cs['satisfaction_score'] - cl['satisfaction_score']), 1)

    channel_comp = {
        'email': cs,  # Short calls mapped to "email" channel for chart compat
        'call': cl,   # Long calls mapped to "call" channel
        'insight': {
            'difference': diff,
            'message': 'Les appels courts <3min ({} conv.) ont {}% de satisfaction vs {}% pour les appels longs ({} conv.). Les appels longs sont lies a des problemes complexes.'.format(
                len(short_r), cs['satisfaction_score'], cl['satisfaction_score'], len(long_r)),
            'recommendation': 'Ameliorer la resolution au premier contact pour reduire la duree des appels et augmenter la satisfaction.'
        }
    }
    write_json('channel-comparison_dpd.json', channel_comp)

    # ─── 9. site-performance_dpd.json ──────────────────────────────────
    site_perf = []
    for sname in site_names:
        d = site_data[sname]
        t = d['total']
        site_perf.append({
            'site': sname, 'total': t,
            'positive': d['positive'], 'neutral': d['neutral'], 'negative': d['negative'],
            'satisfaction_percentage': round(d['positive'] / t * 100, 1) if t else 0,
            'volume': t
        })
    write_json('site-performance_dpd.json', site_perf)

    # ─── Summary ───────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print("  Total conversations: {}".format(total))
    print("  Positive: {:>4} ({:5.1f}%)".format(pos, pos / total * 100))
    print("  Neutral:  {:>4} ({:5.1f}%)".format(neu, neu / total * 100))
    print("  Negative: {:>4} ({:5.1f}%)".format(neg, neg / total * 100))
    print("  Satisfaction score: {}%".format(sat_score))
    print("  Themes detected: {}".format(len(themes_list)))
    print("  Keywords extracted: {}".format(min(50, len(wc_list))))
    print("  Top negative theme: {} ({} neg mentions)".format(top_neg_theme, top_neg_count))
    print("  Short calls (<3m): {} | Long calls (>=3m): {}".format(len(short_r), len(long_r)))
    print("  Output: {}".format(OUTPUT_DIR))
    print("=" * 60)
    print("\n  All 9 _dpd.json files generated successfully!")


def write_json(filename, data):
    """Write data to JSON file in the output directory."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("  -> {}".format(filename))


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  DPD VOC - Sentiment Analysis Pipeline")
    print("  (Deterministic - first {} conversations)".format(MAX_CONVERSATIONS))
    print("=" * 60)

    # Load data
    print("\n--- Loading Data ---")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        all_convs = json.load(f)
    conversations = all_convs[:MAX_CONVERSATIONS]
    print("  Loaded {} conversations (from {} total)".format(len(conversations), len(all_convs)))

    # Analyze each conversation (using both summary + transcript)
    print("\n--- Analyzing Sentiments & Themes (summary + transcript) ---")
    results = []
    for i, conv in enumerate(conversations):
        summary = conv.get('summary', '') or ''
        transcript = conv.get('transcript_speaker_1', '') or ''
        sentiment, confidence, neg_score, pos_score = analyze_sentiment(summary, transcript)
        themes = extract_themes(summary)
        keywords = extract_keywords(summary, transcript)

        results.append({
            'sentiment': sentiment,
            'confidence': confidence,
            'themes': themes,
            'keywords': keywords,
        })

        if i < 10 or i % 50 == 0:
            print("  [{:>3}] {} (conf:{}) neg={} pos={} themes={}".format(
                i, sentiment.upper().ljust(8), confidence, neg_score, pos_score, themes[:2]))

    # Summary of sentiments
    sc = Counter(r['sentiment'] for r in results)
    print("\n  Analysis complete:")
    print("    Positive: {}  Neutral: {}  Negative: {}".format(
        sc.get('positive', 0), sc.get('neutral', 0), sc.get('negative', 0)))

    # Generate dashboard files
    print("\n--- Generating Dashboard Files ---")
    generate_dashboard_files(conversations, results)


if __name__ == '__main__':
    main()
