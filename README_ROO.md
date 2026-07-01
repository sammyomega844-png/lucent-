Roo integration notes

- Add `ROO_API_KEY` to your `.env` to enable Roo.
- Set `AI_PROVIDER=roo` to use Roo instead of Groq.
- Install the Roo SDK in your virtualenv (example):

```bash
pip install roo
```

If Roo uses a different package name or client API, share the SDK snippet and I'll adapt `get_ai_response()` accordingly.
