# Deployment Instructions for IUT Orsay Internship Portal

## Prerequisites
Before deploying the application, ensure you have the following installed:
- Python 3.x
- pip
- Docker and Docker Compose (if using containerization)
- Git

## Setting Up the Environment
1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd iut-orsay-internship-portal
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Database Setup
1. **Migrate the Database**
   ```bash
   python manage.py migrate
   ```

2. **Load Demo Data (Optional)**
   If you want to load demo data, run:
   ```bash
   python manage.py loaddata fixtures/demo_data.json
   ```

## Running the Application
### Option 1: Using Django Development Server
1. **Run the Server**
   ```bash
   python manage.py runserver
   ```

2. **Access the Application**
   Open your web browser and go to `http://127.0.0.1:8000`.

### Option 2: Using Docker
1. **Build the Docker Image**
   ```bash
   docker-compose build
   ```

2. **Run the Application**
   ```bash
   docker-compose up
   ```

3. **Access the Application**
   Open your web browser and go to `http://localhost:8000`.

## Additional Configuration
- Ensure that your `settings.py` file is configured for production, including allowed hosts and database settings.
- Set up a production-ready database (e.g., PostgreSQL) if necessary.

## Stopping the Application
- If running with Docker, you can stop the application with:
  ```bash
  docker-compose down
  ```

## Conclusion
You have successfully deployed the IUT Orsay Internship Portal. For further customization and development, refer to the developer guide in the `docs` directory.