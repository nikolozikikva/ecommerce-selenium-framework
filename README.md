# ecommerce-selenium-framework

Automated end-to-end testing framework for the SauceDemo e-commerce web application (https://www.saucedemo.com) built using Python, Selenium WebDriver, and Pytest with the Page Object Model (POM) architectural pattern.

## Architecture

The framework enforces strict separation between test logic, page element definitions, test configurations, and test runners.

```
ecommerce-selenium-framework/
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_authentication.py
│   ├── test_cart_and_sorting.py
│   └── test_checkout_e2e.py
├── utils/
│   ├── __init__.py
│   └── config.py
├── screenshots/
├── reports/
├── .github/
│   └── workflows/
│       └── e2e-tests.yml
├── pytest.ini
├── requirements.txt
└── README.md
```

### Architectural Principles

1. Page Object Model (POM):
   - Every application view is represented by a dedicated class inheriting from `BasePage`.
   - Locators and UI interaction logic reside exclusively within page classes, preventing locator leakage into test assertions.
2. Explicit Synchronization:
   - Arbitrary sleep statements (`time.sleep`) are strictly prohibited across the entire project.
   - All state transitions and DOM lookups use `WebDriverWait` with expected conditions (`visibility_of_element_located`, `element_to_be_clickable`, etc.).
   - Explicit timeout defaults to 15 seconds, handling both standard response times and simulated network/rendering delays (e.g., `performance_glitch_user`).
3. Failure Capture and Diagnostic Reporting:
   - `conftest.py` implements a `pytest_runtest_makereport` hook.
   - Upon any test failure, the hook automatically dumps a timestamped PNG screenshot into `screenshots/` and embeds the image in the self-contained HTML report.
4. Defect Tracking via Pytest Markers:
   - Known upstream application defects (such as duplicate broken thumbnails on `problem_user`) are explicitly decorated with `@pytest.mark.xfail(strict=True)`.

## Prerequisites

- Python 3.10 or higher
- Google Chrome browser installed
- Pip package manager

Selenium 4 includes Selenium Manager, which resolves and manages compatible ChromeDriver binaries automatically.

## Installation

1. Clone or navigate to the project directory:
   ```bash
   cd ecommerce-selenium-framework
   ```

2. Create and activate a Python virtual environment:
   - On Linux/macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - On Windows (PowerShell):
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Test Execution

### Run Full Test Suite

Execute `pytest` from the root of `ecommerce-selenium-framework`:

```bash
pytest
```

Or run with verbose console output:

```bash
pytest -v
```

### Run Specific Test Modules

- Authentication suite:
  ```bash
  pytest tests/test_authentication.py -v
  ```

- Cart and catalog sorting suite:
  ```bash
  pytest tests/test_cart_and_sorting.py -v
  ```

- End-to-end checkout suite:
  ```bash
  pytest tests/test_checkout_e2e.py -v
  ```

### Run Specific Test Methods

```bash
pytest tests/test_checkout_e2e.py::TestCheckoutE2E::test_complete_e2e_purchase_flow -v
```

## HTML Test Report

Running `pytest` automatically triggers the `pytest-html` plugin configured via `pytest.ini`:

- Output path: `reports/test_report.html`
- Mode: `--self-contained-html` (all styles, scripts, and failure screenshots are bundled directly within the single HTML file)

### Viewing the Report

Open the generated report in any browser:

- On Windows:
  ```powershell
  Start-Process reports/test_report.html
  ```
- On macOS:
  ```bash
  open reports/test_report.html
  ```
- On Linux:
  ```bash
  xdg-open reports/test_report.html
  ```

The report provides test execution status, elapsed times, stdout/stderr logs, and embedded screenshot artifacts for any test failures.

## Continuous Integration (CI/CD)

The repository includes a GitHub Actions workflow located at `.github/workflows/e2e-tests.yml`.

- Trigger: Pushes and pull requests targeting the `main` branch.
- Execution environment: `ubuntu-latest` with headless Chrome.
- Artifact publishing: The `reports/` directory and `screenshots/` directory are archived and made available as downloadable workflow artifacts for each run.
