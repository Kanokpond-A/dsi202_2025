# 🌳 PLOOKJING 🌳

> **PLANTING IS NOT GIVING BACK. IT'S MOVING FORWARD.**  
PLOOKJING is a digital platform that empowers individuals to take part in environmental restoration through meaningful and accessible remote tree planting.

Our mission is simple yet powerful: bring nature back into everyday life. We combine technology, sustainability, and community to make climate action something anyone can participate in—seamlessly, meaningfully, and consistently. Whether you're planting one tree a month or growing a home garden with eco-tools, you're not just giving back—you're growing forward.

---

### 1. Select Tree and Planting Location
**As a** user
**I want to** select the tree I wish to plant and specify the planting location
**So that** I can plant the tree in an area that I care about

### 2. Receive Tree Care Notifications
**As a** user
**I want to** receive notifications about tree care tasks such as fertilizing, watering, and pruning
**So that** I can effectively monitor and support my tree’s growth

### 3. Purchase Tree Planting Equipment
**As a** user
**I want to** purchase tree planting equipment and real trees for home planting
**So that** I can grow trees on my own and create a peaceful, natural atmosphere in my life

---

## What is PLOOKJING?

PLOOKJING allows users to choose tree species and assign real-world planting locations. Once planted, each tree becomes part of the user's digital forest, complete with care updates, growth tracking, and a personal sense of environmental impact. The platform also features a curated eco-shop offering trees, tools, and accessories for those who prefer planting with their own hands at home or in their communities.

**We provide multiple ways for users to take action:**

- Remote tree planting in designated provinces  
- In-home planting with ordered equipment  
- Growth monitoring and alerts  
- Personalized dashboards showing planted trees and order history

---

## Getting Started

When visiting `http://localhost:8000`, users are greeted by a beautifully designed **"Get Started" landing page** introducing the platform. This welcome screen introduces PLOOKJING's users to proceed to the main site at `/home`.

**Main Navigation Bar:**

- Left:
  - Home
  - About Us
  - Tree & Equipment

- Right:
  - Notifications
  - Shopping Cart
  - Profile (or login/signup if not signed in)

If logged in, users see their username and gain access to profile, orders, and logout options.

---

## Home Page Experience

The homepage sets the tone with soft colors, elegant typography, and a nature-focused aesthetic. It includes:

- A brief about the importance of tree planting
- A map-based or dropdown selection to choose a planting location
- "Tree of the Month" or featured recommendations

Users are reminded to log in or sign up—either via custom email or integrated Google Login.

---

## Tree & Equipment Page

The Tree & Equipment section is a sleek blend of utility and design. Users can:

- Use the **search bar** to filter trees and tools
- View items as modern cards including:
  - Image
  - Name and description
  - **BUY NOW** button
  - **Add to Cart** link

Each item card includes smooth animations, rounded edges, and hover effects for enhanced UX.

---

## Remote Tree Planting Flow

Once a tree is selected and purchased:

1. The user selects a planting province.
2. The order is confirmed and logged.
3. Notifications follow, such as:
   - “Your tree has been planted!”

All alerts appear under the notification icon and the **My Tree** section.

---

## Eco-Equipment Purchase Flow

For DIY users, the platform supports full eco-tool purchases with delivery:

1. Choose tools (e.g., compost, shovels, saplings)
2. Add to cart or buy directly
3. Input **shipping address** and **contact number**
4. Complete secure payment
5. Track progress via **My Orders**

The system distinguishes tree orders from equipment purchases for clarity.

---

## Notification System

The built-in notification engine alerts users of:

- Tree planting confirmations
- Equipment order statuses (pending → shipped → delivered)
- Platform news and campaigns

Dropdowns under the 🔔 icon present messages cleanly and beautifully.

---

## User Dashboard: My Tree & My Orders

Accessible features:

- **My Tree** — Track your planted trees, location
- **My Orders** — View equipment order history and shipping info

These views align with the brand’s green-forward visual style.

---

## Developer Installation Guide

Follow these steps to run the project locally:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/plookjing.git
cd plookjing
```

---

### 2. Set Up the Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
```

---

### 3. Run Migrations

```bash
python manage.py migrate
```

---

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

---

### 5. Launch the Server

```bash
python manage.py runserver
```

---

Once running, visit:

```bash
http://localhost:8000
```

---
Youtube Link:
https://youtu.be/27HkvXHWId4
---
