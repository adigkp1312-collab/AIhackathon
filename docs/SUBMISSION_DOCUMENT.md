SeekhoFree - AI for Bharat Hackathon Submission
================================================

Team Name: [Your Team Name]
Track: [Student / Professional]
GitHub: https://github.com/adigkp1312-collab/AIhackathon
Date: February 2026

================================================================================
SECTION 1: IDEA SUBMISSION
================================================================================

1.1 Problem Statement
---------------------

India has 850M+ people who cannot afford paid learning platforms like Seekho, Unacademy, or BYJU's (Rs 500-5000/month). Meanwhile, world-class free educational content already exists — scattered across YouTube, NPTEL, MIT OCW, Khan Academy, and SWAYAM.

The core problems:
- Discovery: Searching "learn Python" on YouTube gives 50M+ results with no structured path
- Curation: Learners don't know WHAT to learn, in WHAT order, from WHERE
- Language barrier: Most structured courses are in English; 90% of India prefers Hindi or regional languages
- Access: Paid apps require downloads and subscriptions; rural India is WhatsApp-first
- Drop-off: 65% of self-learners drop out within the first week due to lack of structure and guidance

This is not a content problem — it is an organization and access problem.


1.2 Proposed Solution
---------------------

SeekhoFree is a voice-first AI learning assistant that:

1. Understands what the user wants to learn (voice or text, in any of 11 Indian languages)
2. Uses Amazon Bedrock AI to generate a structured, multi-week course plan
3. Curates the best FREE resources from YouTube, NPTEL, MIT OCW, Khan Academy, SWAYAM
4. Prioritizes Hindi and regional language content
5. Delivers the plan on the platform the user already uses — WhatsApp, Telegram, Messenger, or web

Key insight: We don't create content. We use AI to organize the internet's best free education into personalized learning paths.

Think of it as "Google Maps for education" — the roads (content) already exist, we just give you the best route.


1.3 Target Users
----------------

- Tier 2/3 city students preparing for tech careers
- Rural smartphone users who primarily use WhatsApp
- First-generation learners who need guidance in their own language
- College students who can't afford coaching classes
- Working professionals looking to upskill for free


1.4 Technical Approach
----------------------

Architecture:

  User (Voice or Text, 11 Indian Languages)
       |
       v
  [Sarvam AI - Speech-to-Text]
  Converts voice input to text using Saaras v2 model
  Supports: Hindi, Tamil, Telugu, Bengali, Gujarati, Kannada, Malayalam, Marathi, Punjabi, Odia, English
       |
       v
  [Amazon Bedrock - AI Course Plan Generator]
  Uses Claude on Bedrock to:
  - Understand the learning goal
  - Assess skill level from conversation
  - Generate a structured multi-module curriculum
  - Recommend specific free resources for each module
  - Prioritize Hindi/regional language content
       |
       v
  [Content Aggregation Layer]
  Searches and curates content from:
  - YouTube (CodeWithHarry, CampusX, Apna College, FreeCodeCamp, etc.)
  - NPTEL (IIT/IISc courses)
  - MIT OpenCourseWare
  - Khan Academy
  - SWAYAM
       |
       v
  [Sarvam AI - Text-to-Speech]
  Reads the course plan aloud using Bulbul v2 model
  Natural Indian-accent voices in all 11 languages
       |
       v
  [Multi-Platform Delivery]
  - Web App (mobile-first responsive UI)
  - WhatsApp Business API (webhook integration)
  - Facebook Messenger (webhook integration)
  - Telegram Bot (webhook integration)


1.5 AWS Services Used
---------------------

| AWS Service         | How We Use It                                              |
|--------------------|------------------------------------------------------------|
| Amazon Bedrock     | Core AI engine - generates personalized course plans       |
|                    | from user's learning goals using Claude foundation model   |
| Amazon Q           | Enhances content discovery and recommendation quality      |
| AWS Lambda (next)  | Serverless webhook handlers for messaging platforms        |
| Amazon DynamoDB    | Store user learning progress and preferences (next phase)  |
| Amazon S3          | Cache aggregated content metadata (next phase)             |
| Amazon CloudFront  | CDN for web app delivery (next phase)                      |


