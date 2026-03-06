# Contributing to Red WiFi

Thank you for your interest in contributing to Red WiFi! We welcome contributions from everyone.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) in all interactions.

## How to Contribute

### Reporting Bugs

Before creating bug reports, check the [issue tracker](https://github.com/redwifi/red-wifi/issues) as you might find the issue already reported.

When reporting a bug, include:
- Clear description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When suggesting an enhancement:
- Use a clear, descriptive title
- Provide a step-by-step description of the enhancement
- Provide examples
- Describe the current behavior and expected behavior

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write or update tests
5. Follow PEP 8 style guidelines (use `black` for formatting)
6. Commit with clear messages (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Code Guidelines

- Follow PEP 8 style guide
- Use type hints where applicable
- Write docstrings for all modules, classes, and functions
- Include unit tests for new features
- Run `flake8` for linting: `flake8 red_wifi/`
- Format code with `black`: `black red_wifi/`

## Testing

Run tests before submitting:
```bash
python -m pytest tests/
```

## Documentation

- Update README.md if adding new features
- Update docs/ files if changing user-facing functionality
- Use clear, technical language
- Include examples

## Questions?

Open an issue or contact the maintainers.

## License

By contributing, you agree that your contributions will be licensed under its MIT License.
