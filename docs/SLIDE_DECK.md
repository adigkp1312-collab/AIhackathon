# SeekhoFree - Hackathon Slide Deck Content
## AI for Bharat | Hack2Skill + AWS

Use this content to fill in the prescribed 10-12 slide template.

---

### Slide 1: Title Slide

**SeekhoFree**
*Learn Anything. Free Forever.*

Voice-first AI learning assistant that brings free education to every Indian through YouTube, NPTEL, and open university courses.

Team: [Your Team Name]
Track: [Student / Professional]

---

### Slide 2: The Problem

**850M+ Indians cannot afford paid learning platforms**

- Seekho, Unacademy, BYJU's charge Rs 500-5000/month
- Meanwhile, world-class free content exists scattered across YouTube (CodeWithHarry, CampusX, Apna College), NPTEL, MIT OCW, Khan Academy
- But learners don't know WHAT to learn, in WHAT order, from WHERE
- Language barrier: Most structured courses are in English; learners prefer Hindi/regional languages
- Discovery problem: Searching "learn Python" gives 50M results - no structured path

**Impact:**
- 65% of Indian learners drop out within first week due to lack of structure
- Rural learners have smartphones but not the Rs 500/month for learning apps

---

### Slide 3: Our Solution

**SeekhoFree = AI-Powered Free Course Aggregator + Voice-First Interface**

1. Tell the AI what you want to learn (voice or text, any Indian language)
2. AI creates a structured course plan from the best FREE resources
3. Resources curated from YouTube, NPTEL, MIT OCW, Khan Academy, SWAYAM
4. Prioritizes Hindi/regional language content
5. Available on web, WhatsApp, Messenger, Telegram - no app download needed

*"Seekho jaisa experience, completely free"*

---

### Slide 4: How It Works (Architecture)

```
User (Voice/Text)
    |
    v
[Sarvam AI] -- Speech-to-Text (11 Indian languages)
    |
    v
[Amazon Bedrock] -- AI Course Plan Generator
    |                (understands learning goals,
    |                 creates structured curriculum)
    v
[Content Aggregator] -- YouTube API, NPTEL, MIT OCW
    |
    v
[Response] -- Structured course plan + resource links
    |
    v
[Sarvam AI] -- Text-to-Speech (reads plan aloud)
    |
    v
User (Web / WhatsApp / Messenger / Telegram)
```

---

### Slide 5: Key Features

| Feature | How |
|---|---|
| **AI Course Planning** | Amazon Bedrock generates personalized, structured learning paths |
| **Voice-First** | Sarvam AI enables voice interaction in 11 Indian languages |
| **Free Content Only** | Aggregates YouTube, NPTEL, MIT OCW, Khan Academy, SWAYAM |
| **Multi-Platform** | Web app + WhatsApp + Messenger + Telegram bots |
| **Hindi Priority** | Prefers Hindi/regional language content when available |
| **Zero Cost** | 100% free for learners, always |

---

### Slide 6: Demo / Screenshots

[Include screenshots of the web app showing:]
1. Welcome screen with quick topic chips
2. User asking "I want to learn Python programming"
3. AI generating a structured 6-week course plan
4. Modules with curated YouTube + NPTEL resources
5. Voice interaction button (mic icon)
6. WhatsApp bot conversation example

---

### Slide 7: AWS Services Used

| AWS Service | Usage |
|---|---|
| **Amazon Bedrock** | Core AI engine - generates personalized course plans from learning goals |
| **Amazon Q** | Enhances content discovery and recommendation quality |
| Future: **Amazon Polly** | Fallback TTS for languages not covered by Sarvam |
| Future: **AWS Lambda** | Serverless webhook handlers for WhatsApp/Messenger |
| Future: **Amazon DynamoDB** | Store user learning progress and preferences |
| Future: **Amazon S3** | Cache aggregated content metadata |

---

### Slide 8: Differentiators

| vs Seekho/Unacademy/BYJU's | SeekhoFree |
|---|---|
| Rs 500-5000/month | **Free forever** |
| Proprietary content | **Aggregates existing free content** |
| App-only | **WhatsApp, Messenger, Web, Telegram** |
| Pre-built courses | **AI creates personalized plans** |
| English-heavy | **Hindi-first, 11 Indian languages** |
| Watch passively | **Voice-first, conversational** |

**Key insight:** We don't create content. We organize the internet's best free education with AI.

---

### Slide 9: Impact & Relevance

**Target Users:**
- 850M+ Indians who can't afford paid platforms
- Tier 2/3 city students preparing for careers
- Rural smartphone users (WhatsApp-first)
- First-generation learners who need guidance in their language

**Potential Impact:**
- Democratize access to world-class education
- Bridge the language gap in tech education
- Reduce dependency on expensive coaching
- Enable self-paced learning with AI mentorship

**Alignment with AI for Bharat:**
- Solves a real Indian problem using AI
- Uses AWS infrastructure (Bedrock)
- Multilingual, accessible, inclusive

---

### Slide 10: Market Opportunity

- Indian EdTech market: $10.4B by 2025 (growing 39% CAGR)
- 500M+ smartphone users in India
- WhatsApp has 500M+ users in India (largest market)
- NPTEL has 60,000+ free hours of content
- YouTube has 1M+ free courses relevant to Indian learners

**Business model (future, to sustain free access):**
- Freemium mentorship (AI mentor is free; human mentor connects for a fee)
- Certificate partnerships with NPTEL/SWAYAM
- Corporate sponsorships (companies sponsor free learning in their tech stack)
- Zero ads, zero paywalls on core learning

---

### Slide 11: Roadmap

**Phase 1 (Now - Prototype):**
- Web app with AI course planning (Amazon Bedrock)
- Voice interaction (Sarvam AI)
- YouTube + NPTEL content aggregation
- WhatsApp bot scaffold

**Phase 2 (1-3 months):**
- Live WhatsApp + Telegram bots
- User progress tracking
- Content quality scoring with AI
- Regional language UI (Hindi, Tamil, Telugu)

**Phase 3 (3-6 months):**
- Community features (study groups)
- AI-powered quizzes from course content
- Offline content caching for low-connectivity areas
- Partnerships with NPTEL, SWAYAM for certificates

---

### Slide 12: Team & Ask

**Team:** [Your Name(s)]

**What we've built:**
- Working prototype with AI course planning
- Voice-first interface in 11 Indian languages
- Multi-platform architecture (Web + WhatsApp + Messenger + Telegram)

**What we need:**
- AWS credits for Bedrock scaling
- Partnerships with content platforms (NPTEL, SWAYAM)
- Mentorship on scaling to 1M+ users

**Our vision:** Every Indian learns what they want, when they want, in their language - for free.

---

## Judging Criteria Alignment

| Criteria (Weight) | How We Score |
|---|---|
| **Technical Excellence (30%)** | Amazon Bedrock for AI planning, Sarvam AI for voice, multi-platform webhooks, clean FastAPI architecture |
| **Innovation & Creativity (30%)** | Novel approach - don't create content, organize free content with AI. Voice-first for accessibility. WhatsApp delivery for reach. |
| **Impact & Relevance (25%)** | Directly addresses India's education access gap. 850M+ potential users. Hindi-first. Works on any smartphone via WhatsApp. |
