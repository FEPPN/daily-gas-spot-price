import pandas as pd
import matplotlib.pyplot as plt

# REMPLACEZ LE LIEN CI-DESSOUS PAR VOTRE LIEN DE PUBLICATION GOOGLE SHEET CSV
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRT_moHbxSD2GZ7lygIo_aXIXs5PlzD5WNNd8HuM6kz4_dc4YIO1Br9mx4yMkdfjVEasP1rrRwqO1Mi/pub?gid=1803115037&single=true&output=csv"

def main():
    try:
        # 1. Lecture des données depuis le lien Google Sheets
        df = pd.read_csv(SHEET_CSV_URL)
        
        # 2. Nettoyage basique (Adapter 'Date' et 'Valeur' aux noms exacts de vos colonnes)
        # Si vos colonnes s'appellent "Jour" et "Total", remplacez les mots ci-dessous.
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')

        # 3. Construction graphique
        plt.figure(figsize=(10, 5))
        plt.plot(df['Date'], df['Valeur'], marker='o', color='#2ea44f', linewidth=2)
        
        plt.title('Mise à jour automatique des données', fontsize=14, fontweight='bold')
        plt.xlabel('Dates', fontsize=12)
        plt.ylabel('Valeurs', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # 4. Sauvegarde de l'image dans le dépôt
        plt.savefig('graphique.png', dpi=150)
        print("Le graphique a été généré avec succès sous le nom 'graphique.png'.")
        
    except Exception as e:
        print(f"Erreur lors de la génération : {e}")
        exit(1)

if __name__ == "__main__":
    main()
