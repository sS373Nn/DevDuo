import os
from dotenv import load_dotenv
import time
from typing import Dict, List, Optional
from openai import OpenAI
import json

# Load environment variables
load_dotenv()

class Agent:
    """Base class for DevDuo agents"""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4')
        
        # Initialize OpenAI client
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = OpenAI(api_key=self.api_key)
        
        # Define system prompts for each agent type
        self.system_prompts = {
            "Writer Agent": """You are a skilled software developer focused on writing clean, functional code. 
            Your role is to:
            - Write initial implementations for coding tasks
            - Improve existing code based on reviewer feedback
            - Focus on functionality and clarity
            - Include code in ```python code blocks
            - Provide brief explanations of your approach
            
            Always structure your response with code blocks and explanations.""",
            
            "Reviewer Agent": """You are an experienced code reviewer focused on improvement and best practices.
            Your role is to:
            - Review code for correctness, efficiency, and best practices
            - Identify potential bugs or edge cases
            - Suggest specific improvements
            - Provide improved code when necessary
            - Include improved code in ```python code blocks
            
            Be constructive and specific in your feedback. If the code is already good, acknowledge it."""
        }
    
    def think(self, prompt: str) -> str:
        """Send prompt to OpenAI API and get response"""
        print(f"\n🤖 {self.name} is thinking...")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompts[self.name]},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            error_message = str(e)
            print(f"❌ Error with {self.name}: {error_message}")
            
            # Check for model access errors and exit gracefully
            if any(phrase in error_message.lower() for phrase in [
                'does not exist or you do not have access',
                'model_not_found',
                'insufficient_quota',
                'rate_limit_exceeded'
            ]):
                self._handle_critical_error(error_message)
            
            return f"Error: Could not get response from {self.name}. Please check your API key and connection."
    
    def _handle_critical_error(self, error_message: str):
        """Handle critical API errors that should stop the program"""
        print("\n" + "=" * 50)
        print("💥 CRITICAL ERROR")
        print("=" * 50)
        
        if 'does not exist or you do not have access' in error_message:
            print(f"❌ Model '{self.model}' is not available with your API key.")
            print("This usually means:")
            print("  • You selected a model your account can't access")
            print("  • Free accounts typically only have access to gpt-3.5-turbo")
            print("  • GPT-4 models require a paid account with usage history")
            print(f"\n💡 Try running the program again and selecting 'gpt-3.5-turbo'")
            
        elif 'insufficient_quota' in error_message:
            print("❌ You've exceeded your API quota (out of credits).")
            print("💳 Please add credits to your OpenAI account and try again.")
            
        elif 'rate_limit_exceeded' in error_message:
            print("❌ Rate limit exceeded.")
            print("⏰ Please wait a moment and try again.")
            
        else:
            print(f"❌ API Error: {error_message}")
            print("🔧 Please check your OpenAI API key and account status.")
        
        print("\n👋 Exiting DevDuo...")
        exit(1)

