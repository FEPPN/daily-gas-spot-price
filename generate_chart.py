import pandas as pd
import plotly.express as px

# VOTRE LIEN DE PUBLICATION GOOGLE SHEET CSV
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRT_moHbxSD2GZ7lygIo_aXIXs5PlzD5WNNd8HuM6kz4_dc4YIO1Br9mx4yMkdfjVEasP1rrRwqO1Mi/pub?gid=1803115037&single=true&output=csv"

def main():
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')

        # Création d'un graphique interactif avec Plotly
        fig = px.line(df, x='Date', y='Valeur', title='Données en temps réel')
        
        # Personnalisation rapide du style
        fig.update_layout(
            template='plotly_white',
            xaxis_title='Dates',
            yaxis_title='Valeurs'
        )

        # SAUVEGARDE EN HTML (au lieu de PNG)
        fig.write_html('index.html', include_plotlyjs='cdn')
        print("Graphique interactif généré sous le nom 'index.html'.")
        
    except Exception as e:
        print(f"Erreur : {e}")
        exit(1)

if __name__ == "__main__":
    main()
