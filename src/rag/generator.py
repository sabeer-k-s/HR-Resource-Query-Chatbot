from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
from groq import Groq
from collections import deque
import pandas as pd

# Load environment variables from .env file
load_dotenv()

class Generator:
    def __init__(self, model_name: str = "llama-3.1-8b-instant"):
        """
        Initialize the Generator with a Groq model and conversation history.

        Args:
            model_name (str): Name of the Groq model (e.g., 'mixtral-8x7b-32768').
        """
        self.model_name = model_name
        self.conversation_history = deque(maxlen=3)  # Store up to 3 previous query-response pairs
        
        # Initialize Groq client
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
        self.groq_client = Groq(api_key=api_key)

        # OPENAI START: Commented out for Groq implementation
        # api_key = os.getenv("OPENAI_API_KEY")
        # if not api_key:
        #     raise ValueError("OPENAI_API_KEY not found in .env file")
        # self.openai_client = OpenAI(api_key=api_key)
        # OPENAI END

        # OLLAMA START: Commented out for Groq implementation
        # self.llm_provider = os.getenv("LLM_PROVIDER", "ollama").lower()
        # if self.llm_provider == "ollama":
        #     self.model_name = "mistral"  # Default Ollama model
        # OLLAMA END

    def generate_response(self, query: str, employees: Optional[List[Dict]] = None) -> str:
        """
        Generate a natural language response using Groq based on the query, optional employee data, and conversation history.
        Respond human-like for greetings or general queries, using RAG-based content for talent-related queries.

        Args:
            query (str): User query (e.g., "Hi" or "Find Python developers with 3+ years experience").
            employees (Optional[List[Dict]]): List of employee dictionaries from the retriever, or None if not applicable.

        Returns:
            str: Generated natural language response.
        """
        # Handle employee data
        context = ""
        valid_employees = []
        required_keys = {'name', 'skills', 'experience_years', 'projects', 'availability'}

        if employees:
            # Handle if employees is a DataFrame (from retriever)
            if isinstance(employees, pd.DataFrame):
                try:
                    if not all(col in employees.columns for col in required_keys):
                        missing = set(required_keys) - set(employees.columns)
                        return f"Error: Employee data missing columns: {missing}. Please check the retriever output."
                    valid_employees = employees[list(required_keys)].to_dict(orient='records')
                except Exception as e:
                    return f"Error processing employee DataFrame: {str(e)}"
            else:
                # Validate list of dictionaries
                valid_employees = [
                    emp for emp in employees
                    if isinstance(emp, dict) and required_keys.issubset(emp.keys())
                ]
                if not valid_employees and employees:
                    return f"Error: No valid employee data provided. Missing keys in some records."

            # Format employee data into context
            if valid_employees:
                context = "\n".join([
                    f"- {emp['name']}: {emp['experience_years']} years, "
                    f"Skills: {', '.join(emp['skills'])}, "
                    f"Projects: {', '.join(emp['projects'])}, "
                    f"Availability: {emp['availability']}"
                    for emp in valid_employees
                ])
                context = f"Available Candidates:\n{context}\n\n"

        # Format conversation history (up to 3 previous interactions)
        history_context = ""
        if self.conversation_history:
            history_context = "\n\nPrevious Conversation:\n"
            for i, (prev_query, prev_response) in enumerate(self.conversation_history, 1):
                history_context += f"Interaction {i}:\nQuery: {prev_query}\nResponse: {prev_response}\n\n"

        # Enhanced prompt for human-like conversational mode with intent detection
        prompt = (
            f"{history_context}"
            f"Current Query: {query}\n\n"
            f"{context if valid_employees else ''}"
            "You are a professional HR assistant specializing in candidate recommendations.\n\n"
            "INSTRUCTIONS: Always reply using the following format and rules when responding to role/candidate search queries:\n"
            "\n"
            "### Top Candidates\n"
            "- For each match, start with **bolded name** and a short, convincing summary (1–2 sentences).\n"
            "- Add a bullet point list under each: Skills, Experience, Notable Projects, and Availability.\n"
            "- Highlight domain/project alignment (e.g., 'healthcare', 'machine learning').\n"
            "\n"
            "### Why They’re A Fit\n"
            "- Briefly explain for each top candidate why their experience, projects, or skills make them perfect for this request."
            "\n"
            "### Next Steps\n"
            "- Suggest a concrete next step, such as offering to share more project details, check availability, or schedule introductions."
            "\n"
            "If NO suitable candidates are found, clearly state this and suggest how the user might broaden or clarify their criteria.\n"
            "For greetings or unrelated queries, respond warmly and helpfully as an HR assistant.\n"
            "Always keep your answer concise and use markdown for clear presentation."
        )


        try:
            # Use Groq API to generate response
            response = self.groq_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a friendly, professional HR assistant. Respond naturally and human-like. "
                            "Analyze the query and conversation history to determine intent. "
                            "Use candidate data only for talent-related queries. Handle greetings warmly. "
                            "Provide detailed recommendations when relevant, with examples and formatting. "
                            "Always offer next steps. Be engaging and consultative."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.5
            )
            generated_response = response.choices[0].message.content.strip()

            # Store the query and response in conversation history
            self.conversation_history.append((query, generated_response))
            return generated_response

        except Exception as e:
            return f"I apologize, but I'm experiencing a technical issue while processing your request. Please try again shortly, or let me know if I'd like assistance in a different way. Error: {str(e)}"

        # OPENAI START: Commented out for Groq implementation
        # response = self.openai_client.chat.completions.create(
        #     model=self.model_name,
        #     messages=[
        #         {"role": "system", "content": "You are a professional HR assistant specializing in talent matching. Provide detailed, well-structured recommendations with specific examples and professional formatting. Always explain why candidates are good fits and offer helpful next steps."},
        #         {"role": "user", "content": prompt}
        #     ],
        #     max_tokens=600,
        #     temperature=0.3
        # )
        # return response.choices[0].message.content.strip()
        # OPENAI END

        # OLLAMA START: Commented out for Groq implementation
        # if self.llm_provider == "ollama":
        #     import ollama
        #     response = ollama.generate(model=self.model_name, prompt=prompt)
        #     return response["response"].strip()
        # OLLAMA END