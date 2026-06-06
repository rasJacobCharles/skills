# Fixture Example: Mock Hashing Input

This file illustrates how to define mock data to test suggestions against before presenting them to the Coordinator.

```json
{
  "test_fixture": {
    "username": "admin",
    "password": "superSecretPassword123"
  },
  "assertions": [
    {
      "method": "login",
      "args": ["admin", "superSecretPassword123"],
      "expected_return": true
    }
  ]
}
```
