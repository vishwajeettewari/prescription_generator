from flask import Flask, request, render_template, jsonify
import openai

# Create a Flask app
app = Flask(__name__)

# Define a route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the user's message from the form
        user_message = request.form.get('user_message')
        
        # Get the API key from the query parameter in the URL
        api_key = request.args.get('api_key')

        # Check if an API key is provided in the URL
        if not api_key:
            return "API key is missing in the URL. Please provide the 'api_key' parameter."

        # Initialize the OpenAI API client with the provided API key
        openai.api_key = api_key

        # Create a list of messages to simulate a conversation
        messages = [
            {'role': 'system', 'content': """Generate a prescription for [patient name] who is [age] years old and has been diagnosed with [medical condition]. The patient is experiencing [symptoms]. Please include the following information in the prescription:
            - Medication name, dosage, and frequency
            - Any special instructions or precautions
            - Dietary recommendations, if applicable
            - Follow-up appointment details

            [Additional context or specific requests can be added here if needed.]
             """},
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": "- Medication name, dosage, and frequency\n- Any special instructions or precautions\n- Dietary recommendations, if applicable\n- Follow-up appointment details"},
        ]

        # Generate a response using the ChatCompletion model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use the turbo model for better performance
            messages=messages,
            max_tokens=500,  # Adjust this based on the desired response length
        )

        # Extract the assistant's reply
        assistant_reply = response.choices[0].message["content"]
        assistant_reply = assistant_reply.split('\n')

        return render_template('index.html', user_message=user_message, assistant_reply=assistant_reply)

    return render_template('index.html', user_message=None, assistant_reply=None)

if __name__ == '__main__':
    app.run(debug=True)
