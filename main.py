import os
import argparse
from prompts import system_prompt
from google import genai
from google.genai import types
from dotenv import load_dotenv
from call_function import available_functions, call_function

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

    final_response = None

    for _ in range(20):

        response = client.models.generate_content(model="gemini-2.5-flash", contents=messages,
                                              config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))

        if response.usage_metadata == None:
            raise RuntimeError("API request failed.")
    
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        for candidate in response.candidates:
            messages.append(candidate.content)

        if response.function_calls:
            function_results = []
            for func_call in response.function_calls:
                func_result = call_function(func_call, args.verbose)
                if not len(func_result.parts) or not func_result.parts[0].function_response or not func_result.parts[0].function_response.response:
                    raise Exception("didn't get valid response from function call.")
                function_results.append(func_result.parts[0])
                if args.verbose:
                    print(f"-> {func_result.parts[0].function_response.response}")
                messages.append(types.Content(role="user", parts=function_results))

        else:
            final_response = response.text
            break
    
    if final_response is None:
        print("Error: Maximum number of iterations reached")
        exit(1)
    else:
        print(final_response)

if __name__ == "__main__":
    main()