class DevDuo:
    """Main DevDuo system orchestrating two agents"""
    
    def __init__(self, selected_model: str = None):
        # If a model is explicitly selected, use it. Otherwise use env default
        model_to_use = selected_model or os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        
        self.writer = Agent("Writer Agent", "Code Writer")
        self.reviewer = Agent("Reviewer Agent", "Code Reviewer")
        
        # Override the model for both agents
        self.writer.model = model_to_use
        self.reviewer.model = model_to_use
        
        self.conversation_history = []
        self.current_model = model_to_use
    
    def collaborate(self, task: str, max_iterations: int = 3, verbose: bool = True) -> Dict:
        """Main collaboration method"""
        print(f"\n🚀 DevDuo Starting Collaboration")
        print(f"📝 Task: {task}")
        print("=" * 50)
        
        self.conversation_history = []
        current_code = ""
        
        for iteration in range(max_iterations):
            print(f"\n📍 Iteration {iteration + 1}/{max_iterations}")
            
            # Writer creates or improves code
            if iteration == 0:
                writer_prompt = f"""Please write code for this task: {task}

Requirements:
- Write clean, functional Python code
- Include proper error handling where appropriate
- Add brief comments explaining your approach
- Make sure the code is ready to run"""
            else:
                writer_prompt = f"""Please improve this code based on the reviewer's feedback:

Original task: {task}

Previous code:
{current_code}

Reviewer feedback:
{self.conversation_history[-1]['content']}

Please provide an improved version that addresses the reviewer's concerns."""
            
            writer_response = self.writer.think(writer_prompt)
            
            if verbose:
                print(f"\n💬 {self.writer.name}:")
                print(writer_response)
            
            self.conversation_history.append({
                'agent': self.writer.name,
                'content': writer_response,
                'iteration': iteration + 1
            })
            
            # Extract code from writer response
            current_code = self._extract_code(writer_response)
            
            # Small delay to respect API rate limits
            time.sleep(1)
            
            # Reviewer analyzes the code
            reviewer_prompt = f"""Please review this code for the task: '{task}'

Code to review:
{writer_response}

Please provide:
1. What the code does well
2. Any issues or improvements needed
3. Specific suggestions for enhancement
4. If improvements are needed, provide updated code

Be thorough but constructive in your review."""
            
            reviewer_response = self.reviewer.think(reviewer_prompt)
            
            if verbose:
                print(f"\n💬 {self.reviewer.name}:")
                print(reviewer_response)
            
            self.conversation_history.append({
                'agent': self.reviewer.name,
                'content': reviewer_response,
                'iteration': iteration + 1
            })
            
            # Small delay to respect API rate limits
            time.sleep(1)
            
            # Check if reviewer is satisfied (improved heuristic)
            if self._is_satisfied(reviewer_response) and iteration > 0:
                print(f"\n✅ Collaboration complete! Reviewer is satisfied.")
                break
        
        # Get final code (prefer reviewer's improved version if available)
        final_code = self._get_final_code()
        
        return {
            'task': task,
            'final_code': final_code,
            'conversation_history': self.conversation_history,
            'iterations': len(self.conversation_history) // 2
        }
    
    def _extract_code(self, response: str) -> str:
        """Extract code blocks from agent responses"""
        lines = response.split('\n')
        code_lines = []
        in_code_block = False
        
        for line in lines:
            if line.strip().startswith('```python'):
                in_code_block = True
                continue
            elif line.strip().startswith('```') and in_code_block:
                in_code_block = False
                continue
            elif in_code_block:
                code_lines.append(line)
        
        return '\n'.join(code_lines) if code_lines else "# No code block found"
    
    def _get_final_code(self) -> str:
        """Get the best final code from the conversation"""
        # Look for the most recent code block from either agent
        for entry in reversed(self.conversation_history):
            code = self._extract_code(entry['content'])
            if code and code != "# No code block found":
                return code
        
        return "# No final code found"
    
    def _is_satisfied(self, reviewer_response: str) -> bool:
        """Improved heuristic to check if reviewer is satisfied"""
        # Look for positive indicators
        satisfied_indicators = [
            'looks good', 'well done', 'excellent', 'perfect', 'solid implementation',
            'great job', 'this is good', 'good work', 'nicely done', 'well implemented'
        ]
        
        # Look for major concern indicators
        concern_indicators = [
            'major issue', 'significant problem', 'needs improvement', 'several issues',
            'should be fixed', 'must be addressed', 'critical problem'
        ]
        
        response_lower = reviewer_response.lower()
        
        # If there are major concerns, not satisfied
        if any(concern in response_lower for concern in concern_indicators):
            return False
        
        # If there are satisfied indicators, consider satisfied
        if any(indicator in response_lower for indicator in satisfied_indicators):
            return True
        
        # Default to not satisfied to allow for more iterations
        return False
    
    def save_result(self, result: Dict, filename: str = "devduo_result.json"):
        """Save collaboration result to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Results saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving results: {str(e)}")

def get_available_models():
    """Get list of available chat models from OpenAI API"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return []
    
    try:
        client = OpenAI(api_key=api_key)
        models = client.models.list()
        
        # Filter for chat models
        chat_models = []
        for model in models.data:
            if any(keyword in model.id for keyword in ['gpt-3.5', 'gpt-4', 'turbo']):
                chat_models.append(model.id)
        
        return sorted(chat_models)
    except Exception as e:
        print(f"⚠️  Could not fetch models: {str(e)}")
        return []

def select_model(available_models):
    """Let user select a model from available options"""
    if not available_models:
        print("⚠️  No models detected. Using default: gpt-3.5-turbo")
        return 'gpt-3.5-turbo'
    
    print(f"\n🔍 Found {len(available_models)} available models:")
    print("-" * 40)
    
    for i, model in enumerate(available_models, 1):
        print(f"{i}. {model}")
    
    print("\nChoose a model number or press Enter for default:")
    choice = input("> ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= len(available_models):
        selected = available_models[int(choice) - 1]
        print(f"✅ Selected: {selected}")
        return selected
    else:
        default = available_models[0]  # First in sorted list
        print(f"✅ Using default: {default}")
        return default

def main():
    """Main function to run DevDuo"""
    print("🤖 Welcome to DevDuo - AI Pair Programming System")
    print("=" * 50)
    
    # Check for API key
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY environment variable is required")
        print("Please set your OpenAI API key in your .env file")
        return
    
    # Get available models and let user choose
    print("\n🔍 Checking available models...")
    available_models = get_available_models()
    selected_model = select_model(available_models)
    
    # Initialize DevDuo with selected model
    try:
        duo = DevDuo(selected_model)
    except ValueError as e:
        print(f"❌ Error: {str(e)}")
        return
    
    # Example tasks
    example_tasks = [
        "Write a function to calculate fibonacci numbers efficiently",
        "Write a function to reverse a string with proper error handling",
        "Write a function to check if a number is prime",
        "Write a function to find the longest palindrome in a string",
        "Write a function to implement binary search"
    ]
    
    print("\nExample tasks:")
    for i, task in enumerate(example_tasks, 1):
        print(f"{i}. {task}")
    
    # Get user input
    print("\nChoose an example task (1-5) or enter your own:")
    user_input = input("> ").strip()
    
    if user_input.isdigit() and 1 <= int(user_input) <= len(example_tasks):
        task = example_tasks[int(user_input) - 1]
    else:
        task = user_input if user_input else example_tasks[0]
    
    # Run collaboration
    print(f"\n🔄 Starting collaboration with {duo.current_model}")
    print(f"📝 Task: {task}")
    result = duo.collaborate(task, verbose=True)
    
    # Show final results
    print("\n" + "=" * 50)
    print("🎯 FINAL RESULTS")
    print("=" * 50)
    print(f"Task: {result['task']}")
    print(f"Iterations: {result['iterations']}")
    print(f"\nFinal Code:")
    print(result['final_code'])
    
    # Ask if user wants to save results
    save_choice = input("\nWould you like to save the results to a file? (y/n): ").strip().lower()
    if save_choice == 'y':
        duo.save_result(result)

if __name__ == "__main__":
    main()
