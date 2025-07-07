# DevDuo

A multi-agent AI coding system where two AI agents collaborate in real-time to write and improve code using OpenAI's API.

## What is DevDuo?

DevDuo is a collaborative AI coding system that demonstrates multi-agent AI collaboration for programming tasks. It uses two specialized OpenAI-powered agents working together:

- **Writer Agent**: Takes coding tasks and writes initial implementations
- **Reviewer Agent**: Reviews code, identifies issues, and suggests improvements

The agents iterate together through multiple rounds to refine solutions, simulating real developer collaboration with AI assistance.

## Why DevDuo?

This project demonstrates:
- Multi-agent AI system architecture
- Real-time AI collaboration patterns
- Iterative code improvement processes
- OpenAI API integration for specialized agents
- Agent orchestration and communication
- Practical AI pair programming concepts

## How It Works

1. **User provides a coding task** (e.g., "Write a function to calculate fibonacci numbers")
2. **Writer Agent** creates the initial implementation using OpenAI API
3. **Reviewer Agent** analyzes the code and provides detailed feedback
4. **Agents iterate** up to 3 times, refining the solution based on feedback
5. **Final optimized code** is presented with full conversation history

## Features

✅ **Real OpenAI API Integration** - Uses GPT-3.5-turbo or GPT-4 models  
✅ **Dynamic Model Selection** - Choose from available models at runtime  
✅ **Intelligent Iteration** - Stops when reviewer is satisfied  
✅ **Comprehensive Error Handling** - Graceful handling of API errors  
✅ **Conversation History** - Complete record of agent interactions  
✅ **Code Extraction** - Automatically extracts code blocks from responses  
✅ **Result Persistence** - Save collaboration results to JSON files  
✅ **Rate Limit Compliance** - Built-in delays for API rate limiting  
✅ **Model Compatibility Check** - Verifies model access before running  

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/devduo.git
cd devduo

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=your_api_key_here
# OPENAI_MODEL=gpt-3.5-turbo  # or gpt-4 if available
```

## Prerequisites

- **OpenAI API Key**: Required for agent functionality
- **Python 3.7+**: For running the system
- **Internet Connection**: For API calls

### Getting an OpenAI API Key

1. Visit [OpenAI's website](https://openai.com/api/)
2. Create an account and navigate to API keys
3. Generate a new API key
4. Add it to your `.env` file

## Usage

### Basic Usage

```bash
# Run the interactive system
python devduo.py
```

### Programmatic Usage

```python
from devduo import DevDuo

# Initialize with specific model
duo = DevDuo(selected_model="gpt-3.5-turbo")

# Collaborate on a task
result = duo.collaborate("Write a function to reverse a string")

# Access results
print(f"Task: {result['task']}")
print(f"Iterations: {result['iterations']}")
print(f"Final Code:\n{result['final_code']}")

# Save results
duo.save_result(result, "my_collaboration.json")
```

### Check Available Models

```bash
# See which models your API key can access
python check_models.py
```

## Example Session

```
🤖 Welcome to DevDuo - AI Pair Programming System
==================================================

🔍 Checking available models...
✅ Found 3 chat models available:
1. gpt-3.5-turbo
2. gpt-4
3. gpt-4-turbo-preview

Choose a model number or press Enter for default:
> 1

📝 Task: Write a function to calculate fibonacci numbers efficiently

🤖 Writer Agent is thinking...
💬 Writer Agent: I'll create an efficient fibonacci function using memoization...

🤖 Reviewer Agent is thinking...
💬 Reviewer Agent: Good approach! The memoization will help with performance...

🎯 FINAL RESULTS
==================================================
Task: Write a function to calculate fibonacci numbers efficiently
Iterations: 2

Final Code:
def fibonacci(n, memo={}):
    """Calculate fibonacci number efficiently using memoization."""
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci(n-1, memo) + fibonacci(n-2, memo)
    return memo[n]
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
```

### Model Selection

The system supports dynamic model selection:
- **gpt-3.5-turbo**: Fast, cost-effective (recommended for most users)
- **gpt-4**: More capable, higher cost (requires paid account)
- **gpt-4-turbo-preview**: Latest capabilities (if available)

## Architecture

### Agent System

```
DevDuo
├── Writer Agent (OpenAI API)
│   ├── System Prompt: Code writing specialist
│   ├── Task: Create initial implementations
│   └── Iteration: Improve based on feedback
└── Reviewer Agent (OpenAI API)
    ├── System Prompt: Code review specialist
    ├── Task: Analyze and critique code
    └── Feedback: Provide specific improvements
```

### Collaboration Flow

1. **Task Input** → Writer Agent creates initial code
2. **Code Review** → Reviewer Agent analyzes and suggests improvements
3. **Iteration** → Writer Agent refines based on feedback
4. **Satisfaction Check** → System determines if more iterations needed
5. **Final Result** → Best code version with full history

## Error Handling

The system includes comprehensive error handling for:
- **Invalid API Keys**: Clear error messages and exit
- **Model Access Issues**: Graceful fallback suggestions
- **Rate Limiting**: Automatic delays between requests
- **Quota Exceeded**: Informative error messages
- **Network Issues**: Retry logic and user feedback

## File Structure

```
devduo/
├── devduo.py           # Main system implementation
├── check_models.py     # Model availability checker
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variable template
├── README.md          # This file
└── results/           # Saved collaboration results
```

## Tech Stack

- **Language**: Python 3.7+
- **AI Provider**: OpenAI API (GPT-3.5-turbo, GPT-4)
- **Dependencies**: openai, python-dotenv
- **Architecture**: Multi-agent orchestration
- **Environment**: Cross-platform compatibility

## Future Enhancements

- **Specialized Agents**: Add Tester, Optimizer, and Documentation agents
- **Language Support**: Expand beyond Python to other programming languages
- **Web Interface**: Browser-based collaboration interface
- **Integration**: VS Code extension for seamless development
- **Collaboration Patterns**: Implement different agent interaction modes
- **Performance Metrics**: Add code quality scoring and improvement tracking

## Contributing

This project welcomes contributions! Areas for enhancement:
- Additional agent types and specializations
- Improved code analysis and feedback mechanisms
- Better error handling and user experience
- Performance optimizations and caching
- Documentation and examples

## Troubleshooting

### Common Issues

**"Model does not exist or you do not have access"**
- Your API key doesn't have access to the selected model
- Try gpt-3.5-turbo (available to all accounts)
- Check your OpenAI account status

**"Insufficient quota"**
- You've exceeded your API usage limits
- Add credits to your OpenAI account
- Check your usage on the OpenAI dashboard

**"Rate limit exceeded"**
- Too many API requests in a short time
- Wait a few minutes and try again
- System includes automatic delays to prevent this

### Debug Steps

1. Check your API key: `python check_models.py`
2. Verify internet connection
3. Confirm OpenAI account has sufficient credits
4. Try with gpt-3.5-turbo model first

## License

MIT License - Feel free to use this for your own projects and learning.

## Acknowledgments

- OpenAI for providing the powerful language models
- The AI development community for inspiration and best practices
- Contributors and users who provide feedback and improvements