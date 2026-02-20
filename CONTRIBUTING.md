# Contributing to Violet DJ Mixer

Thank you for your interest in contributing to Violet DJ Mixer! 
We welcome contributions from the community to help make this software better.

## 🎯 How to Contribute

### Reporting Bugs

Found a bug? Please create an issue on GitHub:

1. [Open New Issue](https://github.com/violet-dj/violet-dj-mixer/issues/new/choose)
2. Select "Bug Report" template
3. Fill in the details:
   - Description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - System info (OS, Python version, etc.)
   - Logs or screenshots if applicable

### Suggesting Features

Have an idea? We'd love to hear it!

1. [Open Discussion](https://github.com/violet-dj/violet-dj-mixer/discussions/new)
2. Select "Ideas" category
3. Describe the feature and why it would be useful

### Contributing Code

**Areas we're looking for help:**

- 🎵 Audio effects implementation
- 🎛️ Additional hardware controller support
- 🌐 Localization/translations
- 📖 Documentation improvements
- 🐛 Bug fixes
- ✨ New features (discuss first!)

**Development Setup:**

```bash
# Fork and clone
git clone https://github.com/your-username/violet-dj-mixer.git
cd violet-dj-mixer

# Create feature branch
git checkout -b feature/your-feature-name

# Install dev dependencies
pip install -r requirements.txt
pip install pytest pytest-cov flake8

# Make your changes and test
python3 -m pytest tests/
python3 -m flake8 src/

# Commit with clear messages
git commit -m "Add feature: description"

# Push and create pull request
git push origin feature/your-feature-name
```

**Code Style:**
- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions
- Write unit tests for new features

### Documentation

Help improve our docs!

- Fix typos or unclear explanations
- Add new tutorial or guide
- Improve code examples
- Translate documentation

```bash
# Edit docs in /docs folder
# Create pull request with changes
```

## 💼 Code of Conduct

This project maintains a Code of Conduct for all contributors:

- Be respectful and inclusive
- No harassment or discrimination
- Focus on constructive feedback
- Help others learn and grow

## 📋 Pull Request Process

1. **Fork** the repository
2. **Create** feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes with clear commits
4. **Test** thoroughly (run tests, manual testing)
5. **Update** documentation if needed
6. **Push** to your fork
7. **Create** pull request with description
8. **Respond** to review feedback
9. **Merge** once approved!

**PR Guidelines:**
- Keep PRs focused and reasonably sized
- Link related issues
- Update CHANGELOG.md
- Add tests for new functionality
- Include before/after screenshots if UI change

## 🔍 Review Process

- At least one maintainer review
- GitHub Actions tests must pass
- Code quality checks (flake8, type hints)
- Documentation review if applicable
- Once approved, squash and merge

## 📚 Project Structure

```
violet-dj-mixer/
├── src/
│   ├── ui/              # UI components
│   ├── audio/           # Audio processing
│   ├── devices/         # Device detection
│   ├── controllers/     # MIDI controller support
│   └── effects/         # Audio effects
├── docs/                # Documentation
├── tests/               # Test suite
├── scripts/             # Build/install scripts
└── packaging/           # DEB package files
```

## 🚀 Release Process

Releases are made by maintainers:

1. Update version in `__init__.py`
2. Update CHANGELOG.md
3. Create git tag (v1.x.x format)
4. Push tag to trigger release workflow
5. GitHub Actions builds and uploads .deb
6. GitHub Pages updated automatically

## 💬 Community

- **[Discussions](https://github.com/violet-dj/violet-dj-mixer/discussions)** - Ideas and questions
- **[Discord](https://discord.gg/violet-dj)** - Real-time chat
- **[Issues](https://github.com/violet-dj/violet-dj-mixer/issues)** - Bug reports

## 📝 License

By contributing, you agree your contributions are licensed under GPL-3.0.

---

Thank you for contributing to make Violet DJ Mixer better! 🎵
