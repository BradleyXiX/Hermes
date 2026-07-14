readme_content = """# 🏛️ Hermes: Autonomous AI Email Liaison & Calendar Coordinator

An intelligent, zero-cost, multi-agent personal assistant that brings your inbox, calendar, and documents directly to your fingertips via a secure private Telegram Bot. Built with **CrewAI**, powered by **Google Gemini 2.5 Flash** (via Google AI Studio's generous free tier), and integrated natively with Google Workspace.

---

## 🚀 Overview

**Hermes** acts as your digital shadow, running silently in the background (locally or self-hosted) and handling your scheduling, triage, and email management. Instead of spending hours reading through newsletters, draft responses, and coordinating meetings, you interact with Hermes through conversational commands right inside Telegram. 

Designed for developers, students, and busy professionals who want an autonomous setup without recurring API costs.

---

## ✨ Core Features

Hermes is equipped with five main superpowers:

### 1. ✍️ Human-in-the-Loop Email Drafting
*   **Drafting, Not Sending:** Hermes never sends an email without your explicit consent. It reads incoming threads, matches your personal voice, and generates a perfect draft directly in your Gmail account.
*   **Approval Flow:** Receive notifications on Telegram with summaries of drafted replies. Once verified, simply open your Gmail drafts and click send, or let Hermes write alternative versions based on quick feedback.

### 2. 📅 Daily Inbox Briefing (Scheduled Digest)
*   **Morning Summary:** Every morning at your chosen time, Hermes scans your unread emails from the last 24 hours.
*   **Intelligent Filtering:** It filters out newsletters, promotions, and spam, organizing high-priority threads into categorizations (e.g., `🔴 Action Required`, `🟡 FYI`, `🟢 Academic / Work`).
*   **Clean Telegram Delivery:** Delivered directly to your chat in a single, elegantly formatted message so you can plan your day.

### 3. 🕹️ Interactive "Quick Action" Buttons
*   **Frictionless Control:** Important alerts come attached with Telegram Inline Keyboard buttons.
*   **One-Tap Operations:** Tap a button under an urgent incoming mail notification to trigger pre-defined agent tasks:
    *   `[Draft Polite Extension Request]`
    *   `[Confirm Appointment]`
    *   `[Mark as Read & Archive]`

### 4. 🗓️ Google Calendar Coordinator
*   **Smart Scheduling:** Hermes cross-references incoming email meeting requests with your Google Calendar to detect conflicts.
*   **Double-Booking Prevention:** It automatically blocks tentative holds for proposed meeting slots and drafts responses confirming your availability.
*   **Natural Language Creation:** Tell Hermes: *"Create a review session with my team tomorrow at 4 PM"*, and it will schedule the calendar event and invite the relevant parties automatically.

### 5. 📂 Document & Attachment Analyzer
*   **Massive Context Handling:** Harnessing Gemini's immense context window, Hermes can analyze dense attachments forwarded via Telegram (such as course syllabi, assignment PDFs, or extensive API documentation).
*   **Summaries & Extractions:** Ask: *"Summarize the grading rubric from this PDF"* or *"What does this API document require for authentication?"* and receive concise bullet-points in seconds.

### 6. 🧠 Hot-Reloading Knowledge Base (Memory)
*   **Dynamic Learning:** Update Hermes' worldview on the fly. Just tell the bot: *"Remember: I have volunteer sessions every Mon/Wed/Fri from 9 AM to noon."*
*   **Context-Aware Operations:** Hermes saves this constraint to its local knowledge base and automatically avoids scheduling meetings or drafting availability during those hours.

---

## 🛠️ Architecture Stack (Zero-Cost)

*   **Orchestration:** [CrewAI](https://github.com/crewAIInc/crewAI) (Multi-agent framework)
*   **LLM Brain:** [Google Gemini 2.5 Flash](https://aistudio.google.com/) (1,500 free requests per day, 1M+ token context window)
*   **Telegram Bot Interface:** [aiogram v3](https://github.com/aiogram/aiogram) (Asynchronous Telegram Bot API)
*   **Integrations:** Google Workspace APIs (Gmail & Calendar OAuth2)
*   **Scheduler:** [APScheduler](https://github.com/agronholm/apscheduler) (For cron-like background digests)

---

## 📦 Directory Structure

```text
hermes/
│
├── config/
│   ├── agents.yaml          # Role backstories and Gemini prompt configurations
│   └── tasks.yaml           # Scheduled/On-demand task instructions
│
├── tools/
│   ├── gmail_tools.py       # Custom CrewAI tools for Gmail (Draft, Read, Archive)
│   ├── calendar_tools.py    # Custom tools for Google Calendar lookup & scheduling
│   └── knowledge_tools.py   # Memory tools to read/write custom constraints
│
├── memory/
│   └── knowledge_base.json  # Local hot-reloaded memory cache
│
├── .env                     # Private keys (Whitelisted Chat ID, Gemini API Key, Bot Token)
├── .gitignore               # Critical key/token exclusion rules
├── bot.py                   # Main asynchronous Telegram long-polling listener (aiogram)
├── crew.py                  # CrewAI multi-agent initialization and workflow
├── requirements.txt         # Project dependencies
└── README.md                # Documentation (You are here!)