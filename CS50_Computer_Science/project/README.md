# YustePickle Club Management System

#### Video Demo:  [https://youtu.be/coRY6DcPywY]

## Description:

The **YustePickle Club Management System** is a web-based application designed to help manage a pickleball club. Built using Python, Flask, and SQLite, the application allows users to register, log in, book pickleball courts, and view their booking history. Administrators have special privileges to manage court reservations, edit user bookings, and oversee club activities.

This project aims to streamline the process of managing court reservations, providing an intuitive platform where users can book courts, and administrators can oversee the club’s operations with ease. The application is designed with security in mind, using hashed passwords for user accounts, and it includes dynamic elements like real-time court availability, restricted booking slots, and a polished user interface with CSS and Bootstrap.

### Features

1. **User Registration and Login**: Users can create an account, log in, and log out securely. Passwords are hashed to ensure user security, and the session management is handled via Flask.

2. **Court Reservation**: Users can book courts by selecting a specific date and time, ensuring they have access to the courts. The system prevents double-booking by checking existing reservations and blocking off reserved times for a full hour.

3. **Booking History**: Users can view their past bookings in a detailed history page. They also have the ability to cancel their bookings directly from the history section if needed.

4. **Admin Panel**: Administrators have access to a special panel where they can view all court reservations made by any user. From this panel, admins can modify or delete reservations, making it easy to manage bookings and resolve conflicts.

5. **Dynamic Time Blocking**: When a user books a court, the system automatically blocks off that time slot for one hour, ensuring that no other user can book the same court during the same time. This is handled with datetime logic that verifies court availability.

6. **Responsive Design**: The application uses Bootstrap for a modern, responsive design. All pages are optimized for both desktop and mobile devices, ensuring a smooth user experience across platforms.

7. **About Us Page**: A dedicated "About Us" page provides information about the club, including its mission, values, and the services it offers. The page features the YustePickle logo prominently and outlines the club’s goal of fostering a vibrant pickleball community.

8. **Notifications**: When users make a booking, they are shown confirmation pop-ups to ensure that the booking was successful. In case the court is already booked, users receive real-time notifications explaining the issue.

9. **Custom Logo and Branding**: The application features a custom-designed logo for YustePickle, which is displayed prominently on all pages, including the navigation bar and as a favicon.

### How the Project Works

Upon accessing the site, users can log in or register for a new account. Once logged in, they are presented with the option to book a pickleball court. The user selects a date and time from a dropdown menu that includes preset options for both the hour and minute, ensuring valid entries for time slots.

The system prevents double bookings by checking if the selected court is already reserved for that specific time. If the court is available, the reservation is confirmed, and the user receives a confirmation message. If not, the user is notified via a pop-up message, informing them that the court is unavailable.

Users can view all their bookings under the "History" tab, where they have the option to cancel upcoming reservations if needed. Administrators can access the "Admin Panel" to view and manage all club reservations, with the ability to modify or delete any booking. This ensures that the club can handle multiple users and avoid booking conflicts efficiently.

The layout and design of the web application are enhanced with Bootstrap, providing a clean and modern user interface. The use of CSS customizations allows for a unique look and feel, incorporating the club's branding.

### Files

- `app.py`: The core of the application. This file handles routing, form submissions, session management, and database interactions. It contains routes for user authentication, court booking, and admin functions.

- `templates/`: This directory contains all HTML templates used in the project. Key templates include:
  - `layout.html`: The base template, which includes the navigation bar and footer used on all pages.
  - `index.html`: The homepage template where users can navigate to book courts or view their history.
  - `about.html`: The "About Us" page that provides information about the club.
  - `reservation.html`: The court booking page where users can select a court, date, and time.
  - `history.html`: The booking history page where users can view and cancel their reservations.
  - `admin.html`: The admin panel for managing all reservations.

- `static/styles.css`: Custom CSS file for styling the web application. This file enhances the look of forms, buttons, tables, and general layout to match the club’s branding.

- `static/logo.png`: The custom YustePickle logo used throughout the site, including in the navbar and as a favicon.

- `finance.db`: The SQLite database that stores user information, hashed passwords, and all court reservations.

### Design Choices

1. **Blocking Time Slots**: The decision to block courts for one hour when a reservation is made ensures fairness and prevents double bookings. This was implemented using datetime logic and SQL queries that check if a court is available for the selected time.

2. **Pop-up Notifications**: To enhance user experience, pop-up notifications were added to confirm reservations or notify users when a booking conflict occurs. This feature makes the site more interactive and user-friendly.

3. **Administrator Privileges**: Admins have the ability to edit and delete any reservation. This feature was designed to ensure flexibility in case of mistakes or conflicts, giving the club management full control over the court schedules.

4. **Styling and Branding**: The use of Bootstrap along with custom CSS ensured that the application not only functions well but also looks professional. The club’s branding is reinforced through the logo and consistent color scheme across all pages.

### Conclusion

The **YustePickle Club Management System** is a complete web solution for managing pickleball court bookings, user registrations, and administrative tasks. With a secure login system, dynamic court reservation functionality, and a polished user interface, this project provides all the tools necessary for effectively managing a pickleball club. Future improvements could include adding a payment system for reservations or integrating a notification system via email. However, the current implementation offers a robust and scalable solution that meets the immediate needs of a growing club.
