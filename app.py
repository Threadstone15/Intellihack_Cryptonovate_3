from generativeai import TextGenerationRequest, GenerativeModel

# Replace with your API key
API_KEY = "YOUR_API_KEY"

# Initialize the API
generative_model = GenerativeModel("gemini-pro", api_key=AIzaSyBpxppXt_LOWCOdykw4QDRmXtyxN76ING0)

def generate_response(user_input):
  """
  Sends user input to Gemini and returns the generated response.
  """
  request = TextGenerationRequest(
      prompt="USER: " + user_input + "\nBOT: ",
      max_tokens=64  # Maximum length of response
  )
  response = generative_model.generate(request)
  return response.generated_text[0].strip()

# Example conversation flow
while True:
  user_input = input("You: ")
  bot_response = generate_response(user_input)
  print("Bot:", bot_response)
  if user_input.lower() == "bye":
    break

print("Conversation ended.")
