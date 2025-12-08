# IUT d'Orsay Internship Portal

## Overview
The IUT d'Orsay Internship Portal is a web application designed to facilitate the management of internship offers and applications. The application allows companies to post internship offers, enables students to apply for these offers, and provides administrators and stage managers with tools to manage and validate these offers.

## Technologies Used
- **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **Bootstrap**: A front-end framework for developing responsive and mobile-first websites.
- **Chart.js**: A JavaScript library for creating beautiful charts and graphs.

## Features
- **For Companies**:
  - Submit internship offers without the need for authentication.
  
- **For Stage Managers**:
  - View and manage internship offers.
  - Validate or reject offers.
  - Search through offers.

- **For Students**:
  - Browse available internship offers.
  - Apply for offers (limited to 5 applications per offer).
  
- **For Administrators**:
  - Access a dashboard with statistics on offers and applications.
  - Manage all aspects of the internship offers.

## Setup Instructions
1. **Clone the Repository**:
   ```
   git clone <repository-url>
   cd iut-orsay-internship-portal
   ```

2. **Install Dependencies**:
   Ensure you have Python and pip installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Run Migrations**:
   ```
   python manage.py migrate
   ```

4. **Create a Superuser** (for admin access):
   ```
   python manage.py createsuperuser
   ```

5. **Run the Development Server**:
   ```
   python manage.py runserver
   ```

6. **Access the Application**:
   Open your web browser and go to `http://127.0.0.1:8000`.

## Usage
- Navigate to the appropriate section based on your user role (Company, Stage Manager, Student, Administrator).
- Follow the prompts to submit offers, apply for internships, or manage the application process.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# iut-orsay-internship-portal

Quick start:

1. Create venv and install deps
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt

2. Run migrations and create superuser
   python manage.py migrate
   python manage.py createsuperuser

3. Load fixture (ensure file is UTF-8)
   python manage.py loaddata fixtures/initial_data.json

4. Run local server
   python manage.py runserver

Optional: Docker
   docker-compose build
   docker-compose up -d

Run tests:
   python manage.py test