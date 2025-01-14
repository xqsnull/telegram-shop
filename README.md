# Telegram Shop Bot

This project is a Telegram bot for managing an online shop with a basket system, SQLite database for order tracking, and various interactive functionalities. The bot is built using Python and the `pyTelegramBotAPI` library.

## Features

- **Welcome Menu**: Greets users with an interactive menu.
- **Product Categories**: Users can browse products by categories.
- **Basket Management**: Users can add items to their basket, view the basket, and proceed to checkout.
- **Admin Panel**: Restricted access for admins to view orders and manage the shop.
- **SQLite Database**: Keeps track of user orders.

---

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-repo/telegram-shop-bot.git
   cd telegram-shop-bot
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Bot**:

   - Create a `cfg.py` file with the following structure:
     ```python
     class Config:
         token = 'YOUR_TELEGRAM_BOT_TOKEN'
         admin_chat_id = YOUR_ADMIN_CHAT_ID
         all_items = {
             'fortnite': 500,
             'valorant': 600
         }
     ```

4. **Run the Bot**:

   ```bash
   python main.py
   ```

---

## Usage

### Commands

- `/start`: Launches the welcome menu.

### Inline Buttons

- **Магазин**: Opens the shop interface.
- **FAQ**: Provides frequently asked questions.
- **О нас**: Displays information about the shop.
- **Корзина**: Shows the user's current basket.
- **Админка** (Admin Only): Provides access to admin functions like viewing orders.

---

## Code Structure

- ``: Contains the main logic for the bot.
- ``: Stores bot configuration and settings.
- ``: SQLite database file for storing orders.
- ``: Contains image assets used in the bot.

---

## Database Schema

The bot uses an SQLite database to store order details. The schema is as follows:

| Field         | Type      | Description            |
| ------------- | --------- | ---------------------- |
| id            | INTEGER   | Order ID (Primary Key) |
| user\_id      | INTEGER   | Telegram User ID       |
| username      | TEXT      | Username               |
| items         | TEXT      | Items in the order     |
| total\_amount | INTEGER   | Total order amount     |
| currency      | TEXT      | Currency used          |
| order\_date   | TIMESTAMP | Date of the order      |

---

## Basket Management

The `BasketManager` class handles the basket operations for the user:

- ``: Adds an item to the basket.
- ``: Clears the basket.
- ``: Calculates the total price of the basket.
- ``: Provides a summary of items in the basket.
- ``: Checks if the basket is empty.

---

## Admin Panel

The admin panel provides restricted access to manage orders:

- **Просмотр заказов**: View all orders in the database.
- **Назад**: Return to the main menu.

---

## Static Files

The following images should be placed in the `static/` directory:

- `welcome_img.png`
- `shop_img.png`
- `cart_img.png`
- `full_cart_img.png`
- `faq_img.png`

---

## Future Improvements

- Payment gateway integration.
- More product categories.
- Improved order management.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contributions

Contributions are welcome! Feel free to fork the repository and create pull requests.

