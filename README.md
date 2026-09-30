# JSON Toolkit

[绠€浣撲腑鏂嘳(README.zh-CN.md)

One command-line tool for formatting, minifying, validating, sorting, querying, and comparing JSON files.

## Features

- Pretty-format or minify JSON.
- Validate one or many files.
- Recursively sort object keys.
- Query values using paths such as `items[0].name`.
- Produce structured path-based differences.
- Python standard library only.

## Install

```bash
git clone https://github.com/jellywong343-sys/json-toolkit.git
cd json-toolkit
python -m pip install -e .
```

## Usage

```bash
json-toolkit validate examples/sample.json
json-toolkit format examples/sample.json
json-toolkit minify examples/sample.json -o compact.json
json-toolkit sort examples/sample.json -o sorted.json
json-toolkit query examples/sample.json tags[0]
json-toolkit diff examples/sample.json examples/sample-updated.json
```

The `diff` command exits with status 1 when differences are found, which is useful in automated checks.

## Tests

```bash
python -m unittest discover -s tests -v
```

## License

MIT




