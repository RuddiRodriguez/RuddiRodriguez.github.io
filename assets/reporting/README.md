# Python reporting examples

These small functions adapt historical reporting workflows with generic names,
status values and paths. No private records or credentials are included.

Install pandas and numpy, place both Python files together, and run:

```sh
python generate_example.py
```

This creates example_response_summary.csv from invented records. The example
shows duplicate activity consolidation and a response window.

Database functions need SQLAlchemy and the caller's database connection.
API functions need a compatible SOAP client and supplied authentication.
Excel output needs xlwings, desktop Excel and a template with a Data sheet.
Those external functions are examples; the local demonstration does not call them.
