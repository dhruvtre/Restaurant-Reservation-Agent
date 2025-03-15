"""
Restaurant booking system tool definitions and configurations.
Contains function specifications for restaurant search and order management.
"""

#Basic type imports
from typing import List, Dict, Union

#Setting up basic logging
import logging
logger = logging.getLogger('foodiespot')
logger.info("Prompts loaded")

restaurant_tools: List[Dict[str, Union[str, Dict[str, Union[str, Dict[str, Union[str, List[str], Dict[str, Union[str, Dict]]]]]]]]] = [
    {
        "type": "function",
        "function": {
            "name": "search_restaurant_information",
            "description": (
                "Search for restaurants based on a flexible set of query parameters. "
                "The input is a JSON object that may include any of the restaurant information fields based on the information shared by the user."
                "These fields strictly only include 'name', 'location', 'cuisine', 'operating_hours', 'phone', 'restaurant_max_seating_capacity', 'max_booking_party_size'"
                "and 'operating_days'. The function returns a list of restaurants that match the given criteria. "
                "Empty searches return a list of all restaurants."
            ),
            "parameters": {
                "type": "object",
                "required": [],
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the restaurant."
                    },
                    "location": {
                        "type": "string",
                        "description": "Keywords or location details of the restarurant which can include street address or nearby landmark mentioned by the user."
                    },
                    "cuisine": {
                        "type": "string",
                        "description": "Keywords of cuisine types served by the restaurant."
                    },
                    "operating_hours": {
                        "type": "object",
                        "properties": {
                            "open": {
                                "type": "string",
                                "description": "Opening time in HH:MM format."
                            },
                            "close": {
                                "type": "string",
                                "description": "Closing time in HH:MM format."
                            }
                        },
                        "description": "Operating hours of the restaurant."
                    },
                    "phone": {
                        "type": "string",
                        "description": "Contact phone number."
                    },
                    "restaurant_max_seating_capacity":
                    {
                        "type": "integer",
                        "description": "Maximum seating capacity of the restaurant."
                    },
                    "max_booking_party_size":
                    {
                        "type": "integer",
                        "description": "Maximum allowed party size for a single reservation."
                    },
                    "operating_days": {
                        "type": "string",
                        "description": "Days of the week when the restaurant is open."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "make_new_order",
            "description": (
                        "This is a tool to confirm a new order in the restaurant order management system."
                        "Only call this tool when you have the following information from the user: Name, Phone Number, Party Size, Restaurant Preference, Reservation Day and Reservation time."
                        "Review all collected information with the user before calling this tool."
                        "Do not call this function with assumed or hallucinated values. "
                        "All parameters must be explicitly provided by the user through conversation. "
                        "The function will check capacity before confirming - reservations exceeding restaurant capacity will be rejected."
            ),
            "parameters": {
                "type": "object",
                "required": [
                    "restaurant_id",
                    "orderer_name",
                    "orderer_contact",
                    "party_size",
                    "reservation_date",
                    "reservation_time"
                ],
                "properties": {
                    "restaurant_id": {
                        "type": "string",
                        "description": "Unique identifier of the restaurant."
                    },
                    "orderer_name": {
                        "type": "string",
                        "description": "Name of the person making the reservation."
                    },
                    "orderer_contact": {
                        "type": "string",
                        "description": "Contact information for the orderer."
                    },
                    "party_size": {
                        "type": "integer",
                        "description": "Number of people for the reservation."
                    },
                    "reservation_date": {
                        "type": "string",
                        "description": "Reservation date in YYYY-MM-DD format. Convert relative dates (tomorrow, next Friday) to this format."
                    },
                    "reservation_time": {
                        "type": "string",
                        "description": "Reservation time in HH:MM format."
                    }
                },
                "description": "A complete JSON object containing all required order information."
            }
        }
    }
]
