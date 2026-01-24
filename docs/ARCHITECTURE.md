# Smart-Edu Technical Architecture

> **Detailed technical documentation for developers and technical stakeholders**

## System Architecture Overview

Smart-Edu follows a modern full-stack architecture with a clear separation between frontend, backend, and external processing services.

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Browser                            │
│  (React SPA via Inertia.js - Server-Side Routing)           │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/HTTPS
                     │ Session-based Auth
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Laravel Application Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ Controllers  │  │  Services    │  │   Models    │        │
│  │ (HTTP)       │→ │ (Business)  │→ │ (Data)      │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ Process Execution
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           PDF Processing Pipeline (Python)                    │
│  ┌─────────────┐        ┌──────────────┐                   │
│  │  parse.py   │  ────▶ │  extract.py  │                   │
│  │ (Text +     │        │ (Questions + │                   │
│  │  Styling)   │        │  Detection)  │                   │
│  └─────────────┘        └──────────────┘                   │
└─────────────────────────────────────────────────────────────┘
                     │
                     │ Structured JSON
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              MySQL Database                                   │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐              │
│  │  exams     │ │ questions  │ │ choices    │              │
│  │  sessions  │ │ ai_feedbacks││ mappings   │              │
│  └────────────┘ └────────────┘ └────────────┘              │
└─────────────────────────────────────────────────────────────┘
```

## Component Architecture

### Frontend Layer

**Technology**: React 18 + Inertia.js + TypeScript

**Key Components:**
- **Admin Dashboard**: Exam management, import management, question review
- **Student Interface**: Exam taking, results viewing, progress tracking
- **Upload Interface**: Drag-and-drop PDF upload with real-time progress

**State Management:**
- Inertia.js for server-driven state
- React hooks for local UI state
- Form handling via Inertia's useForm hook

**Routing:**
- Server-side routing (Laravel routes)
- Client-side navigation (Inertia Link components)
- No API boilerplate needed

### Backend Layer

**Technology**: Laravel 12 (PHP 8.3+)

**Architecture Pattern**: Service Layer + Repository Pattern

**Key Services:**
- `NewPdfParserService`: Orchestrates PDF parsing workflow
- `ExamService`: Exam CRUD operations
- `QuestionCommentService`: Student question comments
- `ExamSessionService`: Session tracking and scoring

**Request Flow:**
```
HTTP Request → Middleware → Controller → FormRequest (Validation) → Service → Model → Database
```

**Authentication:**
- Laravel Sanctum for API tokens
- Session-based auth for web routes
- Role-based authorization (Admin/Student)

### PDF Processing Layer

**Technology**: Python 3.10+ with PyMuPDF

**Two-Stage Pipeline:**

1. **Parse Stage** (`parse.py`)
   - Input: PDF file path
   - Process: Extract text with styling metadata
   - Output: JSON array of text elements with properties
   - Styling Captured: bold, italic, color, font size, position

2. **Extract Stage** (`extract.py`)
   - Input: Parsed JSON from stage 1
   - Process: Pattern recognition for questions and choices
   - Detection Methods:
     - Question numbers: Regex pattern matching
     - Choice markers: A-D or 1-4 pattern detection
     - Correct answers: Bold+red style analysis
   - Output: Structured questions with metadata

**Error Handling:**
- Graceful degradation on parsing errors
- Quality flags for incomplete questions
- Automatic gap detection in question sequences

## Data Flow

### PDF Import Workflow

```
1. Admin uploads PDF
   ↓
2. Laravel receives file → stores in storage/app/uploaded/
   ↓
3. NewPdfParserService.parseAndExtract() called
   ↓
4. parse.py executed (subprocess)
   → Output: storage/app/parsed/{hash}.json
   ↓
5. extract.py executed (subprocess)
   → Output: storage/app/extracted/{hash}.json
   ↓
6. Format adaptation (new format → legacy DB format)
   ↓
7. Database import (batch transaction)
   → Questions, Choices, ExamQuestionMap created
   ↓
8. Success response with statistics
```

### Exam Taking Workflow

```
1. Student selects exam
   ↓
2. ExamSession created (status: 'in_progress')
   ↓
3. Questions loaded via ExamQuestionMap
   ↓
4. Student answers → StudentAnswer records created
   ↓
5. On submission → ExamSession.status = 'completed'
   ↓
6. Scoring calculation (real-time)
   ↓
7. AI Feedback generation (async, cached)
   ↓
