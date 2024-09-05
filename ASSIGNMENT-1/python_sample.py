# Sample Python program demonstrating conditionals, loops, and classes

def main():
    # Conditional statements
    x = 10
    if x > 5:
        print("x is greater than 5")
    elif x == 5:
        print("x is equal to 5")
    else:
        print("x is less than 5")

    # Loop with a range
    for i in range(5):
        print(f"Loop iteration: {i}")

    # While loop
    count = 0
    while count < 3:
        print(f"While loop count: {count}")
        count += 1

    # List comprehension
    squares = [n**2 for n in range(1, 6)]
    print(f"Squares: {squares}")

    # Creating an object
    person = Person("Alice", 30)
    person.introduce()
    person.have_birthday()
    person.introduce()

# Class definition
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        print(f"Hi, I'm {self.name} and I'm {self.age} years old.")
    
    def have_birthday(self):
        self.age += 1
        print(f"Happy birthday to me! I'm now {self.age}.")

if __name__ == "__main__":
    main()