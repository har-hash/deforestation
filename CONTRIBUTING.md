# Contributing to Illegal Deforestation Tracker

Thank you for your interest in contributing to the Illegal Deforestation Tracker! This document provides guidelines and instructions for contributing.

## 🤝 Ways to Contribute

- Report bugs
- Suggest new features
- Improve documentation
- Submit pull requests
- Review code
- Share the project

## 🐛 Reporting Bugs

### Before Submitting a Bug Report

- Check existing issues to avoid duplicates
- Ensure you're using the latest version
- Test with a clean installation if possible

### How to Submit a Bug Report

Create an issue with:

1. **Clear title**: Brief description of the problem
2. **Description**: Detailed explanation
3. **Steps to reproduce**:
   ```
   1. Go to '...'
   2. Click on '...'
   3. See error
   ```
4. **Expected behavior**: What should happen
5. **Actual behavior**: What actually happens
6. **Screenshots**: If applicable
7. **Environment**:
   - OS: [e.g., Windows 10, macOS 12, Ubuntu 22.04]
   - Python version: [e.g., 3.9.1]
   - Node version: [e.g., 18.0.0]
   - Browser: [e.g., Chrome 120]

## 💡 Suggesting Features

Feature requests are welcome! Please provide:

1. **Use case**: Why is this feature needed?
2. **Description**: What should it do?
3. **Alternatives**: Have you considered other solutions?
4. **Additional context**: Screenshots, mockups, etc.

## 🔧 Development Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- Git
- Google Cloud account
- Earth Engine account

### Setup Steps

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/deforestation-tracker.git
   cd deforestation-tracker
   ```

2. **Set up backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Set up frontend**
   ```bash
   cd frontend
   npm install
   cp .env.local.example .env.local
   # Edit .env.local with your API keys
   ```

4. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 Coding Standards

### Python (Backend)

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and small
- Use meaningful variable names

Example:
```python
def calculate_forest_loss_area(
    geometry: ee.Geometry,
    threshold: float = 0.7
) -> float:
    """
    Calculate total forest loss area within a geometry.
    
    Args:
        geometry: Earth Engine geometry to analyze
        threshold: Confidence threshold for detection
        
    Returns:
        Area in hectares
    """
    # Implementation
    pass
```

### TypeScript/JavaScript (Frontend)

- Use TypeScript for new components
- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use functional components with hooks
- Keep components small and focused
- Use meaningful prop and variable names

Example:
```typescript
interface AlertCardProps {
  severity: 'low' | 'medium' | 'high' | 'critical'
  area: number
  confidence: number
}

export function AlertCard({ severity, area, confidence }: AlertCardProps) {
  // Implementation
}
```

### Code Formatting

**Python:**
```bash
# Install black
pip install black

# Format code
black .
```

**TypeScript/JavaScript:**
```bash
# Format code
npm run lint --fix
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Before Submitting

- [ ] All tests pass
- [ ] Code is formatted
- [ ] No linting errors
- [ ] Documentation updated
- [ ] Changelog updated (if applicable)

## 📤 Submitting Pull Requests

### PR Checklist

- [ ] Branch is up to date with main
- [ ] Tests pass
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] PR description explains changes

### PR Process

1. **Create PR**
   - Use a clear title
   - Describe what changed and why
   - Reference related issues (e.g., "Fixes #123")

2. **Review process**
   - Maintainers will review your PR
   - Address feedback promptly
   - Keep discussions focused and constructive

3. **Merge**
   - PRs are merged by maintainers
   - Your contribution will be credited

### Commit Message Guidelines

Use conventional commits:

```
feat: add timeline visualization component
fix: resolve map rendering issue on mobile
docs: update setup guide with troubleshooting
style: format code with black
test: add tests for DSA algorithms
refactor: simplify BigQuery query logic
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

## 🎨 Design Guidelines

### UI/UX Principles

- **Clarity**: Information should be easy to understand
- **Consistency**: Use established patterns
- **Feedback**: Provide clear feedback for actions
- **Accessibility**: Support keyboard navigation, screen readers
- **Performance**: Optimize for fast loading

### Color Scheme

- Red tones: Critical alerts, deforestation
- Blue tones: Information, actions
- Green tones: Forest, success
- Gray tones: Background, secondary info

## 📚 Documentation

### What to Document

- New features
- API changes
- Configuration options
- Breaking changes
- Migration guides

### Documentation Style

- Clear and concise
- Include examples
- Use proper formatting
- Add screenshots for UI changes

## 🏗️ Project Structure

```
deforestation-tracker/
├── backend/           # Python/FastAPI backend
│   ├── routes/       # API endpoints
│   ├── models/       # Data models
│   └── ...
├── frontend/         # Next.js frontend
│   ├── components/   # React components
│   ├── pages/        # Next.js pages
│   └── ...
└── docs/            # Documentation
```

## 🔍 Code Review

### What Reviewers Look For

- Code quality and style
- Test coverage
- Documentation
- Performance implications
- Security concerns
- Breaking changes

### Being a Good Reviewer

- Be constructive and respectful
- Explain reasoning
- Suggest improvements
- Approve good work promptly

## 📞 Communication

### Channels

- **Issues**: Bug reports, feature requests
- **Pull Requests**: Code changes
- **Discussions**: General questions, ideas

### Be Respectful

- Assume good intentions
- Be patient with newcomers
- Focus on the code, not the person
- Celebrate contributions

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in the project

## ❓ Questions?

- Check existing documentation
- Search closed issues
- Ask in discussions
- Reach out to maintainers

---

**Thank you for contributing to forest conservation! 🌲**



