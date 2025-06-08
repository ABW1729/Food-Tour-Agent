
#  Food Tour Planning Agent

A smart AI agent that crafts detailed one-day foodie itineraries for cities based on:
- Current weather conditions (suggesting indoor/outdoor venues)
- Top iconic local dishes
- Highly-rated restaurants serving those dishes

##  Project Structure

```
.
├── agent.py                  # Main execution script
├── .env                      # Environment variables file
├── requirements.txt          # Python dependencies
└── README.md
```

---

##  How to Run This Project

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ABW1729/Food-Tour-Agent.git
   cd Food-Tour-Agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create `.env` file** in the root directory:
   ```env
   JULEP_API_KEY=your_julep_api_key_here
   OPENWEATHERMAP_API_KEY=your_openweathermap_key_here
   BRAVE_API_KEY=your_brave_search_key_here
   JULEP_LOG=info
   ```

4. **Run the script**:
   ```bash
   python agent.py
   ```

---

## ⚙️ Configurable Parameters

These are stored as environment variables in your `.env` file:

| Variable Name           | Description                         |
|------------------------|-------------------------------------|
| `JULEP_API_KEY`        | API key for Julep agent execution    |
| `OPENWEATHERMAP_API_KEY` | API key for current weather data     |
| `BRAVE_API_KEY`        | API key for internet search queries  |
| `JULEP_LOG`            | Logging level (set to `info` or `debug`) |



---

##   Logging

Enable logging by setting the `JULEP_LOG` environment variable in `.env`:

```env
JULEP_LOG=info    # or debug for more verbose output
```

Python logging is configured via:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

##  Execution Output Sample

The script prints the following during execution:
- Current execution status (e.g. running, succeeded)
- Intermediate outputs from tools (weather, searches)
- Final food tour plan

```bash
Started an execution. Execution ID: 1234-5678-9012
Execution status: running
...
Execution status: succeeded
--- FINAL PLAN ---
Mumbai:
Breakfast at...
```


---

##  Output Example

```
Dadar Food Tour Plan:
Breakfast: Misal Pav at Hotel Aaswad
Lunch: Thali at Gomantak
Dinner: Pav Bhaji at Sukh Sagar
```

---

