from prettyprint import G
from prettyprint import Z

def main():
    examples = [
        "The Scottish Symphony",
        "Scottish authors",
        "Scottish mountains",
        "Scotch broth",
        "Scotch whiskey",
        "Scotch plaid",
        "It rained like billyo",
        "It rained like all get out",
        "‘plenty’ is nonstandard",
        "I've had plenty, thanks",
    ]
    for input_text in examples:  # examples0 + examples1 + examples2 + examples3 + examples4:

        print(f"Text: {G}{input_text}{Z}")
        print("\n")


if __name__ == '__main__':
    main()