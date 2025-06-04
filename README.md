# shunting-yard

- parse input strings (e.g. `"3 + abs(-4)"`)
- use the shunting yard algorithm to emit equivalent RPN tokens
- stretch goals: implement an `eval_rpn` calculator that uses these tokens

## Setup / Testing

This uses the `uv`, `ruff`, and `ty` tools from Astral.sh.
I am using python 3.13.0, but I forget whether anything needs that specifically (vs 3.11 or lower).

### uv, ruff tooling
```sh
uv tool install ruff
uv tool install ty
uv pip install pytest ipython

# autoformat:
ruff format .

# type check:
ty check .
```

### Running tests

```sh
pytest .
pytest tests/test_tokenizer.py
```


