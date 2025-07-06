# DevDuo

A simple 2-agent AI coding system where two AI agents collaborate to write and improve code.

## What is DevDuo?

DevDuo is a learning project that demonstrates multi-agent AI collaboration for coding tasks. It uses two specialized agents:

- **Writer Agent**: Takes a coding task and writes the initial implementation
- **Reviewer Agent**: Reviews the code and suggests improvements

The agents iterate together to refine the solution, simulating how human developers collaborate.

## Why DevDuo?

This project was built to:
- Learn multi-agent AI system design
- Understand how AI agents can collaborate
- Practice agent orchestration concepts
- Build a foundation for more complex AI coding systems

## How It Works

1. **User provides a coding task** (e.g., "Write a function to calculate fibonacci numbers")
2. **Writer Agent** creates the initial code
3. **Reviewer Agent** analyzes the code and suggests improvements
4. **Agents iterate** 2-3 times to refine the solution
5. **Final code** is presented to the user

## Current Status

🚧 **In Development** - This is a learning project and work in progress.

### Phase 1: Mock Implementation ✅
- Basic agent architecture
- Simulated agent responses
- Agent communication flow

### Phase 2: AI Integration (Planned)
- OpenAI API integration
- Real agent responses
- Iterative improvement cycles

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/devduo.git
cd devduo

# Install dependencies
pip install -r requirements.txt

# Run the mock version
python devduo.py
```

## Usage

```python
from devduo import DevDuo

# Initialize the system
duo = DevDuo()

# Give the agents a task
result = duo.collaborate("Write a function to reverse a string")

# See the final code
print(result.final_code)
```

## Example Output

```
Task: Write a function to reverse a string

Writer Agent: Here's my initial implementation...
Reviewer Agent: Good start! I suggest these improvements...
Writer Agent: Thanks for the feedback, here's the updated version...
Reviewer Agent: Much better! This looks solid.

Final Code:
def reverse_string(s):
    """Reverse a string efficiently."""
    return s[::-1]
```

## Tech Stack

- **Language**: Python
- **AI Provider**: OpenAI API (when implemented)
- **Architecture**: Simple agent orchestration
- **Environment**: GitHub Codespaces

## Learning Goals

- Multi-agent system design
- AI API integration
- Agent communication patterns
- Code review automation
- Iterative improvement processes

## Future Ideas

- Add more specialized agents (Tester, Optimizer, etc.)
- Implement different collaboration patterns
- Add support for multiple programming languages
- Create a web interface

## Contributing

This is a learning project, but feedback and suggestions are welcome!

## License

MIT License - Feel free to use this for your own learning projects.