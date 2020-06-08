import sqlite3

class SQLighter:

    def __init__(self, database):
        # Connecting to database and saving the connection
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status=True):
        # Getting all active subscribers
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists(self, user_id):
        # Check if user exists in database
        with self.connection:
            result = self.cursor.execute(
                'SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status=True):
        # Adding new subscriber
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (`user_id`, `status`) VALUES (?,?)", (user_id, status))

    def update_subscription(self, user_id, status):
        # Adding two commands to user: subscribe & unsubscribe
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def close(self):
        # Closing connection
        self.connection.close()
