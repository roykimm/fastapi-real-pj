from dataclasses import dataclass


class Fruit:
    def __init__(self, name: str, calories: float):
        self.name = name
        self.calories = calories

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


banana = Fruit('banana', 10)
apple = Fruit('apple', 20)


#@dataclass(frozen=False)
# @dataclass(kw_only=True)
@dataclass()
class Fruit:
    #__slots__ = ["name", "calories"]

    name: str
    calories: float

    def __str__(self):
        return f"{self.name}:{self.calories}"



banana = Fruit('banana',10)
banana2 = Fruit('banana', 20)

print(banana)


@dataclass()
class Person:
    name: str
    age: int
    job: str = None
    friends: list[str] = None

    def __str__(self):
        return f"{self.name}:{self.age}"


json: dict = {
    'name': 'Bob',
    'age': 10,
    'job': 'sales',
    'friends': ['mario', 'luigi']
}

bob = Person(json['name'], json['age'], json['job'], json['friends'])
bella = Person(json)
print(bob.job)
print(bella)

def generate_id() -> str:
    return "".join(random.choices(string.ascii_uppercase, k=12))


@dataclass(slots=True)
class Person:
    name: str
    address: str
    active: bool = True
    email_address: list[str] = field(default_factory=list)
    id: str = field(init=False, default_factory=generate_id)
    _search_string: str = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._search_string = f"{self.name} {self.address}"


# 4 —A lot of helper methods
# 위에서 적은 것처럼 많은 method를 제공하고 있어서, 다양한 방식으로 사용할 수 있습니다.
#
# dict() — returns a dictionary of the model’s fields and values
# json() — returns a JSON string representation dictionary
# copy() — returns a deep copy of the model
# parse_obj() — a utility for loading any object into a model with error handling if the object is not a dictionary
# parse_raw() — a utility for loading strings of numerous formats
# parse_field() — similar to parse_raw() but meant for files
# from_orm() — loads data into a model from an arbitrary class
# schema() — returns a dictionary representing the model as JSON schema
# schema_json() — returns a JSON string representation of schema()
# construct() — a class method for creating models without running validation
# __fields_set__ — Set of names of fields which were set when the model instance was initialized
# __fields__ — a dictionary of the model’s fields
# __config__ — the configuration class for the model

