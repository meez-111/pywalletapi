
# Django REST API for a Secure Digital Wallet

This project is a robust and secure backend API for a personal digital wallet, built with **Django** and **Django REST Framework**. It allows users to manage their financial accounts, track income and expenses, and transfer funds between users.

This project demonstrates core skills in backend development, including API design, database management, and a focus on data integrity and security.

-----

## Key Features

  * **User Management**: Secure user registration, authentication, and profile management.
  * **Multi-Account Support**: Users can create and manage multiple financial accounts.
  * **Transaction Tracking**: Record income and expenses for each account.
  * **Inter-User Transfers**: Securely transfer funds between different user accounts.
  * **Categorization**: Categorize transactions for better financial tracking.
  * **Data Integrity**: All transfers are handled within a database transaction to ensure atomicity and prevent inconsistencies.

-----

## Architectural Design

The project is built on the **Model-View-Controller (MVC)** pattern, implemented through Django and Django REST Framework.

  * **Models**: Define the database schema for users, accounts, transactions, and categories.
  * **Serializers**: Handle the conversion of complex data types (model instances) into native Python data types that can be easily rendered into JSON.
  * **ViewSets**: Provide the API logic, combining the functionality of a view with the convenience of a router.
  * **Permissions**: Control access to API endpoints to ensure data security and user privacy.

-----

## Technology Stack

  * **Backend Framework**: Django, Django REST Framework
  * **Language**: Python 3.x
  * **Database**: SQLite
  * **Package Management**: pip

-----

## Getting Started

These instructions will get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

  * Python 3.8+
  * pip (Python package installer)

### Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/meez-111/pywalletapi.git
    cd pywalletapi
    ```

2.  Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  Install dependencies:
    You will need to install `drf-yasg` and `gunicorn`.

    ```bash
    pip install -r requirements.txt
    ```

4.  Set up the database:
    Create a `.env` file or set environment variables for your database configuration.
    Then, apply database migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  Run the development server:

    ```bash
    python manage.py runserver
    ```

    The API will be available at `http://127.0.0.1:8000/`.

-----

## API Documentation

This project includes live, interactive API documentation using **Swagger/OpenAPI**, which can be viewed at the following endpoints after starting the server:

  * **Swagger UI**: `http://127.0.0.1:8000/api/swagger/`
  * **Redoc UI**: `http://127.0.0.1:8000/api/redoc/`

-----

## Deployment to Render

You can easily deploy this project to a production environment using a platform like **Render.com**.

1.  **Create a New Web Service**:
    Log in to Render and create a new Web Service.
    Connect your GitHub repository where this project is hosted.

2.  **Configure Build and Start Commands**:

      * **Build Command**: `pip install -r requirements.txt`
      * **Start Command**: `gunicorn my_project.wsgi` (Replace `my_project` with your project's root folder name).

3.  **Set Environment Variables**:
    Add your environment variables (e.g., `SECRET_KEY`).
    Render will provide a `DATABASE_URL` for PostgreSQL, which you'll need to configure in your `settings.py` file.

4.  **Run Database Migrations**:
    After your first successful deployment, you'll need to run your migrations on the server.
    Go to your web service on Render, click the **Shell** tab, and run:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Test Your Live API**:
    After the deployment is complete, Render will provide you with a live URL for your API. You can use this URL to test your endpoints.

-----

## Live Demo

You can interact with a live version of this API at the following URL:

[Pywalletapi live demo](https://pywalletapi.onrender.com/api/schema/swagger-ui/)

-----

## API Endpoints

The following are the main API endpoints for the project.

### 1\. User Management

| Method     | Endpoint       | Description                |
| :--------- | :------------- | :------------------------- |
| **POST**   | `/users/`      | Create a new user account. |
| **GET**    | `/users/{id}/` | Retrieve a user's details. |
| **PATCH**  | `/users/{id}/` | Update user details.       |
| **DELETE** | `/users/{id}/` | Delete a user account.     |

**Example: Create a User**

```json
POST /users/
{
  "username": "jane_doe",
  "password": "strong_password123",
  "email": "jane@example.com"
}
```

### 2\. Account Management

*Requires authentication.*

| Method   | Endpoint          | Description                                   |
| :------- | :---------------- | :-------------------------------------------- |
| **GET**  | `/accounts/`      | List all accounts for the authenticated user. |
| **POST** | `/accounts/`      | Create a new account.                         |
| **GET**  | `/accounts/{id}/` | Retrieve a specific account.                  |

**Example: Create an Account**

```json
POST /accounts/
{
  "account_name": "Savings Account",
}
```

### 3\. Transaction Management

*Requires authentication.*

| Method   | Endpoint         | Description                                       |
| :------- | :--------------- | :------------------------------------------------ |
| **GET**  | `/transactions/` | List all transactions for the authenticated user. |
| **POST** | `/transactions/` | Create a new income or expense transaction.       |

**Example: Create a Transaction**

```json
POST /transactions/
{
  "account": 1,
  "transaction_type": "expense",
  "transaction_amount": 50.25,
  "transaction_description": "Lunch with a friend",
  "transaction_category": 3
}
```

### 4\. Transfers

*Requires authentication. This is a custom action on the `TransactionViewSet`.*

| Method   | Endpoint                  | Description                               |
| :------- | :------------------------ | :---------------------------------------- |
| **POST** | `/transactions/transfer/` | Transfer funds between two user accounts. |

**Example: Transfer Funds**

```json
POST /transactions/transfer/
{
  "sender_account": 1,
  "recipient_username": "john_doe",
  "recipient_account": 2,
  "transaction_amount": 75.00
}
```

-----

## How to Contribute

We welcome contributions\! If you have suggestions or want to fix a bug, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes and write tests.
4.  Commit your changes (`git commit -m 'Add a new feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Create a new Pull Request.

-----

## Future Enhancements

  * **Budgeting**: Implement a budgeting feature to help users monitor their spending against a set limit.
  * **API Enhancements**: Add filtering and sorting to the transactions endpoint.
  * **Two-Factor Authentication (2FA)**: Integrate a secure 2FA system to enhance user security.

-----


## Author

Email: [Email](meez.sabra.111@gmail.com)

LinkedIn: [LinkedIn](https://www.linkedin.com/in/moaz-sabra-3a7565330/)