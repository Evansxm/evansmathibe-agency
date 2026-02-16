# EvansMathibe Agency Backend

A FastAPI backend for the EvansMathibe Agency website.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python main.py
```

The server will start on `http://localhost:8000`

## API Endpoints

### Submit Inquiry
- **POST** `/api/inquiry`
- Body (JSON):
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "1234567890",
  "service": "Web Development",
  "message": "I'd like to inquire about your services"
}
```

### Get All Inquiries
- **GET** `/api/inquiry`

## Admin Panel

- **URL**: `http://localhost:8000/admin`
- **Password**: `admin123` (change in main.py)

## Data Storage

Inquiries are stored in `inquiries.json` in the project directory.
