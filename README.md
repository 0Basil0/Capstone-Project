Project Title:
NutriGuard — AI-Powered Food Allergy & Meal Planner System
________________________________________
Overview
    NutriGuard is a web application designed to help users with food allergies safely manage their diet and meal planning.
    By leveraging AI and automation, the system allows users to:
    •	Create personalized accounts and manage their allergy profiles.
    •	Receive AI-powered recommendations about which foods are safe to eat.
    •	Plan their meals efficiently with a 7-day automated meal planner tailored to their allergies.
    •	Interact with an AI chatbot that can answer questions about ingredients and allergen safety in real time.
    The goal of NutriGuard is to prevent allergic reactions, provide smart food guidance, and make meal planning stress-free for users with dietary restrictions.
________________________________________
Core Features
    1.	User Authentication: Secure login, logout, and account management.
    2.	Allergy Management: Users can add, update, or delete allergies.
    3.	Food & Recipe Database: Catalog of foods tagged with allergens.
    4.	AI Chatbot: Conversational assistant that checks ingredient safety and provides recommendations.
    5.	Day Meal Planner: Automatically generates meal plans based on user allergies.

    6.	Dashboard: Visual summary of safe foods and AI suggestions.
_______________________________________
🧩 User Stories
🔐 Account & Authentication
    • As a visitor, I can create an account (sign up) with my first name, last name, username, email, password, and an optional age field.
    • As a registered user, I can log in and log out securely.
    • After logging in, I am redirected to my Home dashboard automatically.

👤 Profile Management
    • As a user, I can edit my profile information, including my first name, last name, and age.
    • As a user, I can upload or change my profile avatar from the Edit Profile page.
    • If I don’t upload an avatar, the system displays my initials (based on first/last name or username) in the navbar and chat interface.

⚕️ Allergies
    • As a user, I can add one or more allergies using a comma-separated input field.
    • As a user, I can view all my saved allergies and see their descriptions.
    • As a user, I can edit or delete any of my saved allergies.
    
🍽️ Meal Planner
    • As a user, I can generate AI-suggested meals for the current day (Breakfast, Lunch, Dinner) by clicking “Generate Today’s Plan.”
    • When a plan is generated:
        o New Food records are created, along with timestamped images saved in static directories.
        o A MealPlan entry is created or updated for the day, linking to the generated food items.
    • The Home dashboard displays three interactive meal circles (Breakfast, Lunch, Dinner) featuring:
        o Background images of the meals.
        o Meal names and expandable details (ingredients & description).
    • Clicking a meal circle opens a modal or inline panel with ingredients and description.
    • Closing the view restores the previous snapshot (image and text).

🤖 AI Chat Assistant
    • As a user, I can open the AI Chat interface and view:
        o A sidebar list of my previous chat sessions.
        o A main pane showing messages within the selected session.
    • As a user, I can:
        o Start a new chat, send messages, and receive AI-generated replies (all stored in history).
        o Delete an entire chat session when no longer needed.
    • The chat interface displays:
        o My avatar or initials next to my messages.
📚 References
    • AI Text Generation: Powered by Gemini API (Google AI).
    • AI Image Generation: Uses Pollinations API to generate dynamic and realistic meal images.
_______________________________________
NutriGuard ERD:

![NutriGuard ERD](https://raw.githubusercontent.com/0Basil0/Capstone-Project/main/files/NutriGuard_ERD.png)
