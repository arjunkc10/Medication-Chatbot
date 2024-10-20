import requests
from bs4 import BeautifulSoup

# Function to scrape data from NHS website
def scrape_nhs_data():
    base_url = "https://www.nhsinform.scot/illnesses-and-conditions/a-to-z/"
    symptoms_medications = {}

    # Fetch the list of conditions from A to Z
    for letter in "abcdefghijklmnopqrstuvwxyz":
        url = f"{base_url}{letter}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all condition links
        conditions = soup.find_all('a', class_='nhsuk-list-panel__link')
        
        for condition in conditions:
            condition_url = "https://www.nhsinform.scot" + condition['href']
            condition_response = requests.get(condition_url)
            condition_soup = BeautifulSoup(condition_response.content, 'html.parser')
            
            # Extract illness name and symptoms
            illness_name = condition.text.strip()
            symptom_section = condition_soup.find('h2', text='Symptoms')
            
            if symptom_section:
                symptoms_list = symptom_section.find_next('ul').find_all('li')
                symptoms = [symptom.text.strip() for symptom in symptoms_list]
                
                # Extract medications from the treatment section
                treatment_section = condition_soup.find('h2', text='Treatment')
                if treatment_section:
                    medications_list = treatment_section.find_next('ul').find_all('li')
                    medications = [med.text.strip() for med in medications_list]

                    # Map symptoms to medications
                    for symptom in symptoms:
                        if symptom in symptoms_medications:
                            symptoms_medications[symptom].extend(medications)
                        else:
                            symptoms_medications[symptom] = medications

    return symptoms_medications

# Run the scraper and print the results
data = scrape_nhs_data()
for symptom, meds in data.items():
    print(f"Symptom: {symptom}, Medications: {', '.join(set(meds))}")
