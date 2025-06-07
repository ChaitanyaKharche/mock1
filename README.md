# Lead-to-Lease Chat Concierge

This project is a tenant-facing chat micro-service that collects prospect details, checks for available units, and sends a tour confirmation email.

**Live Demo:** [Link to your deployed Render Frontend URL]

## Tech Stack
- **Backend:** FastAPI (Python)
- **Frontend:** React (Vite)
- **Database:** SQLite for conversation persistence
- **Deployment:** Render (via Docker and Static Site)
- **Email:** Gmail SMTP

## Core Features
- Collects Name, Email, Phone, Move-in Date, and Bed #.
- Validates email and phone number formats.
- Persists conversation state, allowing users to resume.
- Simulates an inventory check.
- Sends a tour confirmation email upon user request ("book").

## How to Run Locally

**Prerequisites:**
- Python 3.9+
- Node.js 18+
- Git

**1. Clone the repository:**
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd homewiz-chat
```

**2. Setup Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Create a `.env` file in the `backend` directory with your SMTP credentials (see `.env.example`).
```bash
# Run the backend server
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.

**3. Setup Frontend:**
In a new terminal:
```bash
cd frontend
npm install
npm run dev
```
The frontend will be available at `http://localhost:5173`.

## Trade-offs & Next Steps

- **State Management:** The current conversational logic is a simple, linear state machine. For more complex, non-linear conversations, an intent-based model using a library like Rasa or a service like Google Dialogflow would be more robust.
- **Inventory Stub:** `check_inventory()` is a stub. A real implementation would connect to a property management database with real-time availability.
- **Error Handling:** Error handling is basic. A production system would have structured logging (e.g., Loguru) and more granular error reporting.
- **SMS Webhook (Bonus):** To implement this, I would add another endpoint like `/sms` that accepts POST requests from a service like Twilio. The logic would be similar to `/chat`, but it would need to manage sessions based on the incoming phone number (`From` field in Twilio's payload).