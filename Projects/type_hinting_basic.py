# This is just a reference file for myself to learn type hinting
# Learning Sources:

# Thanks to: Corey Schafer: https://www.youtube.com/watch?v=RwH2UzC2rIo
# +: https://www.youtube.com/watch?v=fM4O9bModsE
import random
from typing import List
from dataclasses import dataclass
from pydantic import validate_call
from typing import NewType, TypedDict, Any, TypeVar, Literal

# Example for Type Hinting
def create_user(first_name: str, last_name: str, age: int) -> dict:
    email = "something@example.com"
    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "age": age,
    }

user1: dict = create_user("Fortnite", "xD", 67)

UserAlias = NewType("UserAlias", dict[str, str | int | None]) # Type Alias

class UserDict(TypedDict):
    first_name: str
    last_name: str
    email: str
    age: int | None
    # Each value can be type checked individually

# Dataclass example
@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    age: int | None = None
    fav_color: UserAlias | None = None

# Example for data validation
@validate_call # Does the data validation without isinstance manual validation
def create_user(first_name: str, last_name: str, age: int) -> User:
    email = "something@example.com"

    if not isinstance(first_name, str):
        raise TypeError("first_name must be a string")

    # And so on

    return User(
        first_name=first_name,
        last_name=last_name,
        age=age,
        email=email
    ) # -> = Returns the dataclass, but pre-fills the variables with type checking (very good)

def random_user(items: List[Any]) -> Any:
    return ""

    # Any is used when you don't know what type something is, like if you have absolutely no idea
    # Bad practice and should generally not be used (ig)

# Instead use TypeVar
T = TypeVar("T")

def random_user_2(items: list[T]) -> T:
    return random.choice(items) # Simulation
    # Tells the IDE that the input is the same as the output (type perspective)
    # However, this is older syntax, see new for better syntax Python 3.12+


def random_user_2_new[T](items: list[T]) -> T:
    return random.choice(items) # Simulation

# This definitely looks like something I can flex with lmao


# Literal String:

def user_role(role: Literal["admin", "user", "moderator"]) -> str:
    return role
# This is used to specific that role can only be "admin", "user" or "moderator" and nothing else
