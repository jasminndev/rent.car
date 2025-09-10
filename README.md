# 🚘 RentCar: Your Ultimate Car Rental Platform 🚘

### Welcome to RentCar, a dynamic and innovative car rental platform that seamlessly integrates a Django REST Framework backend with a powerful Telegram bot, all unified by a single shared PostgreSQL database. Whether you're renting a car through the web or chatting with our bot, RentCar delivers a smooth, modern, and user-friendly experience.

### 🌟 Project Overview

### RentCar is designed to simplify the car rental process by combining a robust web API with an interactive Telegram bot. From browsing available cars to completing a rental, users can interact with the platform through multiple channels, while admins enjoy full control over the system's features. The platform is built for scalability, real-time updates, and a delightful user experience.

--- 

### 🔑 Core Features

#### User Authentication

###### Secure Registration & Login: Users can sign up and log in via email with JWT-based authentication.

###### Email Verification: Powered by Celery for asynchronous email delivery to ensure a smooth onboarding process.

---

#### Car Management

##### Admin Control: Admins can create, update, or delete cars via the Django REST API.

##### Automated Telegram Updates: New cars are instantly posted to the RentCar Telegram channel with vibrant photos and details. Updates to cars in the API are reflected in real-time on the channel.

---

#### Categories, Regions, & Districts

##### Full CRUD Operations: Admins can manage car categories, regions, and districts through intuitive API endpoints, ensuring organized and localized car listings.

---

#### Telegram Bot Integration

##### Interactive Experience: Each car post in the Telegram channel includes a "More Information" button that redirects users to the bot.

##### Rich Details: The bot displays additional car photos, detailed specs, and inline buttons for renting directly.

##### Real-Time Sync: All bot interactions sync seamlessly with the web platform via the shared database.

---

#### Rental Orders

##### Unified System: Rentals initiated via the web or bot are stored in a single, cohesive system for streamlined management.

##### User-Friendly Process: Renting is as easy as a few clicks, whether on the website or through the Telegram bot.

--- 

#### Wishlist

##### Save Favorites: Users can add cars to their wishlist for quick access later, enhancing the browsing experience.

---

#### Reviews

##### User Feedback: Customers can leave reviews for cars, helping others make informed rental decisions.

---

#### Payments

##### Flexible Options: Pay with cash at pickup or use secure card payments directly within the Telegram bot.

#####Seamless Integration: Card payments are processed efficiently, ensuring a hassle-free transaction.

---

#### 📊 Statistics & Insights

##### Top 5 Cars: Automatically calculated based on rental popularity across both web and bot platforms.

##### Recent Transactions: A unified dashboard displays all orders, providing admins with a clear overview of activity.

---

#### ⚙️ Tech Stack

##### RentCar is built with modern, reliable technologies to ensure performance, scalability, and maintainability:

##### Django REST Framework: Powers the robust and secure API for web interactions.

##### PostgreSQL: A shared database for consistent data across web and bot platforms.

##### Celery: Handles asynchronous tasks like email verification and background processing.

##### JWT Authentication: Ensures secure user sessions.

##### Telegram Bot API: Enables real-time interaction and automation for a seamless user experience.

---

### 🚀 Getting Started

#### Install Dependencies:

```
pip install -r requirements.txt
```

#### Set Up Environment:

##### Configure PostgreSQL and update database settings in settings.py.

#### Set up Celery for async tasks.

##### Add your Telegram Bot Token and channel details.

#### Run the Application:

```
python manage.py runserver
```

---

### Explore the Bot: Connect to the RentCar Telegram bot to experience real-time car browsing and rentals.

--- 

### 👀 Why RentCar?

##### RentCar stands out by blending cutting-edge API technology with the accessibility of a Telegram bot. Whether you're a user looking for a quick rental or an admin managing a fleet of cars, RentCar offers:

##### Real-Time Sync: Updates on the web reflect instantly in the Telegram channel.

##### Unified Experience: One database ensures consistency across platforms.

##### Engaging Design: Interactive bot features and a sleek web interface make renting fun and easy.

---

### Issues & Contributions: Found a bug or want to contribute? Open an issue or submit a pull request!

### Contact: Reach out via the Telegram bot or GitHub for support and feedback.

---

### 🌍 Future Plans

##### Mobile App: Expand RentCar with dedicated iOS and Android apps.

##### Advanced Analytics: Introduce more detailed insights for admins, like user behavior and rental trends.

##### Multi-Language Support: Make the platform accessible to a global audience.

##### AI Recommendations: Suggest cars based on user preferences and rental history.

##### RentCar is more than just a car rental platform—it's a modern, connected experience that brings convenience and excitement to every journey. Hop in and explore the ride! 🚗💨

---

### 👩‍💻 Author

**Made with 🧡 by Jasmina Ochildiyeva**

[🔗 My GitHub profile](https://github.com/itsjasminn)

[📂 RentCar Repository](https://github.com/itsjasminn/RentCar)
