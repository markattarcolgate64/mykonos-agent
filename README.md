# Software Engineer Automation Tracker

A tool to track and analyze software engineer automation activities.

## Features

- Track automation tool usage
- Monitor time spent on automation tasks
- Generate analytics and reports
- Visualize automation trends over time
- Support for multiple engineers

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn automation_tracker:app --reload
```

## API Endpoints

### Record Automation
```
POST /record/automation
```
Required parameters:
- engineer_id: str
- tool_name: str
- start_time: datetime
- end_time: datetime
- description: str (optional)

### Analytics Endpoints

```
GET /analytics/total-time
```
- Get total time spent on automation

```
GET /analytics/tools-usage
```
- Get usage statistics per tool

```
GET /analytics/usage-by-date
```
- Get automation usage by date

```
GET /analytics/generate-report
```
- Generate a comprehensive report with visualizations

## Example Usage

```python
import requests
from datetime import datetime

# Record automation
response = requests.post(
    "http://localhost:8000/record/automation",
    json={
        "engineer_id": "john_doe",
        "tool_name": "pytest",
        "start_time": "2025-05-21T15:00:00",
        "end_time": "2025-05-21T16:00:00",
        "description": "Automated testing of API endpoints"
    }
)

# Get analytics
response = requests.get(
    "http://localhost:8000/analytics/tools-usage",
    params={"engineer_id": "john_doe"}
)
```

## Data Storage

The tool uses SQLite database to store all automation records. The database file will be created automatically at `automation.db`.
# mykonos-agent
