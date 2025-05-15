# NetKeeper - Network Security Assistant

## Chatbot Integration Setup

To enable the chatbot functionality, follow these steps:

1. Create a `.env` file in the root directory of the project
2. Add the following environment variables:
   ```
   CHATBOT_API_KEY=your_api_key_here
   CHATBOT_API_URL=your_api_endpoint_here
   ```
3. Replace the placeholder values with your actual API credentials
4. Never commit the `.env` file to version control

### Security Notes
- Keep your API keys secure and never expose them in the code
- Use environment variables for all sensitive information
- The `.env` file is automatically ignored by git
- API requests are made with proper authentication headers
- Error handling is implemented to protect sensitive information

### API Integration
The chatbot integration uses a secure API connection with:
- Bearer token authentication
- JSON payload format
- Error handling and timeout protection
- Fallback responses for API unavailability

## Running the Application
1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables
3. Run the application: `streamlit run app.py`