
Project Vision: To engineer a robust, secure, and scalable Software as a Service (SaaS) platform for the Integrated School Transportation Management System (SIG-TE). The primary architectural driver is near-zero operational cost, achieved through a purely serverless stack leveraging Google Apps Script for the backend, Google Sheets as the database, and pay-per-use Google Cloud APIs for advanced features.

Core Principles:

Serverless First: All components must scale to zero to eliminate idle costs.

Data-Driven: The entire application schema and logic will be derived from the provided SIG-TE.txt file, ensuring functional parity and a seamless migration path.

AI-Powered: Gemini 2.5 Flash will be integrated for automated reporting, intelligent suggestions, and data analysis.

Secure by Design: Authentication will be handled via Google Identity (OAuth2), with role-based access control (RBAC) implemented at the application layer.

High-Standard UX: The frontend will be a modern, responsive Single-Page Application (SPA) providing a seamless and intuitive user experience.

Section 1: System Architecture & Foundation

This section establishes the foundational structure of the application.

Prompt 1.1: Generate the appsscript.json Manifest

Act as a Google Apps Script expert. Generate the appsscript.json manifest file for the SIG-TE web application.

Rationale: This file is critical for defining the project's permissions (OAuth scopes), execution environment, and web app access levels. The scopes must be comprehensive enough to allow interaction with Sheets, Drive, and external APIs.

code
JSON
download
content_copy
expand_less

{
  "timeZone": "America/Sao_Paulo",
  "runtimeVersion": "V8",
  "exceptionLogging": "STACKDRIVER",
  "oauthScopes": [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/script.external_request",
    "https://www.googleapis.com/auth/script.scriptapp",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/forms"
  ],
  "webapp": {
    "access": "ANYONE",
    "executeAs": "USER_DEPLOYING"
  }
}
Section 2: Data Model & Persistence (Google Sheets)

This section formalizes the Google Sheets structure to act as a relational database, addressing key requirements like history tracking and relationships.

Prompt 2.1: Generate the Master Schema Service (SchemaService.gs)

Act as a senior software architect. Analyze the SHEET_NAMES and SHEET_HEADERS constants within the CreateMissingSheets.gs and SchemaService.gs sections of the provided SIG-TE.txt file. Generate a complete SchemaService.gs file in Google Apps Script.

Rationale: This service will be the single source of truth for the application's data contract. It centralizes all sheet names, headers, data types, and validation rules, making the application robust and easier to maintain.

Requirements:

SHEET_NAMES: Consolidate all sheet names from the source file into a single constant.

SCHEMAS: For each primary entity (e.g., Aluno, Rota, Onibus), create a schema object defining each field with:

type: (e.g., 'string', 'number', 'date', 'boolean', 'cpf', 'phone', 'email').

required: true or false.

label: A user-friendly name for UI forms.

defaultValue: A default value for new records.

validation: An object for special validation rules (e.g., { readonly: true }).

ENTITY_TO_SHEET: Create a mapping from the logical entity name (e.g., Aluno) to its corresponding sheet name constant (e.g., SHEET_NAMES.ALUNOS).

FIELD_ALIASES: Create a mapping to resolve discrepancies between logical schema field names and the actual headers in the Google Sheet (e.g., logical CPF maps to sheet header CPF_Aluno).

Helper Functions: Include functions like getSchema(entityName), getSheetName(entityName), and getSheetHeaders(sheetKey).

Section 3: Backend Development (Google Apps Script Services)

This section generates the core logic of the application, translating the services found in SIG-TE.txt into robust, modular Apps Script files.

Prompt 3.1: Generate Core Data and Validation Services

Act as a lead backend developer. Using the SchemaService.gs as a data contract, generate the following core service files:

DataManager.gs: A generic CRUD (Create, Read, Update, Delete) service that interacts with the Google Sheet.

Rationale: Centralizes all spreadsheet interactions, making the code DRY and easier to debug. It should handle header mapping and data type conversions automatically based on the SchemaService.

Features:

getByEntity(entityName, options): Fetches data with support for filtering, sorting, and pagination.

getById(entityName, id): Fetches a single record.

create(entityName, data): Creates a new record, performing pre-validation checks.

update(entityName, id, data): Updates an existing record.

delete(entityName, id): Implements a soft delete by setting an Ativo or Status column to INATIVO.

History Tracking: When updating or deleting, this service must automatically create a corresponding entry in a [SheetName]_History sheet, logging the old data, the user who made the change, and a timestamp.

ValidationService.gs: A service for server-side data validation.

Rationale: Ensures data integrity before it's written to the sheet, enforcing business rules defined in the schema.

Features:

