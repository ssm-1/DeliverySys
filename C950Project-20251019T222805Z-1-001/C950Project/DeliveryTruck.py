#This will create the delivery truck objects
class DeliveryTruck:
    def __init__(self, max_capacity, travel_speed, current_load, packages, total_mileage, current_location, departure_time):
        """
        Creates a new DeliveryTruck object with specified parameters.

        Parameters:
        max_capacity (int): The truck's maximum load capacity (in units of weight).
        travel_speed (float): The truck's travel speed (in miles per hour).
        current_load (float): The weight currently being carried by the truck.
        packages (list of int): List containing IDs of packages loaded onto the truck.
        total_mileage (float): Total distance covered by the truck (in miles).
        current_location (str): The truck's current location address.
        departure_time (datetime.timedelta): The time when the truck departs from the base or hub.
        """
        self.max_capacity = max_capacity  # Maximum weight the truck can hold
        self.travel_speed = travel_speed  # The truck's speed (in miles per hour)
        self.current_load = current_load  # The current weight of the load
        self.packages = packages  # IDs of the packages currently loaded
        self.total_mileage = total_mileage  # Total miles the truck has traveled
        self.current_location = current_location  # Truck's present address
        self.departure_time = departure_time  # Time at which the truck starts its journey
        self.current_time = departure_time  # Initializes current time with the departure time

    def __str__(self):
        """
        Returns a string representation of the DeliveryTruck instance.

        Returns:
        str: A formatted string with key details about the truck.
        """
        return "{}, {}, {}, {}, {}, {}, {}".format(
            self.max_capacity, self.travel_speed, self.current_load, self.packages, self.total_mileage,
            self.current_location, self.departure_time
        )
