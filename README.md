# Smart-Edu: Intelligent Exam Platform

**Live Demo:** [https://smart-edu.ziadgamal.com](https://smart-edu.ziadgamal.com)

Automated PDF question extraction with 99.61% accuracy. Transforms paper exams into digital practice tests in minutes.

![Admin Dashboard](screenshots/03-admin-dashboard-analytics.png)

---

## Overview

Smart-Edu addresses a critical bottleneck in the e-learning industry: manual data entry. Educational institutions spend countless hours digitizing legacy exams. This platform automates the entire process using a custom AI pipeline, reducing digitization time from days to seconds.

**Key Achievement:** Extracted 2,055 out of 2,063 questions (99.61% accuracy) from a single PDF in under 30 seconds.

## Key Features

### Intelligent PDF Extraction
*   **High Accuracy:** Proven 99.61% extraction rate on complex layouts.
*   **Structure Recognition:** Automatically identifies questions, choices (A-D), and correct answers.
*   **Media Handling:** Preserves mathematical formulas and diagrams.
*   **Quality Control:** Automated flags for low-confidence extractions requiring human review.

![PDF Upload Interface](screenshots/06-admin-pdf-upload.png)

### Student Experience
*   **Real-time Exam Player:** A seamless, distraction-free environment for taking practice tests.
*   **Instant Feedback:** Immediate grading with detailed performance breakdowns.
*   **AI Tutoring:** Integrated AI provides context-aware explanations for incorrect answers, acting as a personal tutor.
*   **Multi-Theme Support:** Optimized for readability in both Light and Dark modes.

![Student Exam Interface](screenshots/12-student-exam-interface.png)
![Student Dashboard](screenshots/10-student-dashboard.png)
![Available Exams](screenshots/11-student-available-exams.png)
![AI Feedback](screenshots/13-student-ai-feedback.png)

## Business Impact

Smart-Edu transforms the operational workflow of educational institutions:
1.  **Operational Efficiency:** Reduces exam digitization time by **99%** (from days to minutes).
2.  **Cost Reduction:** Eliminates the need for dedicated data-entry personnel.
3.  **Student Retention:** Provides a superior, tech-forward learning experience with instant feedback loops, increasing student engagement and satisfaction.


## Technology Stack

*   **Backend:** Laravel 11, PHP 8.3
*   **Frontend:** React 18, Inertia.js, TypeScript
*   **Infrastructure:** Nginx, Supervisor, Redis (Queue Management)
*   **AI & Processing:** Python 3.10, OpenAI API, PyMuPDF

## Architecture & Documentation

For a deep dive into the system's engineering, please refer to the documentation in the `docs/` directory:

*   **[Technical Project Overview](docs/PROJECT.md)**: Detailed feature breakdown and impact analysis.
*   **[System Architecture](docs/ARCHITECTURE.md)**: Diagrams and explanation of the hybrid PHP/Python pipeline and real-time event system.

## License

MIT License. See LICENSE file for details.

---

**Status:** Production Ready
**Contact:** [ziadgamal.com](https://ziadgamal.com)
