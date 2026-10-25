# Digital-Exeat
```markdown
# Digital Exeat

### A Digital School Exeat Management Platform

Digital Exeat is a web-based school management platform designed to modernize the exeat application and approval process for middle schools, senior high schools, and other educational institutions in Ghana.

The platform aims to replace manual, paper-based exeat procedures with a secure, centralized digital system that helps schools manage student departures, parental requests, approvals, and expected return times.

---

## Overview

Digital Exeat provides a structured environment where schools can register their institutions, receive administrative approval, and manage their exeat processes through a digital dashboard.

The platform is being developed with security, simplicity, and school-specific data management in mind.

## Key Features

### 1. School Registration
- Schools can submit their institutional details online.
- School administrators can create an administrator account during registration.
- Each new school registration requires platform administrator approval.
- Schools cannot access their management dashboard until approved.

### 2. School Approval
- Platform administrators can review school registrations.
- Registrations can be approved or rejected.
- Rejection reasons can be recorded for reference.

### 3. School Dashboard
- Approved school administrators can access their school dashboard.
- The dashboard provides the foundation for managing school-specific operations.
- Additional management features can be developed as the platform evolves.

### 4. Student Management
Planned functionality includes:
- Registering and maintaining student records.
- Organizing students by class or other school-defined categories.
- Connecting students to their respective schools.

### 5. Parent and Guardian Exeat Applications
Planned functionality includes:
- Allowing parents or guardians to submit exeat requests.
- Recording the purpose and destination of an exeat.
- Recording departure and expected return dates and times.
- Allowing authorized school personnel to review requests.

### 6. Exeat Monitoring
Planned functionality includes:
- Tracking the status of exeat applications.
- Recording approval decisions.
- Helping schools monitor expected student return times.

---

## Technology Stack

The project currently uses or is designed around the following technologies:

- **Backend:** Python and Django
- **Frontend:** HTML and CSS
- **Database:** Django-supported databases; production database configuration depends on deployment
- **Administration:** Django Admin with django-unfold
- **Version Control:** Git and GitHub
- **Deployment:** Render

Additional technologies may be introduced as development progresses.

---

## Project Structure

The project is organized as a Django application.

```text
digitalexeat/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── digitalexeat/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── schools/
    ├── migrations/
    ├── templates/
    │   └── schools/
    ├── models.py
    ├── forms.py
    ├── views.py
    ├── urls.py
    └── admin.py
```

*Note: This structure illustrates the main files and may change as new applications and features are added.*

---

## Getting Started

Follow these instructions to run the project locally.

### Prerequisites

Install the following:

- Python compatible with the project's dependencies
- Git
- pip
- A terminal or command-line application

### 1. Clone the Repository

Replace the repository URL below with the actual GitHub repository URL.

```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/Digital-Exeat.git
```

Navigate to the project directory:

```bash
cd Digital-Exeat
```

If your Django project is inside a nested `digitalexeat` directory, navigate into that directory before running Django commands.

### 2. Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the environment's Python executable directly instead.

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a local `.env` file if the project's settings are configured to read environment variables from it.

Example:

```dotenv
SECRET_KEY=replace-with-a-local-development-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

These are illustrative values. Configure the variables to match the project's actual settings.

**Security notice:** Never commit real secret keys, passwords, API credentials, or production environment variables to GitHub.

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Create a Django Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an administrative account.

### 7. Start the Development Server

```bash
python manage.py runserver
```

Open the local development site:

http://127.0.0.1:8000/

The Django administration interface is available at:

http://127.0.0.1:8000/admin/

---

## School Registration and Approval Workflow

The current school registration workflow is designed as follows:

1. A school administrator opens the registration page.
2. The administrator submits the school's details and account information.
3. The system creates the school record with a pending approval status.
4. A platform administrator reviews the application.
5. The platform administrator approves or rejects the registration.
6. Approved school administrators can access their school dashboard.
7. Rejected applications display the recorded rejection reason where available.

Approval is required before a school administrator can access the approved school's management dashboard.

---

## Security Considerations

Security is an important part of the platform's development.

The project should maintain the following protections:

- CSRF protection for forms that modify data.
- Secure password handling through Django's authentication system.
- Environment-based configuration for production secrets.
- Appropriate access controls for school administrators.
- School-specific data access restrictions.
- HTTPS in production.
- `DEBUG=False` in production.
- Restricted and validated administrative actions.

Before production use, verify that every school-specific view and database query enforces appropriate authorization and prevents one school from accessing another school's records.

---

## Deployment

The application can be deployed to Render using a connected GitHub repository.

A typical deployment process involves:

1. Push the project to GitHub.
2. Create or open the Render web service.
3. Connect the correct GitHub repository and deployment branch.
4. Install dependencies from `requirements.txt`.
5. Configure production environment variables.
6. Configure a supported production database if required.
7. Apply database migrations.
8. Collect static files.
9. Start the Django application using Gunicorn.
10. Review deployment logs and test the live application.

Example start command, assuming the Django settings package is named `digitalexeat`:

```bash
gunicorn digitalexeat.wsgi:application
```

The actual build and start commands must match the project's configuration. Production deployments should use a persistent database and a suitable static-file serving strategy.

For deployment documentation, consult the official [Render documentation](https://render.com/docs).

---

## Development Status

Digital Exeat is under active development.

| Component | Status |
|---|---|
| Django project setup | Implemented |
| School registration form | Implemented |
| School approval status | Implemented |
| Administrative school review | Implemented |
| Pending approval page | Implemented |
| Rejected registration page | Implemented |
| Approved school dashboard foundation | Implemented |
| Student management | Planned / ongoing |
| Parent and guardian accounts | Planned / ongoing |
| Exeat application workflow | Planned / ongoing |
| Exeat approval and monitoring | Planned / ongoing |
| Additional notifications and reporting | Planned |

*The status table should be updated as features are completed and tested.*

---

## Contributing

Contributions, suggestions, and bug reports are welcome.

To contribute:

1. Fork the repository or create a development branch.
2. Make your changes.
3. Test your changes locally.
4. Commit your work with a descriptive message.
5. Submit a pull request or share your proposed changes with the project maintainer.

Please avoid committing secrets, local databases, virtual environments, or generated deployment files.

---

## Future Improvements

Potential future improvements include:

- Parent and guardian account management.
- Student record management.
- Digital exeat applications and approvals.
- Student departure and expected-return tracking.
- Email or other notification integrations.
- School-level reporting and analytics.
- Improved mobile accessibility.
- Stronger automated tests and monitoring.

---

## License

A license has not yet been specified for this project.

Until a license is added, permission to reuse, distribute, or modify this project's code should not be assumed.

---

## Acknowledgements

Digital Exeat is being developed to support the modernization of school administration and student exeat management through accessible digital technology.
```

## Save it and push it to GitHub

After saving `README.md`, open PowerShell in your project directory and run:

```powershell
git add README.md .gitignore
git status
git commit -m "Add project README and gitignore"
git push
```

These commands assume you have already configured your GitHub remote and are on a branch with an upstream configured. If Git reports that no upstream exists, use the appropriate `git push -u origin <branch-name>` command.

### Before deploying to Render

After GitHub receives the commit, Render can deploy the updated repository. If automatic deployments are enabled, the deployment may start automatically; otherwise, trigger **Manual Deploy → Deploy latest commit** in your Render service.

**One important detail:** The README describes some features as planned rather than completed, so it does not claim that the entire exeat workflow is already operational. Update the development-status table as you finish and test those features.
