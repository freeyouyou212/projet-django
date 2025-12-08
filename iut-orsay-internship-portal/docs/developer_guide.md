# Developer Guide for IUT Orsay Internship Portal

## Introduction
This document serves as a guide for developers working on the IUT Orsay Internship Portal project. It outlines the project structure, coding standards, and best practices to follow while contributing to the application.

## Project Structure
The project is organized into several directories and files, each serving a specific purpose:

- **manage.py**: Command-line utility for managing the Django project.
- **requirements.txt**: Lists the required Python packages.
- **README.md**: Documentation about the project.
- **.gitignore**: Specifies files to be ignored by Git.
- **.gitlab-ci.yml**: Configuration for GitLab CI/CD.
- **Dockerfile**: Instructions for building a Docker image.
- **docker-compose.yml**: Defines services for Docker Compose.
- **iut_portal/**: Contains the main Django project files.
- **apps/**: Contains individual Django apps for offers, accounts, dashboard, and API.
- **templates/**: Contains HTML templates for rendering views.
- **static/**: Contains static files such as CSS and JavaScript.
- **fixtures/**: Contains demo data for testing and development.
- **docs/**: Contains documentation files.

## Coding Standards
- Follow PEP 8 guidelines for Python code.
- Use meaningful variable and function names.
- Write clear and concise comments to explain complex logic.
- Maintain consistent indentation and spacing.

## Best Practices
- Use Django's built-in features for authentication and authorization.
- Validate user input in forms to prevent security vulnerabilities.
- Implement error handling to manage exceptions gracefully.
- Write unit tests for critical functionality to ensure code reliability.
- Keep the code modular by separating concerns into different files and functions.

## Development Setup
1. Clone the repository from GitLab.
2. Create a virtual environment and activate it.
3. Install the required packages using `pip install -r requirements.txt`.
4. Run database migrations with `python manage.py migrate`.
5. Start the development server using `python manage.py runserver`.

## Contribution Guidelines
- Create a new branch for each feature or bug fix.
- Write clear commit messages that describe the changes made.
- Submit a merge request for review before merging into the main branch.

## Conclusion
By following this developer guide, you will contribute to a well-structured and maintainable codebase for the IUT Orsay Internship Portal. Happy coding!