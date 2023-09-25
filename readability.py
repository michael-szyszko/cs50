import cs50

MAX_GRADE = 16

text = cs50.get_string("Text: ")
length = len(text)

words = text.split(" ")
word_count = len(words)
sentence_count = text.count(".") + text.count("?") + text.count("!")
character_count = (
    length
    - word_count
    - sentence_count
    + 1
    - text.count("'")
    - text.count('"')
    - text.count(",")
)

avg_num_letters_per_100_words = character_count / word_count * 100.0
avg_num_sentences_per_100_words = sentence_count / word_count * 100.0

grade = round(
    (0.0588 * avg_num_letters_per_100_words)
    - (0.296 * avg_num_sentences_per_100_words)
    - 15.8
)

if grade > 1 and grade < 16:
    print(f"Grade {grade}")
elif grade >= MAX_GRADE:
    print(f"Grade {MAX_GRADE}+")
else:
    print("Before Grade 1")
