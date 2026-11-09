# DevFlow

A lightweight Python command-line tool for checking repository maintenance basics.

> Early-stage project. DevFlow checks for common files and practices; it is not a security scanner or code-quality certification tool.

## Checks
- README, license, and contribution guidance
- Test directory and GitHub Actions workflow
- `.gitignore` and Python packaging metadata

## Install
```bash
git clone https://github.com/masumkhon98-web/devflow.git
cd devflow
python -m pip install -e ".[dev]"
```

## Use
```bash
devflow .
devflow . --format json
devflow . --format markdown --output report.md
```

Exit codes: `0` no failed checks, `1` one or more failed checks, `2` invalid path or output error.

## Development
```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```

## Roadmap
- [x] Initial repository checks
- [x] Text, JSON, and Markdown reports
- [ ] Configurable profiles
- [ ] More language ecosystems
- [ ] Community plugin interface

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md).

## License
MIT. See [LICENSE](LICENSE).
