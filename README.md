# The Reading Room

The Reading Room is a personal dashboard for reading and comparing academic papers. Upload a PDF and it turns the paper into practical reading notes: its core idea, easy-to-read summary, evidence, gaps, key figures, what it achieved, and what is still left open.

It also includes a **Reference Desk** where you can ask questions across every paper on your shelf.

## Features

- Upload one or more research-paper PDFs.
- Extract PDF text in the browser with PDF.js.
- Analyze each paper through Mistral and save a structured breakdown.
- Read summaries written in plain, everyday language.
- Browse papers through a card catalog and spine-style sidebar.
- Compare evidence, author-identified gaps, inferred gaps, figures, completed work, and open work.
- Use reading-footprint visuals to see the balance of notes in each paper and across the collection.
- Ask collection-wide questions at the Reference Desk.
- Persist papers and notes in the browser’s local storage between sessions.

## Requirements

- Python 3.9 or later
- A Mistral API key
- A modern browser with internet access (needed for PDF.js and Google Fonts)

## Setup

1. Open [`.env`](.env) in this folder.
2. Paste your Mistral key after `MISTRAL_API_KEY=`:

   ```env
   MISTRAL_API_KEY=your_mistral_api_key_here
   ```

3. Start the local server:

   ```powershell
   cd C:\Users\zohai\Documents\Codex\2026-08-02\build\outputs
   python app.py
   ```

4. Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

The API key is read only by `app.py`; it is not stored by the browser or included in model requests from the page.

## Configuration

The `.env` file has the following settings:

```env
MISTRAL_API_KEY=
MISTRAL_ENDPOINT=https://api.mistral.ai/v1/chat/completions
MISTRAL_MODEL=mistral-small-latest
```

- `MISTRAL_API_KEY` is required.
- `MISTRAL_ENDPOINT` only needs changing if you use a compatible proxy or endpoint.
- `MISTRAL_MODEL` selects the Mistral model used for paper analysis and Reference Desk answers.

The Settings button in the app can temporarily override the model or endpoint for that browser. Credentials always remain in `.env`.

## How to use it

1. Select **Add papers** in the sidebar.
2. Choose one or more PDFs with selectable text.
3. Wait for the small status message to move from text extraction to Mistral analysis.
4. Open a paper from the shelf or card catalog to read its notes.
5. Return to **Catalog & Query** and ask a question at the Reference Desk. Answers rely only on the summaries and notes already in your collection.

## Notes on data storage

- Paper notes, catalog entries, and the Q&A thread are stored in your browser’s local storage.
- The original PDF is not saved by the app after text extraction.
- Clearing the browser’s site data for `127.0.0.1` removes the saved catalog and notes.
- The Mistral key stays in the local `.env` file. Do not share or commit that file.

## Troubleshooting

### “MISTRAL_API_KEY is not set”

Make sure the `.env` file sits beside `app.py`, paste the key after `MISTRAL_API_KEY=`, save the file, and retry. The server rereads `.env` on each request.

### The browser cannot reach the app

Confirm the terminal running `python app.py` is still open, then use `http://127.0.0.1:8000` rather than opening `index.html` directly.

### A PDF reports that it has no usable text layer

The file is likely a scanned or image-only PDF. Use an OCR-enabled copy of the paper first, then upload that version.

### The model returns an analysis error

Check that the API key is valid, the selected Mistral model is available to your account, and the paper is not unusually large. The app limits the text it sends to keep requests manageable.

## Project files

- `index.html` — dashboard interface, PDF extraction, local catalog, and visuals
- `app.py` — local Python server and secure Mistral request proxy
- `.env` — local Mistral configuration and API key
