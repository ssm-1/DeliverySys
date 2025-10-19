from datetime import datetime

class Parcel:
    def __init__(self, parcel_id, delivery_address, city, state, zipcode, deadline, weight, status):
        """
        Initializes a new Parcel instance with the provided attributes.

        Parameters:
        parcel_id (int): Unique identifier for the parcel.
        delivery_address (str): Delivery address of the parcel.
        city (str): City where the parcel is to be delivered.
        state (str): State where the parcel is to be delivered.
        zipcode (str): Zip code of the delivery address.
        deadline (str): Deadline for the parcel delivery.
        weight (str): Weight of the parcel.
        status (str): Current status of the parcel (e.g., "At Hub", "En route", "Delivered").
        """
        self.parcel_id = parcel_id  # Unique identifier for the parcel
        self.delivery_address = delivery_address  # Delivery address of the parcel
        self.city = city  # City of the delivery address
        self.state = state  # State of the delivery address
        self.zipcode = zipcode  # Zip code of the delivery address
        self.deadline = deadline  # Deadline by which the parcel should be delivered
        self.weight = weight  # Weight of the parcel
        self.status = status  # Current status of the parcel
        self.departure_time = None  # Time when the parcel departs from the hub (initially None)
        self.delivery_time = None  # Time when the parcel is delivered (initially None)

    def __str__(self):
        """
        Provides a string representation of the Parcel instance.

        Returns:
        str: A formatted string containing all relevant parcel details.
        """
        return "{}, {}, {}, {}, {}, {}, {}, {}, {}".format(
            self.parcel_id, self.delivery_address, self.city, self.state, self.zipcode,
            self.deadline, self.weight, self.delivery_time,
            self.status
        )

    def update_status(self, query_time):
        """
        Updates the status of the parcel based on the provided time.

        Parameters:
        query_time (datetime): The current time used to determine the parcel's status.
        """
        if self.delivery_time and self.delivery_time <= query_time:
            self.status = "Delivered"  # Parcel has been delivered if delivery_time is before or at the current time
        elif self.departure_time and self.departure_time > query_time:
            self.status = "En route"  # Parcel is en route if departure_time is after the current time
        else:
            self.status = "At Hub"  # Parcel is at the hub if neither of the above conditions are met

    def print_package_info_at_time(self, chosen_time):
        """
        Prints the package information at a specific time.

        Parameters:
        chosen_time (datetime): The time at which to print package information.
        """
        formatted_time = chosen_time.strftime("%I:%M %p")
        print(f"Package {self.parcel_id} at {formatted_time}:")

        # Print wrong address for package 9 before 10:20 AM, otherwise print package address as normal
        if self.parcel_id == 9 and chosen_time < datetime.strptime("10:20 AM", "%I:%M %p"):
            print(f"Address: 300 State St")  # Updated address for before 10:20 AM
        else:
            print(f"Address: {self.delivery_address}, {self.city}, {self.state} {self.zipcode}")

        print(f"Delivery Deadline: {self.deadline} | Weight: {self.weight}")

        # Define delivery time of package
        delivery_time = datetime.strptime(self.delivery_time, "%I:%M %p") if self.delivery_time else None

        # Define status of package
        status = ''

        # If chosen time is past delivery time, update status variable to delivered
        if delivery_time and chosen_time >= delivery_time:
            status = 'Delivered'
        # If package is on the late truck and en route, update status
        elif chosen_time > datetime.strptime("09:18 AM", "%I:%M %p") and self.parcel_id in (
        6, 25, 26, 28, 31, 32, 11, 12, 1, 24, 22, 17, 9):
            status = 'En route'
        # If package left at 8 AM and en route, update status
        elif chosen_time > datetime.strptime("08:00 AM", "%I:%M %p") and self.parcel_id not in (
        6, 25, 26, 28, 31, 32, 11, 12, 1, 24, 22, 17, 9):
            status = 'En Route'
        # If package has not left the hub, update status
        else:
            status = "At Hub"

        print(f"Status: {status}")
        # Prints delivery time if status is delivered, or 'Delivery Time: None' if status is en route or still at the hub
        if status == 'Delivered':
            formatted_delivery_time = delivery_time.strftime("%I:%M %p")
            print(f"Delivery Time: {formatted_delivery_time}")
        else:
            print("Delivery Time: None")
        print()

    def get_id(self):
        return self.parcel_id