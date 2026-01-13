import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from RealtimeSTT import AudioToTextRecorder


# https://www.gyan.dev/ffmpeg/builds/
# https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z
# Extract .7z to a location and add the 'bin' folder to your system PATH.
# Restart Terminal and check "ffmpeg -version" 


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

    # Define system instruction
    my_system_instruction = "My name is NIVA"
    my_system_instruction += """You are an Expert Site Reliability Engineer with experience in DevOps, DevSecOps, Cloud,
                             distributed systems, high-scale cloud-native architectures (Kubernetes, Multi-cloud), and 
                             advanced automation. Give the answer in bulletpoints wherever possible and keep the answers 
                             concise and precise. If asked to write code, then write code only, do not explain at end."""

    # # User query to send to Gemini AI model
    # user_query = "Tell me a story about me"

    # Initialize Gemini AI client with the API key
    llm = genai.Client(api_key=GEMINI_API_KEY)

    # Communicating with Gemini AI model
    chat = llm.chats.create(
                    model=GEMINI_MODEL_NAME,
                    # contents=user_query,
                    config=types.GenerateContentConfig( 
                        system_instruction=my_system_instruction,   
                        thinking_config=types.ThinkingConfig(thinking_budget=0) 
                    ),
                )

    # Initializing audio recorder for listening process
    recorder = AudioToTextRecorder(model="tiny.en", language="en", spinner=False)

    # Loop to send user message and receive response in streaming mode
    while True:
        try:
            # Get user input from audio recorder
            print("[💻 You]: ", end="")
            user_input = recorder.text()
            print(user_input)

            # Exit condition based on user input
            if user_input.lower().strip(" .!?") in ['exit', 'quit', 'bye']:
                print("🏆 Exiting chat as per instruction.")

                # Shutdown audio recorder listening process
                recorder.shutdown()
                break

            # Send user message to the chat model
            response = chat.send_message_stream(user_input)

            # Print the response as it streams in
            print(f"[🤖 LLM]: ", end="")
            for chunk in response:
                print(chunk.text, end="", flush=True)
            print()  # For newline after the response

        except KeyboardInterrupt:
            print("\n🟡 Interrupted through Keyboard, Exiting chat!")
            break
        except Exception as e:
            print(f"🔴 An Error occured: {e}")
            break



if __name__ == "__main__":
    main()