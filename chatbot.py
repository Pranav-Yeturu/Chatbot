import os
import requests

class LoanChatBot:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API Key is not set. Please set the GEMINI_API_KEY environment variable.")
        self.loan_type = None
        self.employment_status = None
        self.cibil_score = None
        self.user_details = {}

    def start(self):
        print("Hi, I am the LendBot and will help you with your loan concerns. How may I help you today?")
        self.inquire_loan_type()

    def inquire_loan_type(self):
        user_input = input("Please describe the type of loan you need or its purpose: ")
        self.loan_type = self.classify_loan_type(user_input)
        if self.loan_type:
            print(f"You are interested in a {self.loan_type}.")
            self.inquire_employment_status()
        else:
            self.loan_type = input("Could you be more specific about the loan's purpose? ")
            self.inquire_employment_status()

    def inquire_employment_status(self):
        self.employment_status = input("What is your employment status? Salaried/Self Employed/Unemployed/Student: ").strip().lower()

        if self.employment_status == "salaried":
            self.user_details['net_income'] = input("Please enter your net monthly income: ")
            self.user_details['current_obligations'] = input("Do you have any current financial obligations (e.g., EMIs)? ")

        elif self.employment_status == "self employed":
            self.user_details['monthly_gross_income'] = input("Please enter your monthly gross income: ")
            self.user_details['type_of_business'] = input("What type of business do you run? ")
            self.user_details['location'] = input("Where are you located? ")
            self.user_details['business_proof_doc'] = input("Do you have a valid business proof document? (Yes/No): ")
            self.user_details['bank_statement'] = input("Can you provide your banking statement for the last 1 year? (Yes/No): ")
            self.user_details['itrs'] = input("Do you have ITRs for the past 2 years? (yes/no): ")
            self.user_details['current_obligations'] = input("Do you have any current financial obligations (e.g., EMIs)? ")

        elif self.employment_status == "unemployed":
            self.user_details['unemployment_reason'] = input("Please specify the reason for unemployment (e.g., recent layoff, health issues, etc.): ")
            self.user_details['savings'] = input("Do you have any savings or investments? (Yes/No): ")

        elif self.employment_status == "student":
            self.user_details['institution'] = input("Please enter the name of your educational institution: ")
            self.user_details['course'] = input("What course are you pursuing? ")
            self.user_details['current_funding'] = input("How are you funding your studies currently? (e.g., Family support, Scholarships, Part-time job): ")

        self.cibil_score = int(input("Please enter your CIBIL score: "))
        self.evaluate_eligibility()

    def evaluate_eligibility(self):
        if self.cibil_score >= 650:
            print("You are eligible for the loan. Proceeding to search for banks...")
            self.search_banks(self.loan_type)
        else:
            print("Your CIBIL score is less than 650. Let's explore alternative loan solutions.")
            self.inquire_additional_loan_options()

    def inquire_additional_loan_options(self):
        add_family_member = input("Do you have any additional earning family members who can be added as co-applicants? (yes/no): ").strip().lower()

        if add_family_member == "yes":
            family_member_details = {}
            family_member_details['relation'] = input("What is your relation with the family member? ")
            family_member_details['employment_status'] = input("What is their employment status? (Salaried/Self Employed): ").strip().lower()

            if family_member_details['employment_status'] == "salaried":
                family_member_details['net_income'] = input("Please enter their net monthly income: ")
                

            elif family_member_details['employment_status'] == "self employed":
                family_member_details['monthly_gross_income'] = input("Please enter their monthly gross income: ")
                family_member_details['type_of_business'] = input("What type of business do they run? ")
                family_member_details['location'] = input("Where are they located? ")
                family_member_details['business_proof_doc'] = input("Do they have a valid business proof document? (yes/no): ")
                family_member_details['bank_statement'] = input("Can they provide their banking statement for the last 1 year? (yes/no): ")
                family_member_details['itrs'] = input("Do they have ITRs for the past 2 years? (yes/no): ")

            print(f"Collected co-applicant details: {family_member_details}")

        add_collateral = input("Do you have any collateral (e.g., property, gold)? (Yes/No): ").strip().lower()

        if add_collateral == "yes":
            collateral_value = int(input("Please enter the estimated market value of the collateral: "))
            loan_amount = collateral_value * 0.65
            print(f"You can get a loan amount of up to 65% of the collateral value, which is approximately {loan_amount}.")
        else:
            print("No collateral details provided.")

        print("Now, let's search for banks that offer alternative loan solutions.")
        self.search_banks(self.loan_type)

    def classify_loan_type(self, user_input):
        keywords_to_loan_type = {
            "home": "Home Loan",
            "property": "Loan Against Property (LAP)",
            "insurance": "Loan Against Insurance Policies",
            "gold": "Gold Loan",
            "mutual funds": "Loan Against Mutual Funds and Shares",
            "fixed deposit": "Loan Against Fixed Deposit",
            "personal": "Personal Loan",
            "business": "Business Loan",
            "education" : "Education Loan"
        }
        for keyword, loan_type in keywords_to_loan_type.items():
            if keyword in user_input.lower():
                return loan_type
        return None

    def search_banks(self, category):
        print(f"Searching for banks that offer {category}...")
        results = self.llm_search(category)
        if results:
            print("Here are some banks that might match your criteria:")
            for result in results:
                print(f"- {result}")
        else:
            print("No relevant results found. Please try again or refine your search.")

    def llm_search(self, category):
        prompt = f"A user is looking for a {category}. What are some banks or financial institutions that typically offer {category}s?"

        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "prompt": prompt,
        }

        try:
            response = requests.post(self.gemini_api_endpoint, headers=headers, json=data)
            response.raise_for_status()
            response_data = response.json()

            generated_text = response_data.get('choices', [{}])[0].get('text', '')
            banks = [bank.strip() for bank in generated_text.split('\n') if bank.strip()]
            return banks
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with the LLM API: {e}")
            return None

if __name__ == "__main__":
    try:
        bot = LoanChatBot()
        bot.start()
    except ValueError as ve:
        print(ve)