8. Results displayed with feedback
```

## Database Schema

### Core Tables

**exams**
- `id`, `title`, `created_by_admin_id`, `total_questions`, `is_practice`

**questions**
- `id`, `uid` (UUID), `text`, `question_number`, `source_pdf`, `canonical_hash`, `status`, `confidence_level`

**choices**
- `id`, `question_id`, `text`, `is_correct`, `position` (A-D), `choice_index`

**exam_question_map**
- `id`, `exam_id`, `question_id`, `order_index`
- Unique constraint on (exam_id, question_id)

**exam_sessions**
- `id`, `exam_id`, `student_id`, `status`, `score`, `started_at`, `completed_at`

**student_answers**
- `id`, `session_id`, `question_id`, `choice_id`, `is_correct`, `answered_at`

### Key Indexes

- `questions.canonical_hash` - Unique index for duplicate detection
- `exam_question_map(exam_id, question_id)` - Unique constraint
- Composite indexes on frequently queried columns

## Security Architecture

### Authentication
- **Web Routes**: Laravel session-based (stateless via Sanctum tokens for API)
- **API Routes**: Bearer token authentication
- **CSRF Protection**: Built-in Laravel middleware

### Authorization
- **Role-based**: UserRole enum (Admin/Student)
- **Policies**: ExamPolicy, QuestionPolicy for fine-grained control
- **Resource Ownership**: Admins own exams, students own sessions

### Data Protection
- **Input Validation**: FormRequest classes for all inputs
- **SQL Injection**: Eloquent ORM with parameterized queries
- **XSS Prevention**: Blade/React auto-escaping
- **File Upload**: Type and size validation, secure storage paths

## Performance Optimizations

### Caching Strategy
- **Configuration**: `php artisan config:cache`
- **Routes**: `php artisan route:cache`
- **Views**: `php artisan view:cache`
- **AI Feedback**: Redis/file-based caching for expensive operations

### Database Optimizations
- **Indexes**: Strategic indexes on foreign keys and search columns
- **Eager Loading**: Relationships loaded efficiently (no N+1 queries)
- **Batch Operations**: Bulk inserts for question/choice import
- **Connection Pooling**: MySQL connection management

### Frontend Optimizations
- **Code Splitting**: React lazy loading for routes
- **Asset Bundling**: Vite for optimal production builds
- **Image Optimization**: Lazy loading for question images
- **Caching Headers**: Browser caching for static assets

## Scalability Considerations

### Horizontal Scaling
- **Stateless Design**: Laravel sessions stored in database/Redis
- **Load Balancer Ready**: No server-side session storage
- **Queue Workers**: Separate processes for background jobs

### Vertical Scaling
- **Memory Management**: Queue workers with memory limits
- **Timeout Handling**: Long-running PDF parsing with proper timeouts
- **Resource Monitoring**: Logging and error tracking

### Database Scaling
- **Read Replicas**: Read-heavy queries can use replicas
- **Partitioning**: Exam sessions table could be partitioned by date
- **Archive Strategy**: Old sessions can be archived

## Error Handling & Monitoring

### Exception Handling
- **Global Handler**: Laravel's exception handler
- **Custom Exceptions**: Domain-specific exceptions
- **Graceful Degradation**: Partial imports continue on errors

### Logging
- **Laravel Logs**: `storage/logs/laravel.log`
- **Queue Logs**: Separate logging for background jobs
- **Error Tracking**: Structured error logging with context

### Monitoring Points
- PDF parsing success rate
- Import job completion times
- Database query performance
- API response times
- Queue processing delays

## Deployment Architecture

### Production Stack
- **Web Server**: Nginx (reverse proxy)
- **Application Server**: PHP-FPM 8.3
- **Database**: MySQL 8.0 (standalone)
- **Queue Worker**: Separate PHP process
- **File Storage**: Local filesystem (can migrate to S3)

### Process Management
- **Supervisor**: Queue worker process management
- **Systemd**: PHP-FPM and Nginx service management
- **Cron Jobs**: Scheduled tasks (if any)

### CI/CD Pipeline
- **Git Workflow**: Feature branches → Production
- **Testing**: Automated tests before merge
- **Deployment**: Manual deployment with rollback capability

## Technology Choices Rationale

### Laravel Over Other Frameworks
- **Rapid Development**: Built-in features save development time
- **Ecosystem**: Rich package ecosystem
- **Documentation**: Excellent documentation
- **Community**: Large, active community

### React + Inertia.js Over Traditional SPA
- **No API Boilerplate**: Inertia eliminates need for API layer
- **Server-Side Routing**: SEO-friendly, maintainable routes
- **Full-Stack Integration**: Seamless data flow
- **Performance**: Optimistic updates, minimal JavaScript

### Python for PDF Processing
- **PyMuPDF Performance**: Fast PDF parsing
- **Flexibility**: Easy to modify extraction logic
- **Integration**: Simple subprocess execution from PHP
- **Maintainability**: Clear, readable code

### MySQL Over NoSQL
- **ACID Compliance**: Data integrity guarantees
- **Relationships**: Complex relationships handled efficiently
- **Maturity**: Proven, stable technology
- **Performance**: Excellent for read-heavy workloads

## Development Workflow

### Code Organization
```
app/
├── Http/
│   ├── Controllers/     # HTTP request handling
│   ├── Requests/       # Input validation
│   └── Resources/      # API response transformation
├── Services/           # Business logic
├── Models/            # Database models
└── Jobs/              # Background job processing

resources/js/
├── components/        # Reusable React components
├── pages/            # Inertia page components
└── layouts/          # Layout components
```

### Testing Strategy
- **Unit Tests**: Service layer logic
- **Feature Tests**: HTTP endpoints and workflows
- **Integration Tests**: Full user journeys
- **E2E Tests**: Cypress for critical paths

### Version Control
- **Branching**: Feature branches from main
- **Commits**: Conventional commit messages
- **Code Review**: Pull request reviews
- **Documentation**: Updated with each feature

---

**This architecture supports production-grade performance, security, and maintainability while remaining flexible for future enhancements.**

