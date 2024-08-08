import os
import requests

class LoanChatBot:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY") 
        self.loan_type = None
        self.employment_status = None
        self.gemini_api_endpoint = "https://api.gemini.google.com/v1/generateText"  # Replace with actual endpoint

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
        if not self.employment_status:
            self.employment_status = input("What is your employment status? ")
        self.confirmation_and_search()

    def confirmation_and_search(self):
        print(f"Loan Type: {self.loan_type}")
        print(f"Employment Status: {self.employment_status}")
        confirm = input("Is this information correct? (yes/no): ").strip().lower()
        if confirm == "yes":
            self.search_banks(self.loan_type)
        else:
            self.start()

    def classify_loan_type(self, user_input):
        keywords_to_loan_type = {
            "home": "Home Loan",
            "property": "Loan Against Property (LAP)",
            "insurance": "Loan Against Insurance Policies",
            "gold": "Gold Loan",
            "mutual funds": "Loan Against Mutual Funds and Shares",
            "fixed deposit": "Loan Against Fixed Deposit",
            "personal": "Personal Loan",
            "business": "Short Term Business Loan"
        }
        for keyword, loan_type in keywords_to_loan_type.items():
            if keyword in user_input.lower():
                return loan_type
        return None

    def search_banks(self, category):
        print(f"Searching for banks that offer {category}...")
        results = self.llm_search(category) 
        print("Here are some banks that might match your criteria:")
        if results:
            for result in results:
                print(f"- {result}")
        else:
            print("No relevant results found. Please try again or refine your search.")

    def llm_search(self, category):
        # 1. Prepare Prompt for Gemini: 
        prompt = f"A user is looking for a {category}. What are some banks or financial institutions that typically offer {category}s?" 

        # 2. Make API Call (replace with actual Gemini API call)
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "prompt": prompt,
            # ... other parameters like temperature, max_tokens, etc.
        }
        response = requests.post(self.gemini_api_endpoint, headers=headers, json=data) 

        # 3. Process the Response
        if response.status_code == 200:
            response_data = response.json()
            # Extract the generated text (bank names) from Gemini's response
            generated_text = response_data['choices'][0]['text'] # Assuming Gemini's response structure
            # Split the generated text into a list of banks
            banks = generated_text.split('\n') 
            return banks 
        else:
            print("Error communicating with the LLM API.")
            return None

if __name__ == "__main__":
    bot = LoanChatBot()
    bot.start()