1.6 Innovation & Creativity
----------------------------

What makes SeekhoFree novel:

1. AI as Curator, Not Creator: Instead of competing with content creators, we organize existing free content. This means infinite content library at zero content cost.

2. Voice-First for India: Most Indian users are more comfortable speaking than typing. Using Sarvam AI's Indian language models, users can say "mujhe Python seekhna hai" and get a full course plan spoken back.

3. WhatsApp Delivery: 500M+ Indians use WhatsApp daily. By delivering course plans via WhatsApp, we meet users where they already are — no app download needed.

4. Multilingual AI Planning: The Bedrock AI understands requests in Hindi, Hinglish, and regional languages, and prioritizes content in the user's preferred language.

5. Zero-Cost Commitment: The platform will always be free. We aggregate free content and use AI to add value on top.


================================================================================
SECTION 2: SLIDE DECK CONTENT (10-12 Slides)
================================================================================

--- SLIDE 1: TITLE ---

SeekhoFree
Learn Anything. Free Forever.

Voice-first AI learning assistant that brings free education to every Indian through YouTube, NPTEL, and open university courses.

Team: [Your Team Name]
Track: [Student / Professional]
AI for Bharat Hackathon | Hack2Skill + AWS


--- SLIDE 2: THE PROBLEM ---

850M+ Indians cannot afford paid learning platforms

- Seekho, Unacademy, BYJU's charge Rs 500-5000/month
- World-class free content exists scattered across YouTube, NPTEL, MIT OCW, Khan Academy
- But learners don't know WHAT to learn, in WHAT order, from WHERE
- Language barrier: Most structured courses are in English
- 65% of Indian self-learners drop out in the first week due to lack of structure

The content exists. The structure doesn't.


--- SLIDE 3: OUR SOLUTION ---

SeekhoFree = AI-Powered Free Course Aggregator + Voice-First Interface

1. Tell the AI what you want to learn (voice or text, any Indian language)
2. AI creates a structured course plan from the best FREE resources
3. Resources curated from YouTube, NPTEL, MIT OCW, Khan Academy, SWAYAM
4. Prioritizes Hindi/regional language content
5. Available on web, WhatsApp, Messenger, Telegram — no app download needed

"Seekho jaisa experience, completely free"


--- SLIDE 4: HOW IT WORKS (ARCHITECTURE) ---

[Architecture diagram - see Section 1.4 above]

User speaks or types in any Indian language
  -> Sarvam AI converts speech to text
  -> Amazon Bedrock generates structured course plan
  -> Content layer finds best free resources
  -> Sarvam AI reads plan aloud
  -> Delivered via Web / WhatsApp / Messenger / Telegram


--- SLIDE 5: KEY FEATURES ---

| Feature              | How                                                      |
|---------------------|----------------------------------------------------------|
| AI Course Planning  | Amazon Bedrock generates personalized learning paths     |
| Voice-First         | Sarvam AI: voice interaction in 11 Indian languages      |
| Free Content Only   | Aggregates YouTube, NPTEL, MIT OCW, Khan Academy, SWAYAM |
| Multi-Platform      | Web + WhatsApp + Messenger + Telegram                    |
| Hindi Priority      | Prefers Hindi/regional language content when available    |
| Zero Cost           | 100% free for learners, always                           |


--- SLIDE 6: DEMO ---

[Screenshots to add:]
1. Welcome screen with topic suggestions
2. User asking "I want to learn Python programming"
3. AI-generated 6-week structured course plan
4. Module detail with YouTube + NPTEL resources
5. Voice input button and language selector
6. WhatsApp conversation example


--- SLIDE 7: AWS SERVICES USED ---

| AWS Service      | Usage                                                |
|-----------------|------------------------------------------------------|
| Amazon Bedrock  | Core AI - generates personalized course plans        |
| Amazon Q        | Content discovery and recommendation enhancement     |
| Lambda (next)   | Serverless webhook handlers for messaging platforms  |
| DynamoDB (next) | User progress tracking and preferences               |
| S3 (next)       | Content metadata caching                             |
| CloudFront      | Web app CDN delivery                                 |


