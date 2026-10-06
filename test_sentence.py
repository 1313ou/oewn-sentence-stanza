import load_stanza as model
from sentence import parse_sentence


# T E S T

def main():
    examples0 = [
        "is anybody here",
        "is anybody happy",
    ]
    examples1 = [
        "go",
        "don't go",
        "do go",
        "let's go",
        "let me explain",
        "let the man go",
        "let there be more light",
    ]
    examples2 = [
        "is anybody here",
        "this is obvious",
        "This is a sentence.",
        "I like music",
        "This is a complete sentence.",
        "The quick brown fox jumps over the lazy dog.",
        "She loves programming and solving complex problems.",
        "The cat sat on the mat.",
        "He was smoking.",
        "do you smoke",
    ]
    examples3 = [
        "A full thought, it is.",
        "Incomplete",
        "running fast",
        "What about this?",
        "a quick brown fox",
        "obvious though this is ",
    ]
    examples4 = [
        "We were so far back in the theater, we could barely read the subtitles.",
        "We were so far back in the theater we could barely read the subtitles.",
        "force out the air",
        "blow on the soup to cool it down",
        "beat the living hell out of him",
        "was immensely more important to the project as a scientist than as an administrator",
        "would have scarce arrived before she would have found some excuse to leave",
        "would have scarcely arrived before she would have found some excuse to leave",
    ]
    examples5 = [
        "an RBI double that drove in Tony Campana",
        "it was none other than Marco Scutaro who drove in Ryan Theriot",
        "I'm enjoying this. I know. This rules!",
        "It rocks, but it can get a little dense.",
        "A shot of tequila and then turn up the song, it kicks ass",
        "To say Ben slays in these photos is an understatement",
        "Machado drove in the game - winning run in a 3 - 2 win",
        "Longoria hit 17 home runs and drove in 55 runs",
        "Brian McCann drove in four runs with four hits",
    ]
    examples6 = [
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
    for input_text in examples6:  # examples0 + examples1 + examples2 + examples3 + examples4:
        sentence_result = parse_sentence(input_text, model.nlp, color=True)
        flag = {sentence_result[0]}
        ndeps = {sentence_result[1]}
        cdeps = {sentence_result[2]}

        print(f"Text: {input_text}")
        print(f"Sentence: {flag}")
        for ndep in  ndeps:
            print(f"Deps:\n{ndep}")
        for cdep in  cdeps:
            print(f"Constituency:\n{cdep}")
        print("\n")


if __name__ == '__main__':
    main()
