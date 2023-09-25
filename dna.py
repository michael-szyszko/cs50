import csv
import sys


def main():
    # Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # Read database file name into a variable
    database_file_name = sys.argv[1]

    # Read DNA sequence file into a variable
    dna_sequence_file_name = sys.argv[2]

    # Find longest match of each STR in DNA sequence
    with open(database_file_name) as file:
        reader = csv.DictReader(file)
        field_names = reader.fieldnames

    with open(dna_sequence_file_name) as file:
        sequence_text = file.readline()

    sequence_match_counts = {}
    # Search
    for field_name in field_names[1:]:
        sequence_match_counts[field_name] = longest_match(sequence_text, field_name)

    # Check database for matching profiles
    matches_needed = len(sequence_match_counts)
    with open(database_file_name) as file:
        reader = csv.DictReader(file)
        for row in reader:
            matches = 0
            for field_name in field_names[1:]:
                if int(row[field_name]) == sequence_match_counts[field_name]:
                    matches += 1
            if matches == matches_needed:
                print(row["name"])
                return
    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):
        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:
            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
