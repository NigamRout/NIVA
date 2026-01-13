import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    # Load environment variables from .env file
    load_dotenv()                                       # loading Environment variable from .env file
    # load_dotenv('./../../AI.env')                       # loading Environment variable from a specific .env file
    # load_dotenv(os.getenv("CREDENTIAL_STORE_FILE_AI"))  # loading Environment variable from a specific .env file

    # Get API KEY and Model name from .env file and if not found then Error out 
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME")
    if not GEMINI_API_KEY: raise EnvironmentError("GEMINI_API_KEY not found in environment variables.")
    if not GEMINI_MODEL_NAME: raise EnvironmentError("GEMINI_MODEL_NAME not found in environment variables.")
    print(f"Using Model: {GEMINI_MODEL_NAME} \n")

    # User query to send to Gemini AI model
    user_query = "Explain how AI works in 3 lines"

    # Initialize Gemini AI client with the API key
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)

    # Communicating with Gemini LLM model
    gemini_response = gemini_client.models.generate_content(
                    model=GEMINI_MODEL_NAME,
                    contents=user_query,
                    config=types.GenerateContentConfig(  
                        thinking_config=types.ThinkingConfig(thinking_budget=0) # Disable model's "thinking" process for faster response
                    ),
                )

    print(f"[💻 User Query]: {user_query}\n")
    print(f"[🤖 AI Response]: {gemini_response.text}")



if __name__ == "__main__":
    main()