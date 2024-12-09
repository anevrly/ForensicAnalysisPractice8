# Running the solutions

```
uvicorn app_safe:app --reload
```

**OR**

```
uvicorn app_unsafe:app --reload
```

**AND**

```
uvicorn app_password_cracking:app --reload --port 8080
```

## Default config

- **Main server** (safe / unsafe): `http://127.0.0.1:8000`
- **Brute-force server**: `http://127.0.0.1:8080`
