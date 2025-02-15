import argparse
import subprocess

def run_main():
    """Runs the main example."""
    subprocess.run(["python", "src/main.py"], check=True)

def run_tests():
    """Runs the unit tests."""
    subprocess.run(["python", "-m", "unittest", "discover", "tests/unit"], check=True)

def main():
    parser = argparse.ArgumentParser(description="CLI for the trading bot framework.")
    subparsers = parser.add_subparsers(title="commands", dest="command")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run the main example")
    run_parser.set_defaults(func=run_main)

    # Test command
    test_parser = subparsers.add_parser("test", help="Run unit tests")
    test_parser.set_defaults(func=run_tests)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    else:
        args.func()

if __name__ == "__main__":
    main()