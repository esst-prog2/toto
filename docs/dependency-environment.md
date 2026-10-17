# Dependency rationale and tested environment

Recorded for Homework 6 Review 4 on 2026-10-17. Dependency floors describe documented API/runtime prerequisites; they are not a claim that every permitted version combination was tested.

## Declared minimum versions

| Dependency | Constraint | Rationale |
| --- | --- | --- |
| NumPy | `numpy>=2.1.0` | The generator uses `Generator`, `PCG64`, and Poisson sampling. The 2.1 series provides an upstream Python 3.10–3.13 baseline, including the declared 3.11 floor and the 3.13 development interpreter. This avoids choosing a NumPy 1.26 floor whose upstream support stops at 3.12. [NumPy 2.1 release notes](https://numpy.org/doc/2.1/release/2.1.0-notes.html). |
| pandas | `pandas>=2.2.3` | First generally Python-3.13-compatible release; its release notes also record NumPy 2.1 compatibility fixes. This is a runtime compatibility baseline, not a claim that older pandas lacks every API used here. [pandas 2.2.3 notes](https://pandas.pydata.org/docs/whatsnew/v2.2.3.html). |
| Streamlit | `streamlit>=1.49.0` | Versioned documentation confirms `width="stretch"` for both buttons and dataframes, which the app uses. It also includes the AppTest API used by tests. [Button API](https://docs.streamlit.io/1.49.0/develop/api-reference/widgets/st.button), [Dataframe API](https://docs.streamlit.io/1.49.0/develop/api-reference/data/st.dataframe). |
| pytest (development) | `pytest>=8.3.3` | A conservative patch baseline in the 8.3 series after upstream Python 3.13 support was added, with built-in `pythonpath` configuration and the fixtures/parametrization used here. This is not asserted to be the earliest possible pytest version. [pytest changelog](https://docs.pytest.org/en/stable/changelog.html). |
| Jinja2 | `Jinja2>=3.1.5` | The application uses `DataFrame.style`. The installed pandas 3.0.6 optional-dependency checker (`pandas.compat._optional.VERSIONS["jinja2"]`) requires 3.1.5. Installed pandas metadata also lists `jinja2>=3.1.5` under output-formatting. Declaring just Jinja2 avoids adding unrelated pandas extras. |

No upper version bounds were added. `requires-python = ">=3.11"` and the existing `setuptools>=68` isolated build requirement remain unchanged. No new dependency-management tool was introduced.

## Exact tested environment

- CPython **3.13.12**, standard GIL build, Clang 16.0.0.
- macOS **26.6.2**, **arm64**.
- NumPy **2.5.3** (`Requires-Python >=3.12`).
- pandas **3.0.6** (`Requires-Python >=3.11`).
- Streamlit **1.64.0** (`Requires-Python >=3.10`).
- pytest **9.1.1** (`Requires-Python >=3.10`).
- Jinja2 **3.1.6** (`Requires-Python >=3.7`).
- pip **25.3**; local project version **0.1.0** from this checkout.

[constraints-tested-py313.txt](../constraints-tested-py313.txt) records every installed third-party/tool distribution at its exact version, excluding the local project. It can constrain an installation of this checkout without another package manager:

```bash
python -m pip install -c constraints-tested-py313.txt '.[dev]'
```

Use a comparable Python 3.13/macOS arm64 environment. The snapshot is an installed-environment record, not a portable, hash-locked dependency solution. It does not fix Python itself, isolated build dependencies, additional platform-specific dependencies, or future dependencies absent from the recorded environment. The constrained fresh installation was not performed during this review; verification uses the existing recorded environment. Build isolation supplies setuptools separately; setuptools is not installed in the current runtime environment, and no exact isolated-backend version was captured.

## Compatibility limits

No Python 3.11 interpreter is available locally. The minimum releases' upstream metadata/runtime support permit Python 3.11: NumPy 2.1 supports Python 3.10–3.13; pandas 2.2.3 requires >=3.9; Streamlit 1.49.0 requires >=3.9 excluding 3.9.7; pytest 8.3.3 requires >=3.8. See the [pandas](https://pypi.org/project/pandas/2.2.3/), [Streamlit](https://pypi.org/project/streamlit/1.49.0/), and [pytest](https://pypi.org/project/pytest/8.3.3/) release metadata. This establishes metadata plausibility, not a tested project environment or a complete transitive resolution on 3.11.

The project suite was not run on Python 3.11, on the exact minimum dependency combination, or across all future Python/dependency releases. In particular, do not apply the Python 3.13 snapshot on Python 3.11: its NumPy 2.5.3 pin requires >=3.12. An unconstrained install on 3.11 must resolve different compatible versions and still needs project-level verification, including byte-identical dataset regeneration. The ordinary README installation command intentionally remains available without the environment snapshot.

## Test invocation

Pytest alone adds both `src` and the repository root to its import paths through `pyproject.toml`; this does not change application imports. From the repository root, both activated-environment commands are supported:

```bash
python -m pytest
.venv/bin/pytest
```
