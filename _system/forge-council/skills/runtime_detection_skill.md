# Skill: Runtime detection

## Steps

1. Identify primary language and package manager files.  
2. Extract test runner (`pytest`, `npm test`, `go test`, …).  
3. Extract lint/typecheck if declared.  
4. Record **unknown** explicitly — do not invent commands.

## Output

- Section in `REPO_PROFILE.md` under **Detected stack**.
