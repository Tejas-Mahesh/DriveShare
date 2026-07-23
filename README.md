# 🚗 DriveShare - Car Rental & Car Sharing Platform

DriveShare is a full-stack web application developed using **Python Django** that enables users to rent cars, list their own vehicles for rental, and manage bookings through a secure and user-friendly platform.

The system supports three different user roles:

- 👤 Customer
- 🚘 Car Owner
- 👨‍💼 Administrator

---

# 📌 Features

## 👤 Customer

- User Registration & Login
- Email Verification
- Browse Available Cars
- Search Cars
- Wishlist Cars
- Book Cars
- Secure Online Payment (Razorpay)
- Wallet System
- Booking History
- Payment History
- Profile Management
- Upload Aadhaar & Driving License
- Booking Invoice
- Notifications

---

## 🚘 Car Owner

- Register as Owner
- Upload Profile
- Upload Aadhaar & Driving License
- Add Cars
- Upload Multiple Car Images
- Edit Car Details
- View Listed Cars
- Manage Booking Requests
- Approve/Reject Booking Requests
- View Earnings
- Commission Calculation
- Owner Dashboard
- Notifications

---

## 👨‍💼 Admin

- Admin Dashboard
- Django Admin Panel
- Approve Customer Documents
- Approve Owner Documents
- Approve Car Listings
- Reject Cars with Reason
- Manage Bookings
- Revenue Dashboard
- Platform Commission
- User Management

---

# 💳 Payment Features

- Razorpay Payment Gateway
- Payment Success Handling
- Payment History
- Invoice Generation
- Wallet Support

---

# 📧 Email Notifications

Automatically sends email for:

- Account Registration
- Booking Confirmation
- Booking Approval
- Booking Rejection
- Payment Success

---

# 📊 Dashboards

### Customer Dashboard

- Active Bookings
- Booking History
- Wishlist
- Wallet
- Notifications

### Owner Dashboard

- Listed Cars
- Booking Requests
- Monthly Earnings
- Total Earnings
- Commission Deducted

### Admin Dashboard

- Total Users
- Total Cars
- Pending Cars
- Pending Verifications
- Revenue Report

---

# 🛠 Technology Stack

## Frontend

- HTML5
- CSS3
- JavaScript
- Font Awesome
- AOS Animation

## Backend

- Python
- Django

## Database

- SQLite (Development)
- PostgreSQL (Production Ready)

## Payment Gateway

- Razorpay

## Media Storage

- Cloudinary (Production)

## Deployment

- Render

---

# 📁 Project Structure

```
DriveShare/
│
├── accounts/
├── bookings/
├── cars/
├── core/
├── dashboard/
├── notifications/
├── templates/
├── static/
├── media/
├── DriveShare/
│
├── manage.py
├── requirements.txt
├── Procfile
├── runtime.txt
└── README.md
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/Tejas-Mahesh/DriveShare.git
```

Move inside project

```bash
cd DriveShare
```

Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

Install Requirements

```bash
pip install -r requirements.txt
```

Run Migrations

```bash
python manage.py migrate
```

Collect Static Files

```bash
python manage.py collectstatic
```

Run Server

```bash
python manage.py runserver
```

Open

```
http://127.0.0.1:8000
```

---

# ⚙ Environment Variables

Create a `.env` file in the project root.

```env
SECRET_KEY=your_secret_key

DEBUG=True

ALLOWED_HOSTS=127.0.0.1,localhost

EMAIL_HOST_USER=your_email

EMAIL_HOST_PASSWORD=your_password

RAZORPAY_KEY_ID=your_key

RAZORPAY_KEY_SECRET=your_secret

CLOUDINARY_CLOUD_NAME=your_cloud

CLOUDINARY_API_KEY=your_api_key

CLOUDINARY_API_SECRET=your_api_secret
```

---

# 📸 Screenshots

Add screenshots here after deployment.

- Home Page
- Login
- Signup
- Customer Dashboard
- Owner Dashboard
- Admin Dashboard
- Booking Page
- Payment Page

---

# Future Enhancements

- AI Car Recommendation
- Live Chat
- GPS Tracking
- OTP Verification
- Mobile Application
- Multi-language Support
- Advanced Analytics
- Coupon & Offers
- Ratings & Reviews
- Vehicle Availability Calendar

---

# 👨‍💻 Developer

**Pavan Kumar M**

Python Full Stack Developer

GitHub

https://github.com/Tejas-Mahesh

---

# 📜 License

This project is developed for educational and portfolio purposes.

© 2026 DriveShare. All Rights Reserved.
