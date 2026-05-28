import pandas as pd
import plotly.graph_objects as go
import plotly.offline as offline

# VOTRE LIEN DE PUBLICATION GOOGLE SHEET CSV
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRT_moHbxSD2GZ7lygIo_aXIXs5PlzD5WNNd8HuM6kz4_dc4YIO1Br9mx4yMkdfjVEasP1rrRwqO1Mi/pub?gid=1803115037&single=true&output=csv"

# Configuration graphique stricte
CHART_CONFIG = {
    'title_main': 'Historique des prédictions du prix du kWh TTC au TRVE résidentiel en 2026',
    'title_sub': 'Evolution de l\'estimation depuis janvier 2025',
    'unit': ' € / kWh TTC',
    'color_line': '#4d5dfb',     # Bleu roi dynamique pour la ligne principale
    'color_fill': '#f0f2ff',     # Teinte bleutée très douce pour l'arrière-plan de zone
    'color_grid': '#f5f5f5'      # Gris ultra-léger pour les lignes de repère
}

def main():
    try:
        # 1. Chargement des données
        df = pd.read_csv(SHEET_CSV_URL)
        df.columns = df.columns.str.strip()
        
        col_x = df.columns[0]
        col_y = df.columns[1]

        # 2. Nettoyage et tri chronologique
        df[col_x] = pd.to_datetime(df[col_x], dayfirst=True)
        df = df.sort_values(col_x)
        df[col_y] = pd.to_numeric(df[col_y])

        # 3. Génération du graphique de type "Aire Remplie"
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df[col_x],
            y=df[col_y],
            mode='lines',
            line=dict(
                color=CHART_CONFIG['color_line'], 
                width=2.5,
                shape='spline',    # Rend la courbe parfaitement fluide et lissée
                smoothing=0.8
            ),
            fill='tozeroy',        # Active le remplissage de zone sous la courbe
            fillcolor=CHART_CONFIG['color_fill'],
            hovertemplate='%{x|%d/%m/%Y}<br><span style="color:' + CHART_CONFIG['color_line'] + ';">&#9634;</span> %{y:.4f}' + CHART_CONFIG['unit'],
            name=''
        ))

        # 4. Ajustement fin du layout visuel (Titres, Grilles, Marges)
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=50, r=20, t=90, b=40),
            title=dict(
                text=f"<span style='font-size: 22px; font-weight: bold; font-family: Arial;'>{CHART_CONFIG['title_main']}</span><br>"
                     f"<span style='font-size: 15px; color: #7f8c8d; font-family: Arial;'>{CHART_CONFIG['title_sub']}</span>",
                x=0.5,
                y=0.95,
                xanchor='center'
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor=CHART_CONFIG['color_grid'],
                linecolor='#e0e0e0',
                tickformat='%m/%y',
                dtick='M2'         # Un repère de date tous les 2 mois pour aérer l'axe
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor=CHART_CONFIG['color_grid'],
                tickformat='.4f',
                ticksuffix=CHART_CONFIG['unit']
            ),
            hoverlabel=dict(
                bgcolor='white',
                font_size=13,
                bordercolor='#d7dbe9'
            )
        )

        # 5. Exportation physique
        offline.plot(fig, filename='index.html', auto_open=False, include_plotlyjs='cdn')
        print("Nouveau design appliqué avec succès dans index.html.")
        
    except Exception as e:
        print(f"ERREUR : {e}")
        exit(1)

if __name__ == "__main__":
    main()
