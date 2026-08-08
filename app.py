from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import os
import urllib.error
import urllib.request


ROOT = Path(__file__).parent
DEFAULT_ENDPOINT = "https://api.mistral.ai/v1/chat/completions"
DEFAULT_MODEL = "mistral-large-latest"


def load_env_file():
    """Load simple KEY=value pairs from .env without a third-party package."""
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        # Refresh values on every request, so editing .env takes effect immediately.
        os.environ[key.strip()] = value.strip().strip('"').strip("'")


load_env_file()


class ReadingRoomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_POST(self):
        if self.path != "/api/chat":
            self.send_error(404, "Not found")
            return
        try:
            load_env_file()
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            messages = body.get("messages")
            if not isinstance(messages, list) or not messages:
                raise ValueError("A non-empty messages list is required.")

            api_key = os.environ.get("MISTRAL_API_KEY")
            if not api_key:
                self.respond(400, {"error": "MISTRAL_API_KEY is not set. Paste it into the .env file, then restart app.py."})
                return

            # Allow non-secret model / endpoint selection, while keeping the key server-side.
            endpoint = body.get("endpoint") or os.environ.get("MISTRAL_ENDPOINT") or DEFAULT_ENDPOINT
            model = body.get("model") or os.environ.get("MISTRAL_MODEL") or DEFAULT_MODEL
            payload = json.dumps({
                "model": model,
                "messages": messages,
                "temperature": 0.25,
                "response_format": {"type": "json_object"} if body.get("json_mode") else None,
            }).encode("utf-8")
            decoded = json.loads(payload)
            if decoded["response_format"] is None:
                del decoded["response_format"]
            request = urllib.request.Request(
                endpoint,
                data=json.dumps(decoded).encode("utf-8"),
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
                method="POST",
            )
            with urllib.request.urlopen(request, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))
            content = result.get("choices", [{}])[0].get("message", {}).get("content")
            if not content:
                raise RuntimeError("The model response did not include any message content.")
            self.respond(200, {"content": content})
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            self.respond(exc.code, {"error": f"Model API error: {detail}"})
        except (ValueError, KeyError, RuntimeError) as exc:
            self.respond(400, {"error": str(exc)})
        except Exception as exc:
            self.respond(500, {"error": f"Server error: {exc}"})

    def respond(self, status, payload):
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


if __name__ == "__main__":
    print("The Reading Room is available at http://127.0.0.1:8000")
    print("Paste MISTRAL_API_KEY into .env before running to enable analysis and Q&A.")
    ThreadingHTTPServer(("127.0.0.1", 8000), ReadingRoomHandler).serve_forever()
