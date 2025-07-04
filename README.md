# GitHub Webhook Dashboard

This project listens to GitHub webhooks for:
-  Push
-  Pull Request
-  Merge

Then it:
- Stores each event in **MongoDB Atlas**
- Shows live updates in a simple web UI (updates every 15 seconds)

---

## How to run

1) Clone the repo & go inside:
```bash
git clone <your-repo-url>
cd github_repository_project
2️) Install Python dependencies:
bash
Copy
Edit
pip install -r requirements.txt
3) Set up MongoDB Atlas

Create a cluster & database named: webhook_db

Create collection: events

4) Start the Flask server:
bash
Copy
Edit
python app.py
5) (Optional) Expose to GitHub using ngrok:

bash
Copy
Edit
pip install ngrok
ngrok http 5000
Copy the public HTTPS URL and add as GitHub webhook.

✨ Testing
Visit: http://127.0.0.1:5000/test-insert
Refresh http://127.0.0.1:5000 → see sample event
Each real webhook event will also appear here!

** Project structure
bash
Copy
Edit
github_repository_project/
├── app.py                # Flask backend
├── requirements.txt      # Python dependencies
├── README.md             # Project guide
├── templates/
│   └── index.html        # Frontend
✅ Author
Built by Piuli Kotal for project assignment
