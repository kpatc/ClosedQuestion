import re
import pandas as pd
from bs4 import BeautifulSoup
import re
import string

#Fonction de nettoyage de texte brute scrapper
def clean_text(text):
    if pd.isna(text):  # Gerer les valeurs manquantes
        return text
    
    # Supprimer les balises HTML en gardant seulement le texte brut
    text_without_html = BeautifulSoup(text, "html.parser").get_text()

    # Supprimer les blocs de code (entre backticks et dans <code></code>)
    text_without_code = re.sub(r"```.*?```", "", text_without_html, flags=re.DOTALL)  # Code entre backticks
    text_without_code = re.sub(r"<code>.*?</code>", "", text_without_code, flags=re.DOTALL)  # Code dans <code></code>

    # Supprimer les URL (commencent par http:// ou https://)
    text_without_urls = re.sub(r"http[s]?://\S+", "", text_without_code)

    # Supprimer les hashtags (#) et mentions (@)
    text_without_hashtags_mentions = re.sub(r"#\S+", "", text_without_urls)  # Hashtags
    text_cleaned = re.sub(r"@\S+", "", text_without_hashtags_mentions)  # Mentions

    # Supprimer les espaces superflus
    text_cleaned = re.sub(r"\s+", " ", text_cleaned).strip()
    return text_cleaned

def remove_punctuation(input):
    RE_PUNCT = re.compile(r'([%s])+' % re.escape(string.punctuation), re.UNICODE)
    return input.str.replace(RE_PUNCT, " ", regex=True)
