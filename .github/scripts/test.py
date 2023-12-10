import os

def print_environment_variables():
    print("Environment Variables:")
    for key, value in os.environ.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    print_environment_variables()
