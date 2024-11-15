EventAPI
EventAPI is a Django-based RESTful API for managing events, with role-based access control and JWT-based authentication. The system allows admins to create events and users to purchase tickets, ensuring secure operations and scalability.
________________________________________
Features
•	User Registration and Authentication:
o	JWT-based login system.
o	Role-based access control (Admin/User).
•	Event Management:
o	Admins can create and manage events.
o	Users can view events and purchase tickets.
•	Ticket Purchasing:
o	Users can purchase tickets for events.
o	Validation to ensure requested tickets do not exceed availability.
•	Custom SQL Query:
o	Fetch top 3 events by tickets sold for analytics.
________________________________________
Project Setup
Prerequisites
•	Python 3.8+
•	Django 4.0+
•	PostgreSQL or MySQL
•	Virtual Environment (recommended)
Installation Steps
1.	Clone the repository:
git clone <repository_url>
cd EventAPI
2.	Set up a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3.	Install dependencies:
pip install -r requirements.txt
4.	Configure the database:
o	Update DATABASES in EventAPI/settings.py with your database credentials.
5.	Run migrations:
python manage.py makemigrations
python manage.py migrate
6.	Create a superuser:
python manage.py createsuperuser
7.	Start the development server:

python manage.py runserver
________________________________________
API Endpoints
User Authentication
•	Login (Token Obtain):
POST /api/token/
Request Body:
{
    "username": "user",
    "password": "password"
}
•	Token Refresh:
POST /api/token/refresh/
Request Body:
{
    "refresh": "your_refresh_token"
}
User Management
•	Register a User:
POST /api/register/
Request Body:
{
    "username": "user",
    "password": "password",
    "role": "Admin"  # or "User"
}
Event Management
•	Create an Event (Admin Only):
POST /api/events/
Request Body:
{
    "name": "Event Name",
    "date": "YYYY-MM-DD",
    "total_tickets": 100
}
•	View All Events:
GET /api/events/
Ticket Purchasing
•	Purchase Tickets:
POST /api/events/{id}/purchase/
Request Body:
{
    "quantity": 2
}
Analytics
•	Top 3 Events by Tickets Sold:
GET /api/events/top-selling/
________________________________________
Custom SQL Query
The following query fetches the top 3 events by tickets sold:
SELECT id, name, date, total_tickets, tickets_sold
FROM events_event
ORDER BY tickets_sold DESC
LIMIT 3;
________________________________________
Project Structure
EventAPI/
├── events/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
├── EventAPI/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── manage.py
├── requirements.txt
└── README.md
________________________________________
Testing the API
1.	Use tools like Postman or cURL to test API endpoints.
2.	Include the Authorization header with the JWT token for authenticated requests:
Authorization: Bearer <your_access_token>
________________________________________
Notes
•	Ensure the database is running before starting the server.
•	For deployment, use production-ready settings (e.g., configure ALLOWED_HOSTS, secure SECRET_KEY, etc.).
•	Use Docker for containerized deployment.
________________________________________
Contributing
Feel free to open issues or submit pull requests to improve this project. Contributions are welcome!
________________________________________
License
This project is licensed under the MIT License. See the LICENSE file for details.
