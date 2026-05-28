import pandas as pd
import plotly.express as px

# VOTRE LIEN DE PUBLICATION GOOGLE SHEET CSV
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRT_moHbxSD2GZ7lygIo_aXIXs5PlzD5WNNd8HuM6kz4_dc4YIO1Br9mx4yMkdfjVEasP1rrRwqO1Mi/pub?gid=1803115037&single=true&output=csv"

def main():
    try:
        # 1. Lecture des données
        df = pd.read_csv(SHEET_CSV_URL)
        
        # Nettoyage des espaces vides dans les noms de colonnes
        df.columns = df.columns.str.strip()
        print("Colonnes détectées dans votre fichier :", list(df.columns))

        # 2. Détection automatique des colonnes
        # On prend la première colonne pour l'axe X (Date) et la deuxième pour l'axe Y (Prix)
        colonne_x = df.columns[0]
        colonne_y = df.columns[1]
        
        print(f"Utilisation de '{colonne_x}' pour les dates et '{colonne_y}' pour les prix.")

        # Convertir la colonne X en vraies dates
        df[colonne_x] = pd.to_datetime(df[colonne_x])
        df = df.sort_values(colonne_x)

        # 3. Création du graphique interactif
        fig = px.line(df, x=colonne_x, y=colonne_y, title='Daily Gas Spot Price')
        
        fig.update_layout(
            template='plotly_white',
            xaxis_title=colonne_x,
            yaxis_title=colonne_y
        )

        # 4. Sauvegarde en HTML
        fig.write_html('index.html', include_plotlyjs='cdn')
        print("Graphique interactif généré avec succès sous le nom 'index.html'.")
        
    except Exception as e:
        print(f"ERREUR CRITIQUE : {e}")
        exit(1)

if __name__ == "__main__":
    main()
