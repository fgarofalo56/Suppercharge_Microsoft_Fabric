# Contributing Guide

Thank you for your interest in contributing to the Microsoft Fabric Casino/Gaming POC project!

## Code of Conduct

This project follows the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). By participating, you agree to abide by its terms.

## How to Contribute

### Reporting Issues

1. Check existing issues to avoid duplicates
2. Use the issue template
3. Include:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details

### Suggesting Enhancements

1. Open an issue with "Enhancement" label
2. Describe the use case
3. Explain the proposed solution
4. Consider alternatives

### Pull Requests

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes
4. Write/update tests
5. Update documentation
6. Submit PR

## Development Setup

### Prerequisites

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Suppercharge_Microsoft_Fabric.git
cd Suppercharge_Microsoft_Fabric

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\Activate on Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=data-generation --cov-report=html

# Run specific test file
pytest validation/unit_tests/test_generators.py
```

### Code Style

We use:
- **Black** for Python formatting
- **Ruff** for linting
- **MyPy** for type checking

```bash
# Format code
black .

# Lint
ruff check .

# Type check
mypy data-generation/
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Tests
- `chore`: Maintenance

Examples:
```
feat(generators): add compliance data generator
fix(bronze): resolve schema mismatch in slot telemetry
docs(tutorials): update Day 2 agenda
```

## Project Structure

```
Suppercharge_Microsoft_Fabric/
├── infra/                 # Bicep templates
├── docs/                  # Documentation
├── tutorials/             # Step-by-step guides
├── data-generation/       # Python generators
├── notebooks/             # Fabric notebooks
├── validation/            # Tests
└── poc-agenda/            # Workshop materials
```

## Pull Request Process

1. **Branch naming:** `feature/description` or `fix/description`
2. **PR title:** Use conventional commit format
3. **Description:** Explain what and why
4. **Tests:** Add/update tests
5. **Documentation:** Update if needed
6. **Review:** Address feedback

### PR Checklist

- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No secrets or credentials
- [ ] Conventional commit message

## Review Process

1. Automated checks must pass
2. At least one maintainer review required
3. Address all feedback
4. Maintainer merges after approval

## Getting Help

- Open an issue for questions
- Tag maintainers for urgent items
- Check existing documentation

## Recognition

Contributors are recognized in:
- README acknowledgments
- Release notes
- Contributors file

Thank you for contributing!
