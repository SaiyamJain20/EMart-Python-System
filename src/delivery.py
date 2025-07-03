import uuid
import datetime

class Delivery:
    """
    Represents a delivery associated with an order in the E-Mart system.

    Attributes:
        delivery_id (str): Unique identifier for the delivery.
        order_id (str): Identifier for the associated order.
        delivery_status (str): Current status of the delivery.
    """

    def __init__(self, order_id: str):
        """
        Initializes a new delivery instance.
        """
        self.delivery_id = uuid.uuid4().hex  # Generate a unique delivery ID
        self.order_id = order_id  # Associated order ID
        self.delivery_status = "Preparing" 

    def update_status(self, status: str) -> bool:
        """
        Updates the delivery status.
        """
        if not status:
            raise ValueError("Status cannot be empty.")
        self.delivery_status = status  # Update the delivery status
        return True

    def get_estimated_time(self) -> datetime.datetime:
        """
        Estimates the delivery time.
        """
        return datetime.datetime.now() + datetime.timedelta(hours=2)

    def track_delivery(self) -> str:
        """
        Retrieves the current delivery status.
        """
        return self.delivery_status
