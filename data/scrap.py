import requests
from datetime import datetime
import pandas as pd

# Paramètres de l'API
filter_id = "!nNPvSNPI7A"
url = "https://api.stackexchange.com/2.3/questions"
params = {
    "order": "desc",
    "filter": filter_id,
    "sort": "creation",
    "site": "stackoverflow",
    "pagesize": 100,  # Maximum autorisé par l'API
}
max_pages = 100  # Nombre maximum de pages à parcourir
questions_data = []  # Liste pour stocker toutes les données

for page in range(1, max_pages + 1):
    params["page"] = page  # Ajouter le paramètre de page
    response = requests.get(url, params=params)

    # Vérification de la réponse
    if response.status_code != 200:
        print(f"Erreur : {response.status_code} - {response.text}")
        break

    data = response.json()

    # Vérifier si le quota est épuisé
    if data.get("quota_remaining", 0) == 0:
        print("Quota API épuisé. Veuillez réessayer plus tard.")
        break

    # Ajouter les données de chaque page
    for question in data['items']:
        question_id = question.get('question_id', 'N/A')
        creation_date = question.get('creation_date', 'N/A')
        owner_user_id = question.get('owner', {}).get('user_id', 'N/A')
        reputation = question.get('owner', {}).get('reputation', 'N/A')
        accept_rate = question.get('owner', {}).get('accept_rate', 'N/A')
        tags = question.get('tags', [])
        is_answered = question.get('is_answered', 'N/A')
        view_count = question.get('view_count', 'N/A')
        answer_count = question.get('answer_count', 'N/A')
        score = question.get('score', 'N/A')
        last_activity_date = question.get('last_activity_date', 'N/A')
        title = question.get('title', 'N/A')
        body = question.get('body', 'N/A')
        open_status = 'open' if 'closed_date' not in question else question.get('closed_reason', 'not provided')

        # Conversion des dates
        if creation_date != 'N/A':
            creation_date = datetime.utcfromtimestamp(creation_date).strftime('%Y-%m-%d %H:%M:%S')
        if last_activity_date != 'N/A':
            last_activity_date = datetime.utcfromtimestamp(last_activity_date).strftime('%Y-%m-%d %H:%M:%S')

        # Ajouter les données à la liste
        questions_data.append({
            "QuestionId": question_id,
            "CreationDate": creation_date,
            "OwnerUserId": owner_user_id,
            "Reputation": reputation,
            "AcceptRate": accept_rate,
            "Tags": ", ".join(tags),
            "IsAnswered": is_answered,
            "ViewCount": view_count,
            "AnswerCount": answer_count,
            "Score": score,
            "LastActivityDate": last_activity_date,
            "Title": title,
            "Body": body,
            "OpenStatus": open_status
        })

    # Arrêter si nous avons atteint la dernière page
    if not data.get("has_more", False):
        break

# Créer un DataFrame avec toutes les données
df = pd.DataFrame(questions_data)

# Séparer les questions ouvertes et fermées
df_open = df[df['OpenStatus'] == 'open']
df_closed = df[df['OpenStatus'] != 'open']

# Afficher un résumé
print(f"Nombre total de questions récupérées : {len(df)}")
print(f"Questions ouvertes : {len(df_open)}")
print(f"Questions fermées : {len(df_closed)}")

# Enregistrer les résultats (optionnel)
df.to_csv("st_questions_data.csv", index=False)
print("Les données ont été enregistrées dans 'questions_data.csv'.")
