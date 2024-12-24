import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import xgboost as xgb
import numpy as np
import pandas as pd
import torch
from transformers import BertModel ,BertTokenizer
from data.cleaning import remove_punctuation ,clean_text
import texthero as hero
import nltk
#charger le corpus de stopwords
nltk.download('stopwords')

# Initialisation du modèle et de FastAPI
app = FastAPI()

# Charger le modèle XGBoost
model_path = "model.json"
xgb_model = xgb.Booster()
xgb_model.load_model(model_path)

# Charger le tokenizer (exemple avec BERT, à ajuster selon votre pipeline)
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
embed_model = BertModel.from_pretrained("bert-base-uncased")

# Structure des données envoyées
class Question(BaseModel):
    user_id: int
    title: str
    reputation: int
    answer_count: int
    body: str


# Remplacer la fonction remove_punctuation de Texthero
hero.preprocessing.remove_punctuation = remove_punctuation

# Fonction pour transformer les données
def prepare_data(question: Question):
    text=""
    Text = question.title + " " + question.body
    Text=clean_text(Text)
    # Maintenant, utiliser hero.clean pour nettoyer le texte
    Text = pd.Series([Text])  # Convertit une chaîne en Series
    Text= hero.clean(Text)
    Text_Length = Text.apply(lambda x: len(x.split()))
    #Generer les tokens et embeddings du la variable Text
    #Generer les tokens
    text= str(Text.iloc[0])
    tokens = tokenizer(text, padding=True, max_length=64, truncation=True, return_tensors="pt")
    # Génération des embeddings
    with torch.no_grad():
        embeddings = embed_model(**tokens).last_hidden_state.mean(dim=1)
    #Transformer les colonnes numeriques
    num_feat = torch.tensor([[question.reputation,question.answer_count,Text_Length]], dtype=torch.float32)
    comb_feat = torch.cat([embeddings, num_feat], dim=1)
    return tokens, comb_feat,num_feat

# Fonction pour effectuer une prédiction
def predict_class(question: Question):
    _, comb_feat,_ = prepare_data(question)
    dmatrix = xgb.DMatrix(data=comb_feat)
    prediction = xgb_model.predict(dmatrix)
    predicted_class = np.argmax(prediction)
    return predicted_class

# Endpoint pour effectuer des prédictions
@app.post("/predict")
def predict_new_question(question: Question):
    classe=""
    predicted_class = predict_class(question)
    if predicted_class==0:
        classe="Open"
    if predicted_class==1:
        classe="Not suitable for this site"
    if predicted_class==2:
        classe="Needs details or clarity"
    if predicted_class==3:
        classe="Needs more focus"
    if predicted_class==4:
        classe="Duplicate"
    if predicted_class==5:
        classe="Opinion-based"

    return {"user_id": question.user_id, "Class": classe}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)



