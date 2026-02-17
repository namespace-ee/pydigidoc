# pydigidoc TODO

Items identified during cross-project review (Feb 2026).

## pyproject.toml

- [x] ~~Remove `wheel.exclude = ["pydigidoc/lib/**", "pydigidoc/include/**"]`~~ — removed, build never produces these directories since upstream install() rules are suppressed
- [x] ~~Add `Changelog` to `[project.urls]`~~ — added, points to GitHub releases

## CI (.github/workflows/build.yml)

- [x] ~~`actions/upload-artifact` uses `@v6` but `download-artifact` uses `@v7`~~ — upgraded upload-artifact to v7
- [ ] Consider whether OpenSSL 3.0.x LTS (EOL Sep 2026) should be upgraded to OpenSSL 3.5.x LTS in the manylinux wheel build — 3.0 is in security-only mode, 3.5 is the new LTS
- [x] ~~`source /opt/rh/gcc-toolset-13/enable` placement~~ — moved before all builds so GCC 13 is explicitly active for both OpenSSL and xmlsec1
- [ ] `build_wheels` job runs on PRs too — intentional for testing but expensive; consider adding a label-gated trigger or making it manual for PRs

## SWIG interface

- [x] ~~`%rename` rules don't exclude constructors/destructors~~ — added `%$not %$isconstructor, %$not %$isdestructor` to match pycdoc

## Documentation

- [x] ~~`README.md` shows `pip install .`~~ — updated to `uv build --wheel && pip install dist/*.whl`
- [ ] `RELINKING.md` uses `pip install build` / `python -m build --wheel` — keeping pip-based instructions since relinking users may not have uv

## Tests

- [x] ~~Integration tests use manual `try/finally`~~ — added pytest `lib` fixture in conftest.py
- [x] ~~No tests for `initialize_lib()`~~ — added `test_initialize_lib_custom_path`
- [x] ~~No tests for `app_info()` or `user_agent()`~~ — added `test_app_info` and `test_user_agent`
- [ ] `test_container_open_cb_subclass` doesn't assert `cb.called` — `validate_online()` is not called for unsigned containers (no signatures to validate), so the assertion would be unreliable without a signed test fixture

## Python __init__.py

- [x] ~~`user_agent` parameter shadows imported function~~ — renamed to `user_agent_str`

## Upstream tracking

- [ ] libdigidocpp is on v4.3.0 (latest as of Feb 2026) — no action needed now, but set up a process to check for new releases periodically
