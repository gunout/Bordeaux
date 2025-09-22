import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class BordeauxCommuneImmobilierAnalyzer:
    def __init__(self, commune_name):
        self.commune = commune_name
        self.colors = ['#8B0000', '#FFD700', '#00008B', '#228B22', '#FF6B6B', 
                      '#4ECDC4', '#45B7D1', '#F9A602', '#6A0572', '#AB83A1']
        
        self.start_year = 2002
        self.end_year = 2025
        
        # Configuration spécifique à chaque commune bordelaise
        self.config = self._get_commune_config()
        
    def _get_commune_config(self):
        """Retourne la configuration spécifique pour chaque commune bordelaise"""
        configs = {
            "Bordeaux": {
                "population_base": 250000,
                "budget_base": 450,
                "type": "metropole",
                "specialites": ["vin", "tourisme", "administration", "commerce", "universite"],
                "prix_m2_base": 2500,
                "segment_immobilier": "haut_de_gamme"
            },
            "Mérignac": {
                "population_base": 72000,
                "budget_base": 120,
                "type": "aeroportuaire",
                "specialites": ["aeroport", "zones_activites", "commerce", "logistique"],
                "prix_m2_base": 2200,
                "segment_immobilier": "mixte"
            },
            "Pessac": {
                "population_base": 65000,
                "budget_base": 95,
                "type": "universitaire",
                "specialites": ["universite", "recherche", "vin", "residential"],
                "prix_m2_base": 2300,
                "segment_immobilier": "universitaire"
            },
            "Talence": {
                "population_base": 43000,
                "budget_base": 75,
                "type": "universitaire",
                "specialites": ["universite", "recherche", "sport", "residential"],
                "prix_m2_base": 2400,
                "segment_immobilier": "universitaire"
            },
            "Bègles": {
                "population_base": 30000,
                "budget_base": 65,
                "type": "industrielle",
                "specialites": ["industrie", "port", "commerce", "residential"],
                "prix_m2_base": 2100,
                "segment_immobilier": "mixte"
            },
            "Villenave-d'Ornon": {
                "population_base": 36000,
                "budget_base": 60,
                "type": "residentielle",
                "specialites": ["residential", "agriculture", "vin", "recherche"],
                "prix_m2_base": 2000,
                "segment_immobilier": "residentiel"
            },
            "Gradignan": {
                "population_base": 25000,
                "budget_base": 45,
                "type": "residentielle",
                "specialites": ["residential", "espaces_verts", "commerce", "education"],
                "prix_m2_base": 2600,
                "segment_immobilier": "haut_de_gamme"
            },
            "Cenon": {
                "population_base": 25000,
                "budget_base": 50,
                "type": "urbaine",
                "specialites": ["residential", "commerce", "transport", "culture"],
                "prix_m2_base": 1900,
                "segment_immobilier": "abordable"
            },
            "Floirac": {
                "population_base": 17000,
                "budget_base": 35,
                "type": "residentielle",
                "specialites": ["residential", "espaces_verts", "vin", "vue_bordeaux"],
                "prix_m2_base": 2100,
                "segment_immobilier": "mixte"
            },
            "Bouliac": {
                "population_base": 5000,
                "budget_base": 15,
                "type": "residentielle",
                "specialites": ["residential", "vignobles", "vue_bordeaux", "calme"],
                "prix_m2_base": 2800,
                "segment_immobilier": "premium"
            },
            "Parempuyre": {
                "population_base": 10000,
                "budget_base": 25,
                "type": "rurale",
                "specialites": ["agriculture", "residential", "zones_activites", "calme"],
                "prix_m2_base": 1800,
                "segment_immobilier": "abordable"
            },
            "Le Haillan": {
                "population_base": 11000,
                "budget_base": 28,
                "type": "residentielle",
                "specialites": ["residential", "commerce", "sport", "calme"],
                "prix_m2_base": 2200,
                "segment_immobilier": "mixte"
            },
            "Saint-Médard-en-Jalles": {
                "population_base": 32000,
                "budget_base": 70,
                "type": "industrielle",
                "specialites": ["industrie", "aeronautique", "defense", "residential"],
                "prix_m2_base": 1900,
                "segment_immobilier": "industriel"
            },
            "Eysines": {
                "population_base": 25000,
                "budget_base": 55,
                "type": "residentielle",
                "specialites": ["maraichage", "residential", "commerce", "proximite_bordeaux"],
                "prix_m2_base": 2300,
                "segment_immobilier": "mixte"
            },
            "Bruges": {
                "population_base": 20000,
                "budget_base": 48,
                "type": "commerciale",
                "specialites": ["commerce", "zones_activites", "residential", "proximite_aeroport"],
                "prix_m2_base": 2100,
                "segment_immobilier": "commercial"
            },
            "Blanquefort": {
                "population_base": 16000,
                "budget_base": 42,
                "type": "industrielle",
                "specialites": ["industrie", "chateau", "residential", "commerce"],
                "prix_m2_base": 2000,
                "segment_immobilier": "mixte"
            },
            "Lormont": {
                "population_base": 23000,
                "budget_base": 52,
                "type": "urbaine",
                "specialites": ["residential", "port", "transport", "culture"],
                "prix_m2_base": 1700,
                "segment_immobilier": "abordable"
            },
            "Carbon-Blanc": {
                "population_base": 8000,
                "budget_base": 22,
                "type": "residentielle",
                "specialites": ["residential", "commerce", "proximite_bordeaux", "transport"],
                "prix_m2_base": 1850,
                "segment_immobilier": "abordable"
            },
            "Ambès": {
                "population_base": 3000,
                "budget_base": 12,
                "type": "industrielle",
                "specialites": ["industrie", "port", "raffinerie", "nature"],
                "prix_m2_base": 1500,
                "segment_immobilier": "industriel"
            },
            "Bassens": {
                "population_base": 7000,
                "budget_base": 20,
                "type": "portuaire",
                "specialites": ["port", "industrie", "logistique", "residential"],
                "prix_m2_base": 1600,
                "segment_immobilier": "industriel"
            },
            # Configuration par défaut
            "default": {
                "population_base": 15000,
                "budget_base": 30,
                "type": "residentielle",
                "specialites": ["residential", "commerce_local", "services"],
                "prix_m2_base": 2000,
                "segment_immobilier": "mixte"
            }
        }
        
        return configs.get(self.commune, configs["default"])
    
    def generate_financial_data(self):
        """Génère des données financières et immobilières pour la commune bordelaise"""
        print(f"🏛️ Génération des données financières et immobilières pour {self.commune}...")
        
        # Créer une base de données annuelle
        dates = pd.date_range(start=f'{self.start_year}-01-01', 
                             end=f'{self.end_year}-12-31', freq='Y')
        
        data = {'Annee': [date.year for date in dates]}
        
        # Données démographiques
        data['Population'] = self._simulate_population(dates)
        data['Menages'] = self._simulate_households(dates)
        
        # Recettes communales
        data['Recettes_Totales'] = self._simulate_total_revenue(dates)
        data['Impots_Locaux'] = self._simulate_tax_revenue(dates)
        data['Dotations_Etat'] = self._simulate_state_grants(dates)
        data['Autres_Recettes'] = self._simulate_other_revenue(dates)
        
        # Dépenses communales
        data['Depenses_Totales'] = self._simulate_total_expenses(dates)
        data['Fonctionnement'] = self._simulate_operating_expenses(dates)
        data['Investissement'] = self._simulate_investment_expenses(dates)
        data['Charge_Dette'] = self._simulate_debt_charges(dates)
        data['Personnel'] = self._simulate_staff_costs(dates)
        
        # Indicateurs financiers
        data['Epargne_Brute'] = self._simulate_gross_savings(dates)
        data['Dette_Totale'] = self._simulate_total_debt(dates)
        data['Taux_Endettement'] = self._simulate_debt_ratio(dates)
        data['Taux_Fiscalite'] = self._simulate_tax_rate(dates)
        
        # Données immobilières (spécifiques à Bordeaux)
        data['Prix_m2_Moyen'] = self._simulate_avg_price_per_sqm(dates)
        data['Transactions_Immobilieres'] = self._simulate_real_estate_transactions(dates)
        data['Nouveaux_Logements'] = self._simulate_new_housing(dates)
        data['Taxe_Fonciere'] = self._simulate_property_tax(dates)
        data['Taxe_Habitation'] = self._simulate_residence_tax(dates)
        
        # Investissements spécifiques adaptés à Bordeaux
        data['Investissement_Immobilier'] = self._simulate_real_estate_investment(dates)
        data['Investissement_Transport'] = self._simulate_transport_investment(dates)
        data['Investissement_Viticole'] = self._simulate_wine_investment(dates)
        data['Investissement_Tourisme'] = self._simulate_tourism_investment(dates)
        data['Investissement_Culture'] = self._simulate_culture_investment(dates)
        data['Investissement_Education'] = self._simulate_education_investment(dates)
        
        df = pd.DataFrame(data)
        
        # Ajouter des tendances spécifiques au marché immobilier bordelais
        self._add_bordeaux_trends(df)
        
        return df
    
    def _simulate_population(self, dates):
        """Simule la population de la commune (croissance bordelaise forte)"""
        base_population = self.config["population_base"]
        
        population = []
        for i, date in enumerate(dates):
            # Croissance démographique bordelaise (forte attractivité)
            if self.config["type"] == "metropole":
                growth_rate = 0.012  # Croissance forte à Bordeaux
            elif self.config["type"] == "universitaire":
                growth_rate = 0.015  # Croissance très forte autour des universités
            elif self.config["type"] == "residentielle":
                growth_rate = 0.018  # Croissance explosive dans les communes résidentielles
            else:
                growth_rate = 0.010  # Croissance moyenne
                
            growth = 1 + growth_rate * i
            population.append(base_population * growth)
        
        return population
    
    def _simulate_households(self, dates):
        """Simule le nombre de ménages"""
        base_households = self.config["population_base"] / 2.2  # Taille des ménages plus petite
        
        households = []
        for i, date in enumerate(dates):
            growth = 1 + 0.014 * i  # Croissance forte
            households.append(base_households * growth)
        
        return households
    
    def _simulate_total_revenue(self, dates):
        """Simule les recettes totales de la commune"""
        base_revenue = self.config["budget_base"]
        
        revenue = []
        for i, date in enumerate(dates):
            # Croissance économique bordelaise (forte)
            if self.config["type"] == "metropole":
                growth_rate = 0.038  # Croissance très forte à Bordeaux
            elif self.config["type"] == "universitaire":
                growth_rate = 0.035  # Croissance forte dans les villes universitaires
            else:
                growth_rate = 0.032  # Croissance moyenne
                
            growth = 1 + growth_rate * i
            noise = np.random.normal(1, 0.06)
            revenue.append(base_revenue * growth * noise)
        
        return revenue
    
    def _simulate_tax_revenue(self, dates):
        """Simule les recettes fiscales"""
        base_tax = self.config["budget_base"] * 0.38
        
        tax_revenue = []
        for i, date in enumerate(dates):
            growth = 1 + 0.030 * i
            noise = np.random.normal(1, 0.07)
            tax_revenue.append(base_tax * growth * noise)
        
        return tax_revenue
    
    def _simulate_state_grants(self, dates):
        """Simule les dotations de l'État"""
        base_grants = self.config["budget_base"] * 0.35
        
        grants = []
        for i, date in enumerate(dates):
            year = date.year
            if year >= 2010:
                increase = 1 + 0.008 * (year - 2010)
            else:
                increase = 1
            
            noise = np.random.normal(1, 0.05)
            grants.append(base_grants * increase * noise)
        
        return grants
    
    def _simulate_other_revenue(self, dates):
        """Simule les autres recettes"""
        base_other = self.config["budget_base"] * 0.27
        
        other_revenue = []
        for i, date in enumerate(dates):
            growth = 1 + 0.028 * i
            noise = np.random.normal(1, 0.08)
            other_revenue.append(base_other * growth * noise)
        
        return other_revenue
    
    def _simulate_total_expenses(self, dates):
        """Simule les dépenses totales"""
        base_expenses = self.config["budget_base"] * 0.97
        
        expenses = []
        for i, date in enumerate(dates):
            growth = 1 + 0.034 * i
            noise = np.random.normal(1, 0.05)
            expenses.append(base_expenses * growth * noise)
        
        return expenses
    
    def _simulate_operating_expenses(self, dates):
        """Simule les dépenses de fonctionnement"""
        base_operating = self.config["budget_base"] * 0.62
        
        operating = []
        for i, date in enumerate(dates):
            growth = 1 + 0.030 * i
            noise = np.random.normal(1, 0.04)
            operating.append(base_operating * growth * noise)
        
        return operating
    
    def _simulate_investment_expenses(self, dates):
        """Simule les dépenses d'investissement"""
        base_investment = self.config["budget_base"] * 0.35
        
        investment = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2007, 2013, 2019, 2024]:
                multiplier = 1.6
            elif year in [2009, 2015, 2021]:
                multiplier = 0.8
            else:
                multiplier = 1.0
            
            growth = 1 + 0.028 * i
            noise = np.random.normal(1, 0.15)
            investment.append(base_investment * growth * multiplier * noise)
        
        return investment
    
    def _simulate_debt_charges(self, dates):
        """Simule les charges de la dette"""
        base_debt_charge = self.config["budget_base"] * 0.06
        
        debt_charges = []
        for i, date in enumerate(dates):
            year = date.year
            if year >= 2005:
                increase = 1 + 0.007 * (year - 2005)
            else:
                increase = 1
            
            noise = np.random.normal(1, 0.08)
            debt_charges.append(base_debt_charge * increase * noise)
        
        return debt_charges
    
    def _simulate_staff_costs(self, dates):
        """Simule les dépenses de personnel"""
        base_staff = self.config["budget_base"] * 0.42
        
        staff_costs = []
        for i, date in enumerate(dates):
            growth = 1 + 0.029 * i
            noise = np.random.normal(1, 0.03)
            staff_costs.append(base_staff * growth * noise)
        
        return staff_costs
    
    def _simulate_gross_savings(self, dates):
        """Simule l'épargne brute"""
        savings = []
        for i, date in enumerate(dates):
            base_saving = self.config["budget_base"] * 0.03
            
            year = date.year
            if year >= 2010:
                improvement = 1 + 0.009 * (year - 2010)
            else:
                improvement = 1
            
            noise = np.random.normal(1, 0.12)
            savings.append(base_saving * improvement * noise)
        
        return savings
    
    def _simulate_total_debt(self, dates):
        """Simule la dette totale"""
        base_debt = self.config["budget_base"] * 0.80
        
        debt = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2007, 2013, 2019, 2024]:
                change = 1.22
            elif year in [2009, 2015, 2021]:
                change = 0.90
            else:
                change = 1.0
            
            noise = np.random.normal(1, 0.07)
            debt.append(base_debt * change * noise)
        
        return debt
    
    def _simulate_debt_ratio(self, dates):
        """Simule le taux d'endettement"""
        ratios = []
        for i, date in enumerate(dates):
            base_ratio = 0.72
            
            year = date.year
            if year >= 2010:
                improvement = 1 - 0.011 * (year - 2010)
            else:
                improvement = 1
            
            noise = np.random.normal(1, 0.05)
            ratios.append(base_ratio * improvement * noise)
        
        return ratios
    
    def _simulate_tax_rate(self, dates):
        """Simule le taux de fiscalité (moyen)"""
        rates = []
        for i, date in enumerate(dates):
            base_rate = 0.88
            
            year = date.year
            if year >= 2010:
                increase = 1 + 0.004 * (year - 2010)
            else:
                increase = 1
            
            noise = np.random.normal(1, 0.03)
            rates.append(base_rate * increase * noise)
        
        return rates
    
    def _simulate_avg_price_per_sqm(self, dates):
        """Simule le prix moyen au m² (spécifique à Bordeaux)"""
        base_price = self.config["prix_m2_base"]
        
        prices = []
        for i, date in enumerate(dates):
            year = date.year
            
            # Croissance forte du marché immobilier bordelais
            if self.config["segment_immobilier"] == "premium":
                growth_rate = 0.045  # Croissance très forte pour le premium
            elif self.config["segment_immobilier"] == "haut_de_gamme":
                growth_rate = 0.042  # Croissance forte pour le haut de gamme
            elif self.config["segment_immobilier"] == "universitaire":
                growth_rate = 0.038  # Croissance forte autour des universités
            else:
                growth_rate = 0.035  # Croissance moyenne
            
            # Ajustements annuels basés sur des événements réels
            if 2002 <= year <= 2007:
                # Période de forte croissance pré-crise
                multiplier = 1 + 0.06 * (year - 2002)
            elif 2008 <= year <= 2009:
                # Impact modéré de la crise financière à Bordeaux
                multiplier = 0.96
            elif 2010 <= year <= 2019:
                # Forte reprise et boom immobilier bordelais
                multiplier = 1 + 0.05 * (year - 2010)
            elif 2020 <= year <= 2021:
                # Résilience pendant le COVID
                multiplier = 1.02
            else:
                # Croissance soutenue post-COVID
                multiplier = 1 + 0.04 * (year - 2022)
            
            growth = 1 + growth_rate * i
            noise = np.random.normal(1, 0.08)
            prices.append(base_price * growth * multiplier * noise)
        
        return prices
    
    def _simulate_real_estate_transactions(self, dates):
        """Simule le nombre de transactions immobilières"""
        base_transactions = self.config["population_base"] / 100  # Base proportionnelle à la population
        
        transactions = []
        for i, date in enumerate(dates):
            year = date.year
            
            # Variations selon la conjoncture
            if 2002 <= year <= 2007:
                multiplier = 1 + 0.08 * (year - 2002)  # Forte activité
            elif 2008 <= year <= 2009:
                multiplier = 0.75  # Baisse pendant la crise
            elif 2010 <= year <= 2019:
                multiplier = 1 + 0.06 * (year - 2010)  # Reprise progressive
            elif 2020 <= year <= 2021:
                multiplier = 0.85  # Ralentissement COVID
            else:
                multiplier = 1 + 0.05 * (year - 2022)  # Reprise post-COVID
            
            growth = 1 + 0.015 * i
            noise = np.random.normal(1, 0.12)
            transactions.append(base_transactions * growth * multiplier * noise)
        
        return transactions
    
    def _simulate_new_housing(self, dates):
        """Simule le nombre de nouveaux logements construits"""
        base_housing = self.config["population_base"] / 500  # Base proportionnelle
        
        housing = []
        for i, date in enumerate(dates):
            year = date.year
            
            # Pics de construction selon les programmes
            if year in [2005, 2010, 2015, 2020]:
                multiplier = 2.0  # Années de grands programmes
            elif year in [2008, 2014, 2021]:
                multiplier = 0.7  # Ralentissements
            else:
                multiplier = 1.0
            
            growth = 1 + 0.018 * i
            noise = np.random.normal(1, 0.20)
            housing.append(base_housing * growth * multiplier * noise)
        
        return housing
    
    def _simulate_property_tax(self, dates):
        """Simule la taxe foncière"""
        base_tax = self.config["budget_base"] * 0.15
        
        tax = []
        for i, date in enumerate(dates):
            year = date.year
            if year >= 2010:
                increase = 1 + 0.012 * (year - 2010)
            else:
                increase = 1
            
            noise = np.random.normal(1, 0.06)
            tax.append(base_tax * increase * noise)
        
        return tax
    
    def _simulate_residence_tax(self, dates):
        """Simule la taxe d'habitation (en diminution)"""
        base_tax = self.config["budget_base"] * 0.12
        
        tax = []
        for i, date in enumerate(dates):
            year = date.year
            if year >= 2018:
                # Réduction progressive de la taxe d'habitation
                reduction = 1 - 0.15 * min(4, year - 2018)  # Suppression progressive
            else:
                reduction = 1
            
            noise = np.random.normal(1, 0.05)
            tax.append(base_tax * reduction * noise)
        
        return tax
    
    def _simulate_real_estate_investment(self, dates):
        """Simule l'investissement immobilier"""
        base_investment = self.config["budget_base"] * 0.08
        
        # Ajustement selon les spécialités
        multiplier = 1.5 if "residential" in self.config["specialites"] else 0.9
        
        investment = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2006, 2012, 2018, 2023]:
                year_multiplier = 1.8
            else:
                year_multiplier = 1.0
            
            growth = 1 + 0.035 * i
            noise = np.random.normal(1, 0.16)
            investment.append(base_investment * growth * year_multiplier * multiplier * noise)
        
        return investment
    
    def _simulate_transport_investment(self, dates):
        """Simule l'investissement en transport (tramway, etc.)"""
        base_investment = self.config["budget_base"] * 0.06
        
        # Ajustement selon les spécialités
        multiplier = 1.6 if "transport" in self.config["specialites"] else 1.0
        
        investment = []
        for i, date in enumerate(dates):
            year = date.year
            # Pics d'investissement liés au tramway
            if year in [2003, 2007, 2014, 2020]:
                year_multiplier = 2.2
            else:
                year_multiplier = 1.0
            
            growth = 1 + 0.030 * i
            noise = np.random.normal(1, 0.18)
            investment.append(base_investment * growth * year_multiplier * multiplier * noise)
        
        return investment
    
    def _simulate_wine_investment(self, dates):
        """Simule l'investissement viticole (spécifique à Bordeaux)"""
        base_investment = self.config["budget_base"] * 0.04
        
        # Ajustement selon les spécialités
        multiplier = 2.0 if "vin" in self.config["specialites"] else 0.5
        
        investment = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2005, 2010, 2015, 2020]:
                year_multiplier = 1.9
            else:
                year_multiplier = 1.0
            
            growth = 1 + 0.032 * i
            noise = np.random.normal(1, 0.22)
            investment.append(base_investment * growth * year_multiplier * multiplier * noise)
        
        return investment
    
    def _simulate_tourism_investment(self, dates):
        """Simule l'investissement touristique"""
        base_investment = self.config["budget_base"] * 0.05
        
        # Ajustement selon les spécialités
        multiplier = 1.7 if "tourisme" in self.config["specialites"] else 0.8
        
        investment = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2007, 2013, 2019, 2024]:
                year_multiplier = 1.8
            else:
                year_multiplier = 1.0
            
            growth = 1 + 0.028 * i
            noise = np.random.normal(1, 0.17)
            investment.append(base_investment * growth * year_multiplier * multiplier * noise)
        
        return investment
    
    def _simulate_culture_investment(self, dates):
        """Simule l'investissement culturel"""
        base_investment = self.config["budget_base"] * 0.03
        
        # Ajustement selon les spécialités
        multiplier = 1.6 if "culture" in self.config["specialites"] else 0.8
        
        investment = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2010, 2016, 2022]:
                year_multiplier = 1.9
            else:
                year_multiplier = 1.0
            
            growth = 1 + 0.025 * i
            noise = np.random.normal(1, 0.15)
            investment.append(base_investment * growth * year_multiplier * multiplier * noise)
        
        return investment
    
    def _simulate_education_investment(self, dates):
        """Simule l'investissement éducatif"""
        base_investment = self.config["budget_base"] * 0.07
        
        # Ajustement selon les spécialités
        multiplier = 1.8 if "universite" in self.config["specialites"] else 1.0
        
        investment = []
        for i, date in enumerate(dates):
            year = date.year
            if year in [2008, 2014, 2020]:
                year_multiplier = 1.7
            else:
                year_multiplier = 1.0
            
            growth = 1 + 0.030 * i
            noise = np.random.normal(1, 0.14)
            investment.append(base_investment * growth * year_multiplier * multiplier * noise)
        
        return investment
    
    def _add_bordeaux_trends(self, df):
        """Ajoute des tendances réalistes adaptées au marché bordelais"""
        for i, row in df.iterrows():
            year = row['Annee']
            
            # Développement du tramway (phases successives)
            if year in [2003, 2004]:
                df.loc[i, 'Investissement_Transport'] *= 2.5  # Lancement tramway
            if year in [2007, 2008]:
                df.loc[i, 'Investissement_Transport'] *= 2.0  # Extensions
            if year in [2014, 2015]:
                df.loc[i, 'Investissement_Transport'] *= 1.8  # Nouvelles lignes
            
            # Boom immobilier bordelais (2010-2019)
            if 2010 <= year <= 2019:
                df.loc[i, 'Prix_m2_Moyen'] *= 1.05
                df.loc[i, 'Transactions_Immobilieres'] *= 1.08
                df.loc[i, 'Investissement_Immobilier'] *= 1.3
            
            # Effet Cité du Vin (2016)
            if year == 2016:
                df.loc[i, 'Investissement_Tourisme'] *= 2.0
                df.loc[i, 'Investissement_Culture'] *= 1.8
            
            # Impact COVID-19 (2020-2021) - marché résilient à Bordeaux
            if 2020 <= year <= 2021:
                if year == 2020:
                    df.loc[i, 'Transactions_Immobilieres'] *= 0.80
                else:
                    df.loc[i, 'Prix_m2_Moyen'] *= 1.03  # Reprise rapide
                    df.loc[i, 'Transactions_Immobilieres'] *= 1.10
            
            # Plan de relance métropolitain (2022-2025)
            if year >= 2022:
                df.loc[i, 'Investissement_Transport'] *= 1.15
                df.loc[i, 'Investissement_Immobilier'] *= 1.20
                df.loc[i, 'Nouveaux_Logements'] *= 1.25
    
    def create_financial_analysis(self, df):
        """Crée une analyse complète des finances et de l'immobilier"""
        plt.style.use('seaborn-v0_8')
        fig = plt.figure(figsize=(20, 28))
        
        # 1. Évolution des recettes et dépenses
        ax1 = plt.subplot(5, 2, 1)
        self._plot_revenue_expenses(df, ax1)
        
        # 2. Structure des recettes
        ax2 = plt.subplot(5, 2, 2)
        self._plot_revenue_structure(df, ax2)
        
        # 3. Évolution des prix immobiliers
        ax3 = plt.subplot(5, 2, 3)
        self._plot_real_estate_prices(df, ax3)
        
        # 4. Activité immobilière
        ax4 = plt.subplot(5, 2, 4)
        self._plot_real_estate_activity(df, ax4)
        
        # 5. Structure des dépenses
        ax5 = plt.subplot(5, 2, 5)
        self._plot_expenses_structure(df, ax5)
        
        # 6. Investissements communaux
        ax6 = plt.subplot(5, 2, 6)
        self._plot_investments(df, ax6)
        
        # 7. Dette et endettement
        ax7 = plt.subplot(5, 2, 7)
        self._plot_debt(df, ax7)
        
        # 8. Indicateurs de performance
        ax8 = plt.subplot(5, 2, 8)
        self._plot_performance_indicators(df, ax8)
        
        # 9. Démographie
        ax9 = plt.subplot(5, 2, 9)
        self._plot_demography(df, ax9)
        
        # 10. Investissements sectoriels
        ax10 = plt.subplot(5, 2, 10)
        self._plot_sectorial_investments(df, ax10)
        
        plt.suptitle(f'Analyse des Comptes Communaux et Immobiliers de {self.commune} - Bordeaux Métropole ({self.start_year}-{self.end_year})', 
                    fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{self.commune}_bordeaux_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Générer les insights
        self._generate_financial_insights(df)
    
    def _plot_revenue_expenses(self, df, ax):
        """Plot de l'évolution des recettes et dépenses"""
        ax.plot(df['Annee'], df['Recettes_Totales'], label='Recettes Totales', 
               linewidth=2, color='#8B0000', alpha=0.8)
        ax.plot(df['Annee'], df['Depenses_Totales'], label='Dépenses Totales', 
               linewidth=2, color='#00008B', alpha=0.8)
        
        ax.set_title('Évolution des Recettes et Dépenses (M€)', 
                    fontsize=12, fontweight='bold')
        ax.set_ylabel('Montants (M€)')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_revenue_structure(self, df, ax):
        """Plot de la structure des recettes"""
        years = df['Annee']
        width = 0.8
        
        bottom = np.zeros(len(years))
        categories = ['Impots_Locaux', 'Dotations_Etat', 'Autres_Recettes']
        colors = ['#8B0000', '#FFD700', '#00008B']
        labels = ['Impôts Locaux', 'Dotations État', 'Autres Recettes']
        
        for i, category in enumerate(categories):
            ax.bar(years, df[category], width, label=labels[i], bottom=bottom, color=colors[i])
            bottom += df[category]
        
        ax.set_title('Structure des Recettes (M€)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Montants (M€)')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
    
    def _plot_real_estate_prices(self, df, ax):
        """Plot de l'évolution des prix immobiliers"""
        ax.plot(df['Annee'], df['Prix_m2_Moyen'], label='Prix moyen au m²', 
               linewidth=3, color='#8B0000', alpha=0.8)
        
        ax.set_title('Évolution des Prix Immobiliers (€/m²)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Prix (€/m²)')
        ax.grid(True, alpha=0.3)
        
        # Ajouter des annotations pour les événements marquants
        ax.annotate('Lancement Tramway', xy=(2003, df.loc[df['Annee'] == 2003, 'Prix_m2_Moyen'].values[0]), 
                   xytext=(2003, df.loc[df['Annee'] == 2003, 'Prix_m2_Moyen'].values[0] * 0.9),
                   arrowprops=dict(arrowstyle='->', color='red'))
        
        ax.annotate('Boom immobilier', xy=(2015, df.loc[df['Annee'] == 2015, 'Prix_m2_Moyen'].values[0]), 
                   xytext=(2015, df.loc[df['Annee'] == 2015, 'Prix_m2_Moyen'].values[0] * 1.1),
                   arrowprops=dict(arrowstyle='->', color='green'))
    
    def _plot_real_estate_activity(self, df, ax):
        """Plot de l'activité immobilière"""
        # Transactions immobilières
        ax.bar(df['Annee'], df['Transactions_Immobilieres'], label='Transactions', 
              color='#8B0000', alpha=0.7)
        
        ax.set_title('Activité Immobilière', fontsize=12, fontweight='bold')
        ax.set_ylabel('Transactions immobilières', color='#8B0000')
        ax.tick_params(axis='y', labelcolor='#8B0000')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Nouveaux logements en second axe
        ax2 = ax.twinx()
        ax2.plot(df['Annee'], df['Nouveaux_Logements'], label='Nouveaux logements', 
                linewidth=2, color='#00008B')
        ax2.set_ylabel('Nouveaux logements', color='#00008B')
        ax2.tick_params(axis='y', labelcolor='#00008B')
        
        # Combiner les légendes
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    def _plot_expenses_structure(self, df, ax):
        """Plot de la structure des dépenses"""
        years = df['Annee']
        width = 0.8
        
        bottom = np.zeros(len(years))
        categories = ['Fonctionnement', 'Investissement', 'Charge_Dette', 'Personnel']
        colors = ['#8B0000', '#FFD700', '#00008B', '#228B22']
        labels = ['Fonctionnement', 'Investissement', 'Charge Dette', 'Personnel']
        
        for i, category in enumerate(categories):
            ax.bar(years, df[category], width, label=labels[i], bottom=bottom, color=colors[i])
            bottom += df[category]
        
        ax.set_title('Structure des Dépenses (M€)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Montants (M€)')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
    
    def _plot_investments(self, df, ax):
        """Plot des investissements communaux"""
        ax.plot(df['Annee'], df['Investissement_Immobilier'], label='Immobilier', 
               linewidth=2, color='#8B0000', alpha=0.8)
        ax.plot(df['Annee'], df['Investissement_Transport'], label='Transport', 
               linewidth=2, color='#FFD700', alpha=0.8)
        ax.plot(df['Annee'], df['Investissement_Viticole'], label='Viticole', 
               linewidth=2, color='#00008B', alpha=0.8)
        ax.plot(df['Annee'], df['Investissement_Tourisme'], label='Tourisme', 
               linewidth=2, color='#228B22', alpha=0.8)
        ax.plot(df['Annee'], df['Investissement_Education'], label='Éducation', 
               linewidth=2, color='#FF6B6B', alpha=0.8)
        
        ax.set_title('Répartition des Investissements (M€)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Montants (M€)')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_debt(self, df, ax):
        """Plot de la dette et du taux d'endettement"""
        # Dette totale
        ax.bar(df['Annee'], df['Dette_Totale'], label='Dette Totale (M€)', 
              color='#8B0000', alpha=0.7)
        
        ax.set_title('Dette Communale et Taux d\'Endettement', fontsize=12, fontweight='bold')
        ax.set_ylabel('Dette (M€)', color='#8B0000')
        ax.tick_params(axis='y', labelcolor='#8B0000')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Taux d'endettement en second axe
        ax2 = ax.twinx()
        ax2.plot(df['Annee'], df['Taux_Endettement'], label='Taux d\'Endettement', 
                linewidth=3, color='#00008B')
        ax2.set_ylabel('Taux d\'Endettement', color='#00008B')
        ax2.tick_params(axis='y', labelcolor='#00008B')
        
        # Combiner les légendes
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    def _plot_performance_indicators(self, df, ax):
        """Plot des indicateurs de performance"""
        # Épargne brute
        ax.bar(df['Annee'], df['Epargne_Brute'], label='Épargne Brute (M€)', 
              color='#228B22', alpha=0.7)
        
        ax.set_title('Indicateurs de Performance', fontsize=12, fontweight='bold')
        ax.set_ylabel('Épargne Brute (M€)', color='#228B22')
        ax.tick_params(axis='y', labelcolor='#228B22')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Taux de fiscalité en second axe
        ax2 = ax.twinx()
        ax2.plot(df['Annee'], df['Taux_Fiscalite'], label='Taux de Fiscalité', 
                linewidth=3, color='#FF6B6B')
        ax2.set_ylabel('Taux de Fiscalité', color='#FF6B6B')
        ax2.tick_params(axis='y', labelcolor='#FF6B6B')
        
        # Combiner les légendes
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    def _plot_demography(self, df, ax):
        """Plot de l'évolution démographique"""
        ax.plot(df['Annee'], df['Population'], label='Population', 
               linewidth=2, color='#8B0000', alpha=0.8)
        
        ax.set_title('Évolution Démographique', fontsize=12, fontweight='bold')
        ax.set_ylabel('Population', color='#8B0000')
        ax.tick_params(axis='y', labelcolor='#8B0000')
        ax.grid(True, alpha=0.3)
        
        # Nombre de ménages en second axe
        ax2 = ax.twinx()
        ax2.plot(df['Annee'], df['Menages'], label='Ménages', 
                linewidth=2, color='#00008B', alpha=0.8)
        ax2.set_ylabel('Ménages', color='#00008B')
        ax2.tick_params(axis='y', labelcolor='#00008B')
        
        # Combiner les légendes
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    def _plot_sectorial_investments(self, df, ax):
        """Plot des investissements sectoriels"""
        years = df['Annee']
        width = 0.8
        
        bottom = np.zeros(len(years))
        categories = ['Investissement_Immobilier', 'Investissement_Transport', 
                     'Investissement_Viticole', 'Investissement_Tourisme', 
                     'Investissement_Education']
        
        colors = ['#8B0000', '#FFD700', '#00008B', '#228B22', '#FF6B6B']
        labels = ['Immobilier', 'Transport', 'Viticole', 'Tourisme', 'Éducation']
        
        for i, category in enumerate(categories):
            ax.bar(years, df[category], width, label=labels[i], bottom=bottom, color=colors[i])
            bottom += df[category]
        
        ax.set_title('Répartition Sectorielle des Investissements (M€)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Montants (M€)')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
    
    def _generate_financial_insights(self, df):
        """Génère des insights analytiques adaptés au marché bordelais"""
        print(f"🏛️ INSIGHTS ANALYTIQUES - Commune de {self.commune} (Bordeaux Métropole)")
        print("=" * 60)
        
        # 1. Statistiques de base
        print("\n1. 📈 STATISTIQUES GÉNÉRALES:")
        avg_revenue = df['Recettes_Totales'].mean()
        avg_expenses = df['Depenses_Totales'].mean()
        avg_price = df['Prix_m2_Moyen'].mean()
        avg_transactions = df['Transactions_Immobilieres'].mean()
        
        print(f"Recettes moyennes annuelles: {avg_revenue:.2f} M€")
        print(f"Dépenses moyennes annuelles: {avg_expenses:.2f} M€")
        print(f"Prix moyen au m²: {avg_price:.0f} €")
        print(f"Transactions immobilières moyennes: {avg_transactions:.0f}")
        
        # 2. Croissance immobilière
        print("\n2. 📊 CROISSANCE IMMOBILIÈRE:")
        price_growth = ((df['Prix_m2_Moyen'].iloc[-1] / 
                        df['Prix_m2_Moyen'].iloc[0]) - 1) * 100
        population_growth = ((df['Population'].iloc[-1] / 
                             df['Population'].iloc[0]) - 1) * 100
        
        print(f"Croissance des prix au m² ({self.start_year}-{self.end_year}): {price_growth:.1f}%")
        print(f"Croissance de la population ({self.start_year}-{self.end_year}): {population_growth:.1f}%")
        
        # 3. Structure financière
        print("\n3. 📋 STRUCTURE FINANCIÈRE:")
        tax_share = (df['Impots_Locaux'].mean() / df['Recettes_Totales'].mean()) * 100
        state_share = (df['Dotations_Etat'].mean() / df['Recettes_Totales'].mean()) * 100
        property_tax_share = (df['Taxe_Fonciere'].mean() / df['Recettes_Totales'].mean()) * 100
        
        print(f"Part des impôts locaux dans les recettes: {tax_share:.1f}%")
        print(f"Part des dotations de l'État dans les recettes: {state_share:.1f}%")
        print(f"Part de la taxe foncière dans les recettes: {property_tax_share:.1f}%")
        
        # 4. Marché immobilier
        print("\n4. 🏠 MARCHÉ IMMOBILIER:")
        last_price = df['Prix_m2_Moyen'].iloc[-1]
        price_2020 = df.loc[df['Annee'] == 2020, 'Prix_m2_Moyen'].values[0]
        covid_impact = ((last_price / price_2020) - 1) * 100
        
        print(f"Prix actuel au m²: {last_price:.0f} €")
        print(f"Impact COVID-19 sur les prix (2020-{self.end_year}): +{covid_impact:.1f}%")
        print(f"Segment immobilier: {self.config['segment_immobilier']}")
        
        # 5. Spécificités de la commune bordelaise
        print(f"\n5. 🌟 SPÉCIFICITÉS DE {self.commune.upper()}:")
        print(f"Type de commune: {self.config['type']}")
        print(f"Spécialités: {', '.join(self.config['specialites'])}")
        print(f"Prix de référence au m²: {self.config['prix_m2_base']} €")
        
        # 6. Événements marquants du marché bordelais
        print("\n6. 📅 ÉVÉNEMENTS MARQUANTS BORDEAUX:")
        print("• 2003-2007: Développement du tramway et attractivité croissante")
        print("• 2008-2009: Impact modéré de la crise financière")
        print("• 2010-2019: Boom immobilier et forte attractivité")
        print("• 2016: Ouverture de la Cité du Vin")
        print("• 2020-2021: Résilience pendant la crise COVID-19")
        print("• 2022-2025: Plan de relance métropolitain")
        
        # 7. Recommandations stratégiques
        print("\n7. 💡 RECOMMANDATIONS STRATÉGIQUES:")
        if "vin" in self.config["specialites"]:
            print("• Développer l'œnotourisme et les circuits viticoles")
            print("• Valoriser le patrimoine viticole")
        if "universite" in self.config["specialites"]:
            print("• Renforcer les liens université-entreprises")
            print("• Développer l'immobilier étudiant et chercheurs")
        if "residential" in self.config["specialites"]:
            print("• Maîtriser la pression foncière")
            print("• Développer l'offre de logements accessibles")
        print("• Poursuivre les investissements en transports durables")
        print("• Préserver les espaces verts et la qualité de vie")
        print("• Développer l'économie numérique et créative")
        print("• Renforcer l'attractivité commerciale et touristique")

def main():
    """Fonction principale pour Bordeaux Métropole"""
    # Liste des communes de Bordeaux Métropole
    communes = [
        "Bordeaux", "Mérignac", "Pessac", "Talence", "Bègles", 
        "Villenave-d'Ornon", "Gradignan", "Cenon", "Floirac", "Bouliac",
        "Parempuyre", "Le Haillan", "Saint-Médard-en-Jalles", "Eysines", 
        "Bruges", "Blanquefort", "Lormont", "Carbon-Blanc", "Ambès", "Bassens"
    ]
    
    print("🏛️ ANALYSE DES COMPTES COMMUNAUX ET IMMOBILIERS - BORDEAUX MÉTROPOLE (2002-2025)")
    print("=" * 70)
    
    # Demander à l'utilisateur de choisir une commune
    print("Liste des communes disponibles:")
    for i, commune in enumerate(communes, 1):
        print(f"{i}. {commune}")
    
    try:
        choix = int(input("\nChoisissez le numéro de la commune à analyser: "))
        if choix < 1 or choix > len(communes):
            raise ValueError
        commune_selectionnee = communes[choix-1]
    except (ValueError, IndexError):
        print("Choix invalide. Sélection de Bordeaux par défaut.")
        commune_selectionnee = "Bordeaux"
    
    # Initialiser l'analyseur
    analyzer = BordeauxCommuneImmobilierAnalyzer(commune_selectionnee)
    
    # Générer les données
    financial_data = analyzer.generate_financial_data()
    
    # Sauvegarder les données
    output_file = f'{commune_selectionnee}_bordeaux_data_2002_2025.csv'
    financial_data.to_csv(output_file, index=False)
    print(f"💾 Données sauvegardées: {output_file}")
    
    # Aperçu des données
    print("\n👀 Aperçu des données:")
    print(financial_data[['Annee', 'Population', 'Prix_m2_Moyen', 'Transactions_Immobilieres', 'Recettes_Totales']].head())
    
    # Créer l'analyse
    print("\n📈 Création de l'analyse financière et immobilière...")
    analyzer.create_financial_analysis(financial_data)
    
    print(f"\n✅ Analyse de {commune_selectionnee} terminée!")
    print(f"📊 Période: {analyzer.start_year}-{analyzer.end_year}")
    print("🏠 Données: Démographie, finances, marché immobilier, investissements")

if __name__ == "__main__":
    main()