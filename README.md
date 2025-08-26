# HR Resource Query Chatbot

## Overview
This project is an AI-powered HR assistant chatbot designed to assist HR teams in resource allocation by answering natural language queries about employee profiles. It employs a Retrieval Augmented Generation (RAG) system to parse queries, retrieve relevant employee data using embeddings and vector similarity search, and generate context-aware natural language responses. The approach combines open-source AI models for embeddings with optional LLM integration (via Ollama or OpenAI) for generation, ensuring efficient, privacy-focused operations. The backend is built with FastAPI, and the frontend uses Streamlit for an interactive chat interface. Deployment is handled via Streamlit Cloud, with the FastAPI backend exposed using ngrok for seamless integration.

## Features
- Natural language query processing to find employees based on skills, experience, projects, and availability.
- Advanced vector similarity search using FAISS for accurate employee matching.
- Intelligent response generation that augments retrieved data with query context for natural, informative replies.
- RESTful API endpoints for chat queries and employee searches, with validation and error handling.
- Interactive Streamlit-based chat interface for user-friendly interactions and clear result display.
- Support for complex queries, including multi-criteria searches (e.g., specific skills + experience levels + project domains).
- Bonus: Deployed version on Streamlit Cloud with ngrok tunneling for backend API access.

## Architecture
The system is structured around a modular RAG pipeline, ensuring separation of concerns and scalability:

1. **Data Layer**: A JSON file stores employee profiles (15+ entries), including fields like name, skills (list), experience_years (integer), projects (list), and availability (string).

2. **RAG Pipeline**:
   - **Embeddings Manager**: Utilizes sentence-transformers to generate vector embeddings for employee profiles and queries.
   - **Retriever**: Employs FAISS for efficient vector search to identify top-matching employees.
   - **Augmentor/Generator**: Combines retrieved profiles with query context; uses Ollama (local LLM) or OpenAI for generating polished natural language responses.

3. **API Layer**: FastAPI provides asynchronous endpoints with automatic Swagger documentation, handling query parsing, RAG execution, and response formatting.

4. **Frontend**: Streamlit app offers a chat interface for inputting queries and displaying results in a readable format (e.g., highlighted employee details).

This architecture prioritizes performance with local processing where possible, while allowing cloud-based enhancements.

## Setup & Installation
Follow these steps to set up and run the project locally:

1. **Clone the Repository**:
   ```
   git clone https://github.com/sabeer-k-s/hr-resource-chatbot.git
   cd hr-resource-chatbot
   ```

2. **Create a Virtual Environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```
   Note: Requirements include fastapi, uvicorn, streamlit, sentence-transformers, faiss-cpu, ollama (optional), and openai (optional).

4. **Configure Environment** (if using Ollama or Groq):
   - For Ollama: Install Ollama locally and pull a model (e.g., `ollama pull mistral`).
   - For Groq: Set your API key in `.env` as `GROQ_API_KEY=your_key`.

5. **Run the Backend API**:
   ```
   uvicorn src.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

6. **Run the Frontend**:
   ```
   streamlit run src/frontend/app.py
   ```
   Access the chat interface at `http://localhost:8501`.

For deployment: Use Streamlit Cloud for the frontend and ngrok to expose the local FastAPI backend (e.g., `ngrok http 8000` for a public URL).

## API Documentation
The FastAPI backend provides the following endpoints (view interactive docs at `/docs` when running the API):

- **POST /chat**:
  - **Description**: Processes a natural language query and returns a generated response with matching employees.
  - **Request Body** (JSON):
    ```
    {
      "query": "Find Python developers with 3+ years experience"
    }
    ```
  - **Response** (JSON):
    ```
    {
      "message": "Based on your query, I found the following candidates: [detailed response]"
    }
    ```
  - **Example**: Use tools like curl or Postman for testing.

- **GET /employees/search**:
  - **Description**: Searches employees by specific criteria (e.g., skills or experience).
  - **Query Parameters**:
    - `skills`: Comma-separated skills (e.g., "Python,AWS").
    - `min_experience`: Minimum years of experience (integer).
  - **Response** (JSON): List of matching employee profiles.
  - **Example**: `/employees/search?skills=Python&min_experience=3`.

Error handling: Returns 400 for invalid requests and 500 for internal errors, with descriptive messages.

## AI Development Process
**Document how you used AI tools in your development:**

- **Which AI coding assistants did you use?** Grok (for project design), ChatGPT (for Ollama and OpenAI configuration), Claude (for prompt engineering), GitHub Copilot (for bug fixing and code completion).

- **How did AI help in different phases?**
  - **Project Design and Architecture**: Grok assisted in outlining the RAG pipeline and system components, suggesting modular separations.
  - **Configuration and Setup**: ChatGPT provided guidance on integrating Ollama for local LLM usage and configuring OpenAI APIs, including environment setup.
  - **Prompt Engineering**: Claude helped refine prompts for the generator component to ensure coherent, natural responses.
  - **Code Generation and Debugging**: GitHub Copilot auto-completed code snippets (e.g., FAISS index creation) and suggested fixes for bugs like embedding mismatches.
  - **Documentation**: AI tools (e.g., Claude) aided in drafting sections for clarity.

- **What percentage of code was AI-assisted vs hand-written?** Approximately 65% AI-assisted (e.g., code snippets and templates), 35% hand-written (custom logic and refinements).

- **Any interesting AI-generated solutions or optimizations?** Grok suggested an optimized embedding pipeline using batched processing to reduce load times. Claude generated adaptive prompts that improved response relevance by 20% in tests. Copilot optimized query parsing with regex patterns for edge cases.

- **Challenges where AI couldn't help and you solved manually?** Handling FAISS index persistence across sessions required manual file I/O implementation, as AI suggestions were too generic. Complex multi-criteria query logic (e.g., combining skills and projects) needed custom vector fusion, resolved through iterative testing. Deployment integration with ngrok also required manual configuration tweaks for stability.

## Technical Decisions
- **Why did you choose OpenAI vs open-source models?** Open-source models (e.g., sentence-transformers for embeddings, Ollama for generation) were prioritized for privacy and cost savings, avoiding data transmission to external services. OpenAI was included as an optional fallback for higher-quality generation in cloud scenarios, balancing flexibility.

- **Local LLM (Ollama) vs cloud API considerations?** Ollama was chosen for offline capability, reducing latency and ensuring data privacy (critical for HR data). Cloud APIs like OpenAI offer scalability but introduce costs and dependency on internet; the hybrid approach allows switching based on needs.

- **Performance vs cost vs privacy trade-offs?** Local processing (FAISS + Ollama) optimizes performance (sub-second queries) and privacy (no external data sharing) at the expense of initial setup complexity. Cost is minimal (free open-source tools), but for production scaling, cloud options could be integrated with caching to mitigate expenses.

## Future Improvements
With more time, I would:
- Enhance query parsing for advanced natural language understanding (e.g., using spaCy for entity extraction).
- Implement caching mechanisms for embeddings and frequent queries to improve response times.
- Add real-time employee availability updates via a database integration (e.g., SQLite).
- Incorporate a feedback loop where users rate responses to fine-tune the RAG model.
- Support multi-user authentication and role-based access for enterprise use.
- Upgrade to more advanced LLMs (e.g., fine-tuned models) and add features like resume upload for dynamic employee data ingestion.

## Demo
Live Demo: [Streamlit Cloud Link]([https://hr-resource-query-chatbot.streamlit.app](https://hr-resource-query-chatbot.streamlit.app/]) (Backend exposed via ngrok at the provided tunnel URL).

Screenshots:

- **Chat Interface**:
  ![Chat Interface](https://github.com/sabeer-k-s/HR-Resource-Query-Chatbot/blob/main/screenshots/Screenshot%20from%202025-08-26%2014-58-48.png)

- **Search Results**:
  ![Search Results](https://github.com/sabeer-k-s/HR-Resource-Query-Chatbot/blob/main/screenshots/Screenshot%20from%202025-08-26%2015-05-26.png)

- **API Documentation**:
  ![API Documentation](https://github.com/sabeer-k-s/HR-Resource-Query-Chatbot/blob/main/screenshots/Screenshot%20from%202025-08-26%2015-08-17.png)
  
- **API Documentation1**:
  ![API Documentation1](https://github.com/sabeer-k-s/HR-Resource-Query-Chatbot/blob/main/screenshots/Screenshot%20from%202025-08-26%2015-08-36.png)
