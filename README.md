# TripBanau AI

TrioBanau AI is a multi-agent travel planner built with FastAPI and LangGraph. It combines flight search, hotel research, itinerary generation, and an AI-written final travel plan in one web interface.

## Features

- Natural-language trip planning through a browser UI
- Flight lookup with AviationStack
- Hotel and destination research with Tavily
- Budget-aware, day-by-day itinerary generation with Groq
- PostgreSQL-backed LangGraph conversation checkpoints
- Copy and PDF download actions for generated plans
- REST health check and travel-planning endpoints

## Architecture

The LangGraph workflow runs these agents sequentially:

1. `flight_agent` resolves locations to IATA airport codes and searches flights.
2. `hotel_agent` searches for hotel information and destination results.
3. `itinerary_agent` creates a practical itinerary from the collected results.
4. `final_agent` formats the complete response for the user.

The FastAPI application serves the frontend from `templates/index.html` and `static/`, and exposes the workflow through `/api/travel`.

## Requirements

- Python 3.12 or newer
- A PostgreSQL database with a reachable external connection URL
- API keys for Groq and Tavily
- An AviationStack API key for live flight lookups

## Setup

Clone the repository and create a virtual environment:

```bash
python3 -m venv travel
source travel/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
DATABASE_URL=postgresql://user:password@host:5432/database

# Optional: defaults to DAC (Dhaka) when no origin is provided.
DEFAULT_ORIGIN_IATA=DAC
```

Do not commit `.env` files or database connection strings containing credentials. If a database URL has previously been exposed, rotate its password before using it again.

## Run locally

```bash
python app.py
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in a browser.

The application also provides interactive API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## API

### `GET /health`

Returns the service status.

### `POST /api/travel`

Request body:

```json
{
  "message": "Plan a 7 day Japan trip from Bangladesh with flights, hotels, and sightseeing.",
  "thread_id": null
}
```

`thread_id` is optional. Reusing the returned thread ID allows the application to continue a saved conversation.

Successful responses include:

- `answer`: the formatted travel plan
- `flight_results`: flight search output
- `hotel_results`: hotel research output
- `itinerary`: generated itinerary
- `thread_id`: saved conversation identifier
- `llm_calls`: number of model calls used

## Project structure

```text
.
├── app.py                 # FastAPI application and HTTP routes
├── backend.py             # LangGraph workflow and PostgreSQL checkpointer
├── tools/
│   ├── flight_tool.py     # Airport resolution and AviationStack search
│   └── tavily_tool.py     # Tavily hotel and destination search
├── templates/index.html   # Web interface
├── static/                # Frontend JavaScript and CSS
├── requirements.txt       # Python dependencies
└── Dockerfile             # Container configuration
```