--- SLIDE 8: DIFFERENTIATORS ---

| Seekho / Unacademy / BYJU's | SeekhoFree                          |
|-----------------------------|--------------------------------------|
| Rs 500-5000/month           | Free forever                         |
| Proprietary content          | Aggregates existing free content     |
| App-only                     | WhatsApp, Messenger, Web, Telegram   |
| Pre-built courses            | AI creates personalized plans        |
| English-heavy                | Hindi-first, 11 Indian languages     |
| Watch passively              | Voice-first, conversational          |

Key insight: We don't create content. We organize the internet's best free education with AI.


--- SLIDE 9: IMPACT & RELEVANCE ---

Target: 850M+ Indians who can't afford paid platforms

Impact:
- Democratize access to world-class education
- Bridge the language gap in tech education
- Reduce dependency on expensive coaching
- Enable self-paced learning with AI mentorship

Alignment with AI for Bharat:
- Solves a real Indian problem using AI
- Built on AWS infrastructure (Bedrock)
- Multilingual, accessible, inclusive
- Designed for Bharat, not just India's metros


--- SLIDE 10: MARKET OPPORTUNITY ---

- Indian EdTech market: $10.4B+ (growing 39% CAGR)
- 500M+ smartphone users in India
- 500M+ WhatsApp users in India (largest market globally)
- NPTEL: 60,000+ hours of free content
- YouTube: 1M+ free courses relevant to Indian learners

Future sustainability model (to keep it free):
- Freemium mentorship (AI = free, human mentor = paid)
- Certificate partnerships with NPTEL/SWAYAM
- Corporate sponsorships (companies sponsor learning in their tech stack)
- Zero ads, zero paywalls on core learning


--- SLIDE 11: ROADMAP ---

Phase 1 — Now (Prototype):
- Web app with AI course planning (Amazon Bedrock)
- Voice interaction in 11 languages (Sarvam AI)
- YouTube + NPTEL content aggregation
- WhatsApp/Messenger/Telegram webhook scaffold

Phase 2 — 1-3 Months:
- Live WhatsApp and Telegram bots
- User learning progress tracking (DynamoDB)
- AI-powered content quality scoring
- Regional language UI (Hindi, Tamil, Telugu)

Phase 3 — 3-6 Months:
- Community features (study groups, peer learning)
- AI-generated quizzes from course content
- Offline content caching for low-connectivity areas
- Partnerships with NPTEL, SWAYAM for certificates


--- SLIDE 12: TEAM & ASK ---

Team: [Your Name(s) and roles]

What we've built:
- Working prototype with AI course planning
- Voice-first interface in 11 Indian languages
- Multi-platform architecture (Web + WhatsApp + Messenger + Telegram)
- Full codebase on GitHub

What we need:
- AWS credits for Bedrock scaling
- Partnerships with content platforms (NPTEL, SWAYAM)
- Mentorship on scaling to 1M+ users

Our vision: Every Indian learns what they want, when they want, in their language — for free.


================================================================================
SECTION 3: TECHNICAL DETAILS (for GitHub README / Documentation)
================================================================================

3.1 Tech Stack
--------------

| Component   | Technology                                          |
|------------|-----------------------------------------------------|
| AI Engine  | Amazon Bedrock (Claude foundation model)            |
| Voice      | Sarvam AI (Bulbul v2 TTS + Saaras v2 STT)          |
| Backend    | Python 3.11, FastAPI                                |
| Content    | YouTube Data API v3, NPTEL, MIT OCW                 |
| Messaging  | WhatsApp Business API, Messenger, Telegram Bot API  |
| Frontend   | HTML/CSS/JS (mobile-first, no framework bloat)      |


3.2 API Endpoints
-----------------

POST /api/chat              - Send learning query, get structured course plan
POST /api/voice/stt         - Speech-to-text (Sarvam AI)
POST /api/voice/tts         - Text-to-speech (Sarvam AI)
GET  /api/search?q=python   - Search free YouTube content
GET  /api/sources           - List curated free learning sources
GET  /api/languages         - List supported Indian languages
POST /webhooks/whatsapp     - WhatsApp incoming message webhook
POST /webhooks/messenger    - Facebook Messenger webhook
POST /webhooks/telegram     - Telegram bot webhook


