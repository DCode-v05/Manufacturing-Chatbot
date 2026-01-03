# Inventary Assistance (Manufacturing Operations AI Assistant)

## Project Description
**Inventary Assistance** is a comprehensive AI-powered chatbot designed to assist manufacturing shop floor personnel. By leveraging **Google Gemini**, the system combines a static knowledge base of factory procedures (SOPs, Safety, Maintenance) with real-time status checks for specific machines and orders. The solution is deployed as a full-stack web application with a **FastAPI** backend and a **React** frontend.

---

## Project Details

### Problem Statement
Manufacturing environments rely on quick access to machine status, standard operating procedures (SOPs), and safety guidelines. **Inventary Assistance** bridges the gap between static documentation and real-time operational data, providing instant, context-aware support to operators, maintenance engineers, and plant managers.

### Key Features
- **Real-Time Status Queries**: Fetches live status (mocked or DB-driven) for:
  - **Machines**: Checks status for specific IDs (e.g., A1, B5).
  - **Orders**: Tracks order progress for IDs (e.g., 101, 102).
- **Knowledge Base Integration**:
  - Grounds responses in a factory-specific context document (`context_doc.md`).
  - covers Shift Schedules, Emergency Procedures, troubleshoot guides, and QC standards.
- **Context-Aware Conversations**:
  - **User Profiling**: Extracts and remembers user details (Name, Role).
  - **Memory Cache**: Maintains conversation history for relevant follow-up responses.
- **Safety & Compliance**:
  - Filters unsafe content using a dedicated safety middleware.
  - Logs token usage for monitoring.

---

## Tech Stack
- **Backend**: Python 3.x, FastAPI, Uvicorn
- **AI Engine**: Google Gemini (via `google-generativeai`)
- **Frontend**: React.js, Axios, React Markdown
- **Authentication/Security**: Google OAuth libraries (referenced in requirements)
- **Utilities**: `python-dotenv` for environment configuration

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/DCode-v05/Inventory-Assistance.git
cd Inventory-Assistance
```

### 2. Backend Setup
Navigate to the `app` directory and install dependencies:
```bash
cd app
# It is recommended to create a virtual environment first
# python -m venv venv
# venv\Scripts\activate

pip install -r ../requirements.txt
```

Run the FastAPI server:
```bash
uvicorn app.main:app --reload
```
The backend will run at `http://localhost:8000`.

### 3. Environment Configuration
Since `service_account.json` is gitignored for security, you must obtain your own Google Cloud Service Account credentials:
1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a project and enable the **Gemini API**.
3.  Create a Service Account and download the JSON key file.
4.  Rename the file to `service_account.json` and place it in the root directory of the project (same level as `requirements.txt`).

### 4. Frontend Setup
Navigate to the `frontend` directory and install dependencies:
```bash
cd frontend
npm install
```

Start the React development server:
```bash
npm start
```
The application will open at `http://localhost:3000`.

---

## Usage
1.  **Login/Profile**: Start by introducing yourself (e.g., "I am John, a Maintenance Engineer"). The bot will save your profile.
2.  **Ask Questions**:
    *   *Machine Status*: "What is the status of machine A1?"
    *   *SOPs*: "What is the emergency shutdown procedure?"
    *   *Shift Info*: "When does Shift B start?"
3.  **Review Output**: The bot provides concise, bulleted responses grounded in the factory knowledge base.

---

## Project Structure
```
Inventary Assistance/
│
├── app/                        # Backend Application
│   ├── data/
│   │   └── context_doc.md      # Knowledge Base Markdown
│   ├── middleware/             # Custom Middleware (Logging, etc.)
│   ├──routers/                 # API Routes (Chat, Workflow, Batch)
│   ├── services/               # Logic (Gemini, Context, Auth)
│   ├── utils/                  # Utility functions
│   └── main.py                 # Application Entry Point
│
├── frontend/                   # React Frontend
│   ├── public/                 # Static Assets
│   └── src/                    # Components & Pages
│
├── requirements.txt            # Python Dependencies
├── service_account.json        # Google Cloud Credentials (if applicable)
├── token_logs.csv              # Token Usage Logs
├── .gitignore                  # Git Ignore File
└── README.md                   # Project Documentation
```

---

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a pull request describing your changes.

---

## Contact
- **GitHub**: [DCode-v05](https://github.com/DCode-v05)
- **Email**: denistanb05@gmail.com
