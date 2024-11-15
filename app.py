import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Configuration de la page
st.set_page_config(page_title="EDS-R Naming Tool", layout="wide")

# Initialisation des données dans la session state
if 'acronyms' not in st.session_state:
    st.session_state.acronyms = pd.DataFrame(columns=[
        'acronym', 'signification', 'cellule', 'date_ajout'
    ])

if 'evaluations' not in st.session_state:
    st.session_state.evaluations = pd.DataFrame(columns=[
        'acronym', 'evaluator', 'datetime',
        # Critères fonctionnels (25%)
        'fonc_prononciation', 'fonc_international', 'fonc_simplicite', 'fonc_non_ambiguite',
        # Critères scientifiques (25%)
        'sci_credibilite', 'sci_pertinence', 'sci_image',
        # Critères identitaires (20%)
        'id_representation', 'id_adequation', 'id_perennite',
        # Critères communication (20%)
        'com_force', 'com_facilite', 'com_impact',
        # Critères techniques (10%)
        'tech_donnees', 'tech_eds', 'tech_pertinence',
        # Score final
        'score_final'
    ])
# Fonctions utilitaires
def calculate_weighted_score(row):
    # Moyennes par dimension
    fonc_score = np.mean([row['fonc_prononciation'], row['fonc_international'], 
                         row['fonc_simplicite'], row['fonc_non_ambiguite']]) * 0.25
    sci_score = np.mean([row['sci_credibilite'], row['sci_pertinence'], 
                        row['sci_image']]) * 0.25
    id_score = np.mean([row['id_representation'], row['id_adequation'], 
                       row['id_perennite']]) * 0.20
    com_score = np.mean([row['com_force'], row['com_facilite'], 
                        row['com_impact']]) * 0.20
    tech_score = np.mean([row['tech_donnees'], row['tech_eds'], 
                         row['tech_pertinence']]) * 0.10
    
    return (fonc_score + sci_score + id_score + com_score + tech_score) * 100

def create_radar_chart(acronym_data):
    categories = ['Fonctionnel', 'Scientifique', 'Identitaire', 
                 'Communication', 'Technique']
    
    # Calcul des moyennes par dimension
    fonc = np.mean([acronym_data['fonc_prononciation'], acronym_data['fonc_international'], 
                    acronym_data['fonc_simplicite'], acronym_data['fonc_non_ambiguite']])
    sci = np.mean([acronym_data['sci_credibilite'], acronym_data['sci_pertinence'], 
                   acronym_data['sci_image']])
    id = np.mean([acronym_data['id_representation'], acronym_data['id_adequation'], 
                  acronym_data['id_perennite']])
    com = np.mean([acronym_data['com_force'], acronym_data['com_facilite'], 
                   acronym_data['com_impact']])
    tech = np.mean([acronym_data['tech_donnees'], acronym_data['tech_eds'], 
                    acronym_data['tech_pertinence']])
    
    values = [fonc, sci, id, com, tech]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=acronym_data['acronym']
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )),
        showlegend=True
    )
    
    return fig
  # Interface principale
def main():
    st.title("Outil d'évaluation des noms EDS-R")
    
    # Menu de navigation
    menu = ["Accueil", "Ajout Propositions", "Évaluation", "Résultats"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Accueil":
        show_home()
    elif choice == "Ajout Propositions":
        show_add_acronym()
    elif choice == "Évaluation":
        show_evaluation()
    elif choice == "Résultats":
        show_results()

def show_home():
    st.header("Bienvenue dans l'outil d'évaluation des noms EDS-R")
    st.write("""
    Cet outil permet de :
    - Ajouter de nouvelles propositions de noms
    - Évaluer les propositions selon les critères définis
    - Visualiser les résultats en temps réel
    """)
    
    # Afficher les statistiques
    st.subheader("Statistiques actuelles")
    st.write(f"Nombre de propositions : {len(st.session_state.acronyms)}")
    st.write(f"Nombre d'évaluations : {len(st.session_state.evaluations)}")

def show_add_acronym():
    st.header("Ajouter une nouvelle proposition")
    
    with st.form("add_acronym_form"):
        acronym = st.text_input("Acronyme")
        signification = st.text_input("Signification complète")
        cellule = st.selectbox("Cellule", 
                             ["Méthodologie", "Promotion", "Investigation", "Intercellule"])
        
        submitted = st.form_submit_button("Ajouter")
        if submitted and acronym and signification:
            new_acronym = pd.DataFrame({
                'acronym': [acronym],
                'signification': [signification],
                'cellule': [cellule],
                'date_ajout': [datetime.now()]
            })
            st.session_state.acronyms = pd.concat([st.session_state.acronyms, new_acronym], 
                                                ignore_index=True)
            st.success(f"Acronyme {acronym} ajouté avec succès!")
          def show_evaluation():
    st.header("Évaluation des propositions")
    
    if len(st.session_state.acronyms) == 0:
        st.warning("Aucune proposition à évaluer. Ajoutez d'abord des propositions.")
        return
    
    evaluator = st.text_input("Votre nom")
    acronym = st.selectbox("Choisir un acronyme à évaluer", 
                          st.session_state.acronyms['acronym'].tolist())
    
    if evaluator and acronym:
        signification = st.session_state.acronyms[
            st.session_state.acronyms['acronym'] == acronym
        ]['signification'].iloc[0]
        st.write(f"Signification : {signification}")
        
        with st.form("evaluation_form"):
            st.subheader("Critères fonctionnels (25%)")
            fonc_prononciation = st.slider("Facilité prononciation/mémorisation", 1, 5, 3)
            fonc_international = st.slider("Potentiel international", 1, 5, 3)
            fonc_simplicite = st.slider("Simplicité d'utilisation", 1, 5, 3)
            fonc_non_ambiguite = st.slider("Non-ambiguïté", 1, 5, 3)
            
            st.subheader("Critères scientifiques (25%)")
            sci_credibilite = st.slider("Crédibilité académique", 1, 5, 3)
            sci_pertinence = st.slider("Pertinence recherche", 1, 5, 3)
            sci_image = st.slider("Image professionnelle", 1, 5, 3)
            
            st.subheader("Critères identitaires (20%)")
            id_representation = st.slider("Représentation GHICL", 1, 5, 3)
            id_adequation = st.slider("Adéquation mission", 1, 5, 3)
            id_perennite = st.slider("Pérennité", 1, 5, 3)
            
            st.subheader("Critères communication (20%)")
            com_force = st.slider("Force évocatrice", 1, 5, 3)
            com_facilite = st.slider("Facilité d'explication", 1, 5, 3)
            com_impact = st.slider("Impact potentiel", 1, 5, 3)
            
            st.subheader("Critères techniques (10%)")
            tech_donnees = st.slider("Lien avec les données", 1, 5, 3)
            tech_eds = st.slider("Évocation EDS", 1, 5, 3)
            tech_pertinence = st.slider("Pertinence technique", 1, 5, 3)
            
            submitted = st.form_submit_button("Soumettre l'évaluation")
            if submitted:
                new_evaluation = pd.DataFrame({
                    'acronym': [acronym],
                    'evaluator': [evaluator],
                    'datetime': [datetime.now()],
                    'fonc_prononciation': [fonc_prononciation],
                    'fonc_international': [fonc_international],
                    'fonc_simplicite': [fonc_simplicite],
                    'fonc_non_ambiguite': [fonc_non_ambiguite],
                    'sci_credibilite': [sci_credibilite],
                    'sci_pertinence': [sci_pertinence],
                    'sci_image': [sci_image],
                    'id_representation': [id_representation],
                    'id_adequation': [id_adequation],
                    'id_perennite': [id_perennite],
                    'com_force': [com_force],
                    'com_facilite': [com_facilite],
                    'com_impact': [com_impact],
                    'tech_donnees': [tech_donnees],
                    'tech_eds': [tech_eds],
                    'tech_pertinence': [tech_pertinence]
                })
                new_evaluation['score_final'] = calculate_weighted_score(new_evaluation.iloc[0])
                st.session_state.evaluations = pd.concat([st.session_state.evaluations, new_evaluation], 
                                                       ignore_index=True)
                st.success("Évaluation enregistrée avec succès!")

def show_results():
    st.header("Résultats des évaluations")
    
    if len(st.session_state.evaluations) == 0:
        st.warning("Aucune évaluation disponible.")
        return
    
    # Calcul des moyennes par acronyme
    results = st.session_state.evaluations.groupby('acronym')['score_final'].agg(['mean', 'count']).reset_index()
    results.columns = ['Acronyme', 'Score moyen', 'Nombre d\'évaluations']
    results = results.sort_values('Score moyen', ascending=False)
    
    st.subheader("Classement général")
    st.dataframe(results)
    
    # Affichage du graphique radar pour l'acronyme sélectionné
    selected_acronym = st.selectbox("Voir le détail pour :", results['Acronyme'].tolist())
    acronym_data = st.session_state.evaluations[
        st.session_state.evaluations['acronym'] == selected_acronym
    ].iloc[0]
    
    st.plotly_chart(create_radar_chart(acronym_data))

if __name__ == '__main__':
    main()
