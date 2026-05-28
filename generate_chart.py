import pandas as pd
import plotly.graph_objects as go
import plotly.offline as offline

# ⚠️ VOTRE LIEN DE PUBLICATION GOOGLE SHEET CSV (NE PAS MODIFIER)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRT_moHbxSD2GZ7lygIo_aXIXs5PlzD5WNNd8HuM6kz4_dc4YIO1Br9mx4yMkdfjVEasP1rrRwqO1Mi/pub?gid=1803115037&single=true&output=csv"

# Configuration personnalisée du graphique (Copier textuellement ce bloc)
CHART_CONFIG = {
    'title_main': 'Historique des prédictions du prix du kWh TTC au TRVE résidentiel en 2026',
    'title_sub': 'Evolution de l\'estimation depuis janvier 2025',
    'unit': ' € / kWh TTC',
    'color_line': 'rgba(100, 116, 230, 1)', # Bleu ligne
    'color_fill': 'rgba(230, 233, 253, 1)', # Bleu très clair fond
    'color_hover_border': 'rgba(215, 219, 233, 1)' # Gris bordure infobulle
}

def main():
    try:
        # 1. Lecture et nettoyage des données
        df = pd.read_csv(SHEET_CSV_URL)
        df.columns = df.columns.str.strip()
        print("Colonnes détectées :", list(df.columns))

        # 2. Détection automatique des colonnes
        col_x = df.columns[0]
        col_y = df.columns[1]
        print(f"Axe X : '{col_x}', Axe Y : '{col_y}'.")

        # 3. Formatage des données
        df[col_x] = pd.to_datetime(df[col_x], dayfirst=True)
        df = df.sort_values(col_x)
        # S'assurer que Y est bien numérique
        df[col_y] = pd.to_numeric(df[col_y])

        # ==============================================================================
        # CONSTRUCTION DU GRAPHIQUE VISUEL
        # ==============================================================================
        fig = go.Figure()

        # A. Création de la ligne avec zone remplie (Area Chart)
        fig.add_trace(go.Scatter(
            x=df[col_x],
            y=df[col_y],
            mode='lines',
            name='', # Supprime le nom de la série par défaut
            
            # Personnalisation de la ligne (Style & Couleur)
            line=dict(
                color=CHART_CONFIG['color_line'], 
                width=3, # Épaisseur
                shape='spline', # Ligne lissée pour un effet "tendance"
                smoothing=1.3 # Niveau de lissage
            ),
            
            # Personnalisation de la zone remplie
            fill='tozeroy', # Remplit jusqu'à l'axe zéro (Area chart)
            fillcolor=CHART_CONFIG['color_fill'],
            
            # Personnalisation de l'infobulle (HoverLabel)
            # Format: 'Date\n<icône_carré> Valeur Unité'
            hovertemplate='%{x|%d/%m/%Y}<br>' + # Date formatée (JJ/MM/AAAA)
                          '<span style="color:' + CHART_CONFIG['color_line'] + ';">&#9634;</span> ' + # Icône carrée bleue
                          '%{y:.4f}' + CHART_CONFIG['color_y_unit'] # Valeur formatée (.4 décimales) et unité
        ))

        # B. Personnalisation de l'Apparence Global et des Axes
        fig.update_layout(
            # Style & Arrière-plan
            plot_bgcolor='white', # Fond du graphique blanc
            paper_bgcolor='white', # Fond de la page blanc
            margin=dict(l=10, r=10, t=90, b=10), # Marges affinées pour WordPress
            
            # Titres personnalisés (Principal & Secondaire)
            title=dict(
                text=f"<span style='font-size: 24px; font-weight: bold;'>{CHART_CONFIG['title_main']}</span><br>"
                     f"<span style='font-size: 16px; color: #7f8c8d; font-weight: normal;'>{CHART_CONFIG['title_sub']}</span>",
                x=0.5, # Titre centré
                y=0.96, # Ajustement vertical
                xanchor='center'
            ),
            
            # Personnalisation de l'Axe X (Dates)
            xaxis=dict(
                showgrid=True, # Affiche la grille
                gridcolor='#f0f0f0', # Grille très claire
                linecolor='#e0e0e0', # Ligne de l'axe
                tickformat='%m/%y', # Format des étiquettes d'axe (MM/YY)
                dtick='M3' # Une étiquette tous les 3 mois
            ),
            
            # Personnalisation de l'Axe Y (Prix)
            yaxis=dict(
                showgrid=True, 
                gridcolor='#f0f0f0', 
                tickformat='.4f', # Affiche .4 décimales sur l'axe
                ticksuffix=CHART_CONFIG['color_y_unit'], # Ajoute l'unité après chaque chiffre d'axe
                side='left' # Axe à gauche
            ),
            
            # Style personnalisé pour l'infobulle (HoverLabel)
            hoverlabel=dict(
                bgcolor='white', # Fond de l'infobulle blanc
                font_size=13,
                font_family='Arial, sans-serif',
                bordercolor=CHART_CONFIG['color_hover_border'] # Couleur de la bordure grise
            )
        )

        # 4. Sauvegarde du fichier HTML
        offline.plot(fig, filename='index.html', auto_open=False, include_plotlyjs='cdn')
        print("Graphique visuel généré avec succès.")
        
    except Exception as e:
        print(f"ERREUR : {e}")
        exit(1)

# Petite correction sur les clés de configuration pour éviter une erreur
CHART_CONFIG['color_y_unit'] = CHART_CONFIG['unit']

if __name__ == "__main__":
    main()
