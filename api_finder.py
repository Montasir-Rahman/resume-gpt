import google.generativeai as genai
import os

# Configure your API key
# It's best practice to load your API key from environment variables
# For example: os.environ.get("GEMINI_API_KEY")
genai.configure(api_key="AIzaSyAa-VqP0bXlcQnQye-WudxnIfT_Vsa9ENU") 

for m in genai.list_models():
  # Filter for models that support generating content (text, multimodal)
  if "generateContent" in m.supported_generation_methods:
    print(f"Model Name: {m.name}")
    print(f"  Display Name: {m.display_name}")
    print(f"  Description: {m.description}")
    print(f"  Input Token Limit: {m.input_token_limit}")
    print(f"  Output Token Limit: {m.output_token_limit}")
    print("-" * 30)