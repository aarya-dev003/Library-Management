# Library Management System

## Project Overview

The **Library Management System** is a web-based application designed to manage various aspects of a library, such as book borrowing, user management, and admin functionalities. The system allows librarians to manage book inventory, users to request books, and provides a seamless experience for both users and administrators.

### Features:
- **Book Borrowing System**: Users can request to borrow books, and librarians can approve or reject requests.
- **Admin Panel**: A fully-featured admin panel for managing books, borrow requests, and user accounts.
- **User History**: Users can view their borrowing history, and librarians can view the borrowing history of users.
- **Role-Based Access Control (RBAC)**: Different roles (user, librarian) with specific permissions.

---

## Technologies Used

- **Backend**: 
  - **FastAPI**: A modern web framework for building APIs with Python 3.7+ based on standard Python type hints.
  - **SQLAlchemy**: ORM for interacting with the database and managing data models.
  - **PostgreSQL**: A powerful, open-source relational database system used to store all application data.
  - **Alembic**: Database migration tool used to handle database schema changes.

- **Frontend**: 
  - **SQLAdmin**: A UI tool for generating admin panels that simplifies managing database records through a web interface.

  
- **Authentication**: 
  - **OAuth2**: For handling authentication, ensuring secure user access with token-based authentication (JWT).
  
- **Deployment**:
  - **Azure**: Hosting the application and database on Microsoft Azure for cloud deployment and scalability.

---

## Admin Panel

The **Admin Panel** is a key feature of this project, allowing librarians to manage various aspects of the library system effectively. The features of the admin panel include:

- **Manage Books**: Add, update, or remove books from the library inventory.
- **Approve/Reject Borrow Requests**: The librarian can approve or reject book borrowing requests made by users.
- **User Management**: Librarians can view, update, or delete user accounts.
- **Borrowing History**: Librarians can view detailed borrowing history for all users, allowing them to track which books are being borrowed and by whom.

The admin panel is built using **SQLAdmin**, which automatically generates a user-friendly interface for managing the application's models (e.g., books, users, borrow requests) in the database.

---

## User History

- **Users**: Each user has the ability to view their borrowing history, including which books they have borrowed and their current status (approved/rejected). This functionality helps users keep track of their borrowed books and monitor their borrowing limits.
  
- **Librarians**: Librarians can view detailed borrowing histories for each user, giving them insights into the borrow activity in the library and enabling them to make informed decisions regarding book approvals and inventory management.

---

## Role-Based Access Control (RBAC)

RBAC is used in this system to differentiate the permissions and functionalities available to different types of users. There are two primary roles in the system:

1. **User**:
   - **View Books**: Users can view the available books in the library and see details such as title, author, availability, and more.
   - **Request Borrowing**: Users can request to borrow books from the library.
   - **View Borrowing History**: Users can view their borrowing history, including the status of their requests (approved/rejected) and borrowed books.

2. **Librarian**:
   - **Manage Books**: Librarians have the ability to add new books, update existing books, and remove books from the library inventory.
   - **Approve/Reject Borrow Requests**: Librarians can approve or reject borrow requests made by users.
   - **Manage Users**: Librarians can manage user accounts by viewing, updating, or deleting them as necessary.
   - **View Borrowing History**: Librarians can view the borrowing history of any user, including past borrowing activities and the current status of requests.
   - **Admin Panel Access**: Librarians have access to a full admin panel, where they can manage various aspects of the library system, including books, borrow requests, and user accounts.

RBAC ensures that each user type (librarian and user) only has access to the features and actions they are authorized to perform. For example, a user cannot access the admin panel or approve borrow requests, while a librarian has control over the entire system's operations.

---

## How it Works

1. **User Registration**:
   - Users can register through the system with their basic information. After registration, they can start browsing available books and request borrowing.

2. **Borrow Requests**:
   - Users select books they want to borrow, and submit a borrowing request.
   - Librarians can approve or reject these requests through the admin panel.

3. **Approval/Denial Process**:
   - If the librarian approves a borrow request, the book is marked as unavailable.
   - If the librarian rejects a request, the status remains unchanged.

4. **Viewing History**:
   - Users can view their borrowing history under their profile.
   - Librarians can also view users’ histories through the admin panel to keep track of borrowing patterns.

---

## Deployment

The **Library Management System** is deployed and can be accessed through the following URLs:

- **Application**: [http://52.172.9.239:8090/](http://52.172.9.239:8090/)
- **API Documentation**:
  - Swagger: [http://52.172.9.239:8090/docs](http://52.172.9.239:8090/docs)
  - Postman: https://documenter.getpostman.com/view/32664548/2sAYBd67Hu

---
