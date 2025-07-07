import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def check_available_models():
    """Check which models are available with your API key"""
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        return
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Get list of available models
        print("🔍 Checking available models...")
        models = client.models.list()
        
        # Filter for chat models (the ones we care about)
        chat_models = []
        for model in models.data:
            if any(keyword in model.id for keyword in ['gpt-3.5', 'gpt-4', 'turbo']):
                chat_models.append(model.id)
        
        print(f"\n✅ Found {len(chat_models)} chat models available:")
        print("-" * 50)
        
        for model in sorted(chat_models):
            print(f"  📝 {model}")
        
        # Recommend which one to use
        print("\n💡 Recommendations:")
        if any('gpt-4' in model for model in chat_models):
            gpt4_models = [m for m in chat_models if 'gpt-4' in m]
            print(f"  🌟 Use GPT-4: {gpt4_models[0]} (most capable)")
        
        if any('gpt-3.5-turbo' in model for model in chat_models):
            print("  💰 Use gpt-3.5-turbo (cost-effective)")
        
        print(f"\n🔧 Update your .env file with:")
        print(f"OPENAI_MODEL=gpt-3.5-turbo")
        
    except Exception as e:
        print(f"❌ Error checking models: {str(e)}")
        print("\nThis might indicate:")
        print("  - Invalid API key")
        print("  - No internet connection")
        print("  - API key doesn't have proper permissions")

if __name__ == "__main__":
    check_available_models()
