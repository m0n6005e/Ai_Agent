import argparse
import sys
import os
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function, available_functions

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None:
    raise RuntimeError("api key not found")


from google import genai

client = genai.Client(api_key=api_key)



def main():
    #print("Hello from ai-agent!")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt") #
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])] 

    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature=0),

    )
    if response.usage_metadata == None:
        raise RuntimeError("API request failed")

    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}") 
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls != None:
        function_results = []

        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=args.verbose)
            if not function_call_result.parts:
                 raise Exception("No parts in result")
            
            if not function_call_result.parts[0].function_response:
                raise Exception("Not a FunctionResponse object")
            
            if not function_call_result.parts[0].function_response.response:
                raise Exception("response field not an object")
            
            function_results.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")


    else:
        print(response.text)


if __name__ == "__main__":
    main()