validateEntityData(entityName, data): Validates an entire data object against its schema from SchemaService.

Includes specific validators for Brazilian types like CPF (validateCPF) and phone numbers.

Prompt 3.2: Generate Authentication & Authorization Service (AuthService.gs)

Act as a security specialist. Generate an AuthService.gs file to manage user authentication and permissions.

Rationale: Secures the application by ensuring only authorized users can access and modify data.

Features:

Authentication:

authenticate(googleToken): A function that verifies a Google ID token from the frontend.

On successful verification, it checks if the user's email exists in the Secretários or Monitores sheet to determine their role.

Authorization:

hasPermission(user, requiredPermission): Checks if a user object (containing their role) has the necessary permission for an action.

Password Recovery (for local accounts, if any):

initiatePasswordRecovery(email): Generates a secure, single-use token, stores it with an expiry, and sends a recovery email.

resetPassword(token, newPassword): Validates the token and updates the user's password.

Prompt 3.3: Generate Business Logic and AI Services

Act as a senior developer. Translate the logic from the SIG-TE.txt file into the following modular service files. Each service should be self-contained and use DataManager for data access.

CriticalRoutesService.gs: Implements analyzeCriticalRoutes to identify routes with high occupancy.

AbsenceAnalysisService.gs: Implements analyzeAbsencePatterns to identify students at risk.

NotificationService.gs: Implements createNotification and proactive checks like checkPendingAttestations.

GeminiReportService.gs: Implements generateDiagnosticReport and other report-generation functions by building prompts and calling the GeminiService.

GeminiService.gs: A low-level wrapper for the Gemini 2.5 Flash API. It should handle API key management (from Script Properties), request construction, and response parsing. Include caching (CacheService) to reduce costs.

GoogleMapsService.gs: A wrapper for the Google Maps API, handling API key management and requests for geocoding and route optimization.

Section 4: Frontend Development (HTML, CSS, JavaScript)

This section builds the user-facing Single-Page Application (SPA).

Prompt 4.1: Generate the Main HTML and CSS Files

Act as a UI/UX designer and frontend developer. Generate the following files:

index.html: The main entry point for the SPA.

Rationale: This file will contain the core HTML structure, including placeholders for the header, sidebar navigation, main content area, and modals. It will load all necessary CSS and JavaScript.

Structure:

A main container (<div class="app-container">).

A header with the app title and user profile area.

A collapsible sidebar for navigation (<nav class="main-nav">).

A main content area (<main id="main-content">) where sections will be dynamically rendered.

A container for notifications.

styles.css: A modern and professional stylesheet.

Rationale: Defines a consistent visual identity for the "high-standard corporate SaaS." It should be responsive and include styles for all components (forms, tables, cards, dashboards). Use CSS variables for easy theming. Reference the provided CSS files in SIG-TE.txt for style inspiration.

Prompt 4.2: Generate the Core Frontend JavaScript (main.js)

Act as a senior frontend developer. Generate the main JavaScript file that controls the SPA's logic.

Rationale: This script will manage navigation, state, and dynamic content rendering, creating a fluid user experience without page reloads.

Features:

Router: A simple hash-based router to show/hide content sections (e.g., #/dashboard, #/alunos).

API Client: A wrapper around google.script.run to communicate with the backend services. It should include error handling and display loading indicators.

UI Manager: Functions to show/hide loading states, display notifications, and manage modals.

Dynamic Rendering:

renderDashboard(data): Renders dashboard cards and charts (using Chart.js).

renderDataTable(entityName, data): Renders a data table with headers, rows, and action buttons. Must include client-side sorting and pagination.

renderForm(entityName): Fetches the schema for an entity using SchemaService.getSchema and dynamically builds an HTML form with correct input types and validation attributes.

Section 5: Deployment

This final section provides instructions for deploying the application.

Prompt 5.1: Generate Deployment Instructions (README.md)

Act as a DevOps engineer. Generate a README.md file with clear, step-by-step instructions for deploying the SIG-TE application.

Rationale: Clear documentation is essential for maintainability and onboarding new developers.

Instructions to Include:

Prerequisites: Installing clasp (the command-line tool for Apps Script).

Setup:

Cloning the repository.

Running clasp login.

Running clasp create or clasp push to upload the files to a new Google Apps Script project.

Configuration:

How to set required Script Properties (e.g., GEMINI_API_KEY, GOOGLE_MAPS_API_KEY).

How to find and configure the Google Sheet ID in SchemaService.gs.

Deployment:

How to deploy the project as a Web App using clasp deploy.

How to set up the time-based triggers by running the createAllTriggers function from the Apps Script editor.
