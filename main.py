import os
import argparse
from prompts import system_prompt
from google import genai
from google.genai import types
from dotenv import load_dotenv
from call_function import available_functions

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key == None:
        raise RuntimeError("Gemini API key not found.")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(model="gemini-2.5-flash", contents=messages,
                                              config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))

    if response.usage_metadata == None:
        raise RuntimeError("API request failed.")
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
    if len(response.function_calls) > 0:
        for func_call in response.function_calls:
            print(f"Calling function: {func_call.name}({func_call.args})")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