3.3 Supported Languages
------------------------

Hindi, Bengali, Tamil, Telugu, Gujarati, Kannada, Malayalam, Marathi, Punjabi, Odia, English (Indian)


3.4 Free Content Sources
-------------------------

YouTube (Hindi): CodeWithHarry, Apna College, CampusX, Love Babbar, Hitesh Choudhary, 5 Minute Engineering
YouTube (English): freeCodeCamp, Traversy Media, CS50, 3Blue1Brown, Sentdex, Corey Schafer
University: NPTEL (IIT/IISc), MIT OpenCourseWare, Khan Academy, Stanford Online, SWAYAM


================================================================================
SECTION 4: JUDGING CRITERIA ALIGNMENT
================================================================================

| Criteria                          | Weight | How SeekhoFree Scores                                |
|----------------------------------|--------|------------------------------------------------------|
| Technical Excellence             | 30%    | Amazon Bedrock for AI planning, Sarvam AI for voice, |
|                                  |        | multi-platform webhooks, clean FastAPI architecture,  |
|                                  |        | YouTube API integration                               |
|                                  |        |                                                      |
| Innovation & Creativity          | 30%    | Novel approach: organize free content with AI instead |
|                                  |        | of creating paid content. Voice-first for             |
|                                  |        | accessibility. WhatsApp delivery for reach.           |
|                                  |        |                                                      |
| Impact & Relevance               | 25%    | Directly addresses India's education access gap.      |
|                                  |        | 850M+ potential users. Hindi-first. Works on any      |
|                                  |        | smartphone via WhatsApp.                              |
|                                  |        |                                                      |
| Completeness & Presentation      | 15%    | Full working prototype, comprehensive slide deck,     |
|                                  |        | video demo, clean documentation and GitHub repo.      |


================================================================================
SECTION 5: VIDEO PITCH SCRIPT (3 minutes)
================================================================================

[0:00 - 0:30] THE HOOK
"850 million Indians can't afford Seekho or Unacademy. But the best courses in the world are already free on YouTube and NPTEL. The problem isn't content — it's organization. Meet SeekhoFree."

[0:30 - 1:00] THE DEMO
"Watch — I say 'mujhe Python seekhna hai' and the AI instantly creates a 6-week structured course plan from the best free YouTube and NPTEL resources, in Hindi. No signup. No payment. No app download."
[Show the web app: voice input -> course plan generation -> module details]

[1:00 - 1:30] HOW IT WORKS
"Under the hood: Sarvam AI handles voice in 11 Indian languages. Amazon Bedrock generates the personalized curriculum. Our content layer curates from YouTube, NPTEL, MIT OCW, and Khan Academy. And it all works on WhatsApp — where 500 million Indians already are."
[Show architecture briefly]

[1:30 - 2:15] WHY IT MATTERS
"A student in a village in Bihar can now say 'I want to learn web development' on WhatsApp, in Hindi, and get the same quality learning path as someone in Bangalore — for free. That's what AI for Bharat means to us."
[Show WhatsApp integration, language selector, course plan]

[2:15 - 2:45] DIFFERENTIATION & FUTURE
"Unlike paid platforms, we don't create content — we organize existing free content with AI. Our roadmap: progress tracking, AI quizzes, offline caching for low-connectivity areas, and partnerships with NPTEL for certificates."

[2:45 - 3:00] CLOSE
"SeekhoFree. Learn anything, free forever. Built with Amazon Bedrock and Sarvam AI, for Bharat."


================================================================================
END OF SUBMISSION DOCUMENT
================================================================================

Instructions:
1. Copy this into Google Docs
2. Fill in [Your Team Name] everywhere
3. Choose your track: Student or Professional
4. Create the slide deck in the prescribed Hack2Skill template using Section 2
5. Record the video using the script in Section 5
6. Submit at: https://vision.hack2skill.com/event/ai-for-bharat
