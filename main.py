from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import json
import os
from typing import Optional
from datetime import datetime

app = FastAPI(title="EvansMathibe Agency API")

DATA_FILE = "inquiries.json"
ADMIN_PASSWORD = "admin123"

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "website")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
app.mount("", StaticFiles(directory=FRONTEND_DIR), name="root")


@app.get("/")
async def serve_frontend():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    return FileResponse(index_path)


@app.get("/{path:path}")
async def serve_frontend_catchall(path: str):
    file_path = os.path.join(FRONTEND_DIR, path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


class Inquiry(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    service: str
    message: str


def load_inquiries():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_inquiry(inquiry: Inquiry):
    inquiries = load_inquiries()
    inquiry_dict = inquiry.model_dump()
    inquiry_dict["id"] = len(inquiries) + 1
    inquiry_dict["timestamp"] = str(datetime.now())
    inquiries.append(inquiry_dict)
    with open(DATA_FILE, "w") as f:
        json.dump(inquiries, f, indent=2)
    return inquiry_dict


@app.post("/api/inquiry")
async def create_inquiry(inquiry: Inquiry):
    try:
        saved = save_inquiry(inquiry)
        return {
            "success": True,
            "message": "Inquiry submitted successfully",
            "id": saved["id"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/inquiry")
async def get_inquiries():
    return load_inquiries()


@app.get("/admin")
async def admin_page(request: Request):
    return HTMLResponse("""
    <html>
    <head><title>Admin - EvansMathibe Agency</title></head>
    <body>
        <h1>Admin Login</h1>
        <form method="post" action="/admin/login">
            <input type="password" name="password" placeholder="Enter admin password" required>
            <button type="submit">Login</button>
        </form>
    </body>
    </html>
    """)


@app.post("/admin/login")
async def admin_login(request: Request, password: str = Form(...)):
    if password == ADMIN_PASSWORD:
        inquiries = load_inquiries()
        html = """
        <html>
        <head>
            <title>Admin - EvansMathibe Agency</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #4CAF50; color: white; }
                tr:nth-child(even) { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>Inquiries</h1>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Service</th>
                    <th>Message</th>
                    <th>Timestamp</th>
                </tr>
        """
        for i in inquiries:
            html += f"""
                <tr>
                    <td>{i.get("id", "")}</td>
                    <td>{i.get("name", "")}</td>
                    <td>{i.get("email", "")}</td>
                    <td>{i.get("phone", "")}</td>
                    <td>{i.get("service", "")}</td>
                    <td>{i.get("message", "")}</td>
                    <td>{i.get("timestamp", "")}</td>
                </tr>
            """
        html += """
            </table>
            <p><a href="/admin">Logout</a></p>
        </body>
        </html>
        """
        return HTMLResponse(html)
    else:
        return HTMLResponse("Invalid password. <a href='/admin'>Try again</a>")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
