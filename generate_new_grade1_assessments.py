import csv
from pathlib import Path


OUTPUT_BASE = Path("assessments")


def build_multiple_choice(question, choices, correct_index, explanation,
                           test_name, title_item, path,
                           content_type="Question", q_type="Multiple Choice"):
    letters = ["A", "B", "C", "D", "E", "F", "G"]
    row = {
        "Question": question,
        "Answer": letters[correct_index],
        "Explanation": explanation,
        "PictureURL": "",
        "OptionA": choices[0] if len(choices) > 0 else "",
        "OptionB": choices[1] if len(choices) > 1 else "",
        "OptionC": choices[2] if len(choices) > 2 else "",
        "OptionD": choices[3] if len(choices) > 3 else "",
        "OptionE": choices[4] if len(choices) > 4 else "",
        "OptionF": choices[5] if len(choices) > 5 else "",
        "OptionG": choices[6] if len(choices) > 6 else "",
        "TestName": test_name,
        "Content Type": content_type,
        "Title Item": title_item,
        "Type": q_type,
        "Path": path,
    }
    return row


def build_select_all(question, choices, correct_indices, explanation,
                     test_name, title_item, path,
                     content_type="Question"):
    letters = ["A", "B", "C", "D", "E", "F", "G"]
    answer = ",".join(letters[i] for i in correct_indices)
    row = build_multiple_choice(
        question,
        choices,
        correct_indices[0],
        explanation,
        test_name,
        title_item,
        path,
        content_type=content_type,
        q_type="Select All That Apply",
    )
    row["Answer"] = answer
    return row


def write_csv(rows, directory, filename):
    directory_path = OUTPUT_BASE / directory
    directory_path.mkdir(parents=True, exist_ok=True)
    file_path = directory_path / filename
    fieldnames = [
        "Question",
        "Answer",
        "Explanation",
        "PictureURL",
        "OptionA",
        "OptionB",
        "OptionC",
        "OptionD",
        "OptionE",
        "OptionF",
        "OptionG",
        "TestName",
        "Content Type",
        "Title Item",
        "Type",
        "Path",
    ]
    with file_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def counting_questions():
    test_name = "Chapter 1: Numbers and Place Value"
    path = "Chapter 1/Counting 1-100"
    rows = []
    sequences = [14, 27, 38, 49, 63, 76]
    for idx, start in enumerate(sequences, 1):
        next_number = start + 1
        question = f"What number comes after {start} when counting by ones?"
        choices = [str(start - 1), str(next_number), str(next_number + 1), str(next_number + 2)]
        rows.append(
            build_multiple_choice(
                question,
                choices,
                1,
                f"Counting by ones means adding 1 to {start}, so {next_number} comes next.",
                test_name,
                f"Counting Sequence Q{idx}",
                path,
            )
        )
    pairs_by_twos = [8, 22, 36, 48]
    for offset, start in enumerate(pairs_by_twos, 1):
        next_number = start + 2
        question = f"When skip counting by 2s, what number comes after {start}?"
        choices = [str(start + 1), str(next_number), str(next_number + 1), str(next_number + 4)]
        rows.append(
            build_multiple_choice(
                question,
                choices,
                1,
                f"Skip counting by 2s means adding 2 each time, so {next_number} comes after {start}.",
                test_name,
                f"Counting Sequence Q{len(rows) + 1}",
                path,
            )
        )
    pairs_by_fives = [10, 25, 40, 55]
    for start in pairs_by_fives:
        next_number = start + 5
        question = f"What number comes next when counting by 5s starting at {start}?"
        choices = [str(start + 2), str(next_number), str(next_number + 5), str(start + 6)]
        rows.append(
            build_multiple_choice(
                question,
                choices,
                1,
                f"Counting by 5s adds five each time, so {next_number} follows {start}.",
                test_name,
                f"Counting Sequence Q{len(rows) + 1}",
                path,
            )
        )
    tens = [20, 30, 50]
    for start in tens:
        next_number = start + 10
        question = f"When counting by 10s, what number comes after {start}?"
        choices = [str(start + 5), str(next_number), str(next_number + 10), str(start + 20)]
        rows.append(
            build_multiple_choice(
                question,
                choices,
                1,
                f"Counting by 10s adds ten each time, so {next_number} comes after {start}.",
                test_name,
                f"Counting Sequence Q{len(rows) + 1}",
                path,
            )
        )
    question = "Which list shows counting forward by ones starting at 31?"
    choices = ["31, 32, 34, 35", "31, 32, 33, 34", "31, 33, 34, 35", "31, 30, 29, 28"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            1,
            "Counting forward by ones adds 1 each time, so 31, 32, 33, 34 is correct.",
            test_name,
            f"Counting Sequence Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which pattern shows counting by 10s starting at 5?"
    choices = ["5, 15, 25, 35", "5, 10, 15, 20", "5, 14, 23, 32", "5, 20, 30, 40"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Counting by 10s from 5 adds 10 each time: 5, 15, 25, 35.",
            test_name,
            f"Counting Sequence Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def tens_and_ones_questions():
    test_name = "Chapter 1: Numbers and Place Value"
    path = "Chapter 1/Tens and Ones"
    rows = []
    numbers = [34, 52, 18, 90, 67, 45]
    for idx, number in enumerate(numbers, 1):
        tens = number // 10
        ones = number % 10
        question = f"How many tens and ones are in {number}?"
        choices = [
            f"{tens} tens and {ones} ones",
            f"{tens - 1} tens and {ones + 10} ones",
            f"{tens + 1} tens and {ones - 1} ones",
            f"{ones} tens and {tens} ones",
        ]
        correct_index = 0
        explanation = f"{number} has {tens} tens ({tens * 10}) and {ones} ones to make {number}."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                correct_index,
                explanation,
                test_name,
                f"Place Value Q{idx}",
                path,
            )
        )
    numbers_words = [(43, "4 tens and 3 ones"), (71, "7 tens and 1 one"), (28, "2 tens and 8 ones")]
    for number, wording in numbers_words:
        question = f"Which shows the tens and ones for {number}?"
        choices = [
            f"{wording}",
            f"{wording.replace('tens', 'ones')}",
            "3 tens and 4 ones",
            "8 tens and 2 ones",
        ]
        explanation = f"{number} is made of {wording}."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                0,
                explanation,
                test_name,
                f"Place Value Q{len(rows) + 1}",
                path,
            )
        )
    expanded = [
        ("30 + 6", 36, "3 tens and 6 ones"),
        ("50 + 9", 59, "5 tens and 9 ones"),
        ("80 + 2", 82, "8 tens and 2 ones"),
    ]
    for expression, number, wording in expanded:
        question = f"{expression} shows a number. Which number is it?"
        choices = [
            str(number),
            str(number - 1),
            str(number + 10),
            str(number - 10),
        ]
        explanation = f"{expression} means {wording}, which makes {number}."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                0,
                explanation,
                test_name,
                f"Place Value Q{len(rows) + 1}",
                path,
            )
        )
    question = "Select all numbers that have 5 tens."
    choices = ["50", "54", "45", "58"]
    correct_indices = [0, 1]
    explanation = "5 tens means the number is in the 50s, so 50 and 54 each have 5 tens."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Place Value Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which number is made of 2 tens and 7 ones?"
    choices = ["27", "72", "25", "70"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "2 tens make 20 and 7 ones make 7, giving 27.",
            test_name,
            f"Place Value Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which number has 4 tens and 0 ones?"
    choices = ["40", "4", "400", "44"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "4 tens equal 40 with 0 ones.",
            test_name,
            f"Place Value Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def comparing_numbers_questions():
    test_name = "Chapter 1: Numbers and Place Value"
    path = "Chapter 1/Comparing Numbers"
    rows = []
    comparisons = [
        (34, 43, "<"),
        (68, 62, ">"),
        (51, 51, "="),
        (27, 39, "<"),
        (84, 48, ">"),
        (70, 67, ">"),
        (19, 29, "<"),
        (95, 59, ">"),
    ]
    symbols = ["<", ">", "="]
    for idx, (a, b, relation) in enumerate(comparisons, 1):
        question = f"Which symbol makes this statement true: {a} __ {b}?"
        choices = symbols + ["≠"]
        explanation = f"{a} is {relation} {b}, so {relation} is correct."
        correct_index = symbols.index(relation)
        rows.append(
            build_multiple_choice(
                question,
                choices,
                correct_index,
                explanation,
                test_name,
                f"Comparing Numbers Q{idx}",
                path,
            )
        )
    question_sets = [
        ([46, 38, 52], "Which number is greatest?", "52"),
        ([21, 30, 18], "Which number is smallest?", "18"),
        ([73, 37], "Which number is larger?", "73"),
        ([44, 40], "Which number is smaller?", "40"),
        ([65, 56], "Which number is greater?", "65"),
    ]
    for numbers, prompt, correct in question_sets:
        options = [str(n) for n in sorted(set(numbers + [numbers[0] + 10]))][:4]
        if correct not in options:
            options[0] = correct
        question = f"{prompt}"
        explanation = f"Comparing the values shows {correct} is the correct choice."
        correct_index = options.index(correct)
        rows.append(
            build_multiple_choice(
                question,
                options,
                correct_index,
                explanation,
                test_name,
                f"Comparing Numbers Q{len(rows) + 1}",
                path,
            )
        )
    question = "Select all the true statements."
    choices = ["45 > 40", "32 < 30", "28 = 28", "60 < 59"]
    correct_indices = [0, 2]
    explanation = "45 is greater than 40 and 28 equals 28; the other statements are false."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Comparing Numbers Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which number is greatest: 24, 42, or 34?"
    choices = ["42", "34", "24", "All the same"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "42 is the largest number listed.",
            test_name,
            f"Comparing Numbers Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def writing_numbers_questions():
    test_name = "Chapter 2: Number Writing and Recognition"
    path = "Chapter 2/Writing Numbers"
    rows = []
    numbers = [11, 24, 37, 42, 58, 63, 79]
    for idx, number in enumerate(numbers, 1):
        question = f"Which digit is in the tens place of {number}?"
        tens_digit = str(number // 10)
        ones_digit = str(number % 10)
        choices = [tens_digit, ones_digit, str((number // 10) + 1), str((number % 10) + 1)]
        explanation = f"The tens place of {number} is {tens_digit}."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                0,
                explanation,
                test_name,
                f"Writing Numbers Q{idx}",
                path,
            )
        )
    question_words = [
        ("Write the number for 'sixty-four'.", "64"),
        ("Write the number for 'ninety'.", "90"),
        ("Write the number for 'thirty-eight'.", "38"),
    ]
    for prompt, number in question_words:
        choices = [number, str(int(number) + 1), str(int(number) - 1), str(int(number) + 10)]
        explanation = f"'{prompt.split(' ')[-1]}' means {number}."
        rows.append(
            build_multiple_choice(
                prompt,
                choices,
                0,
                explanation,
                test_name,
                f"Writing Numbers Q{len(rows) + 1}",
                path,
            )
        )
    question = "Select all numbers written with three tens."
    choices = ["30", "34", "43", "24"]
    correct_indices = [0, 1]
    explanation = "Three tens means the number is in the 30s, so 30 and 34 have three tens."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Writing Numbers Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which shows the number sixty-seven?"
    choices = ["67", "76", "57", "60"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Sixty-seven means 6 tens and 7 ones, or 67.",
            test_name,
            f"Writing Numbers Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which number is written as seventy-two?"
    choices = ["72", "27", "70", "62"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Seventy-two is 72.",
            test_name,
            f"Writing Numbers Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all numbers that have 2 in the ones place."
    choices = ["12", "22", "32", "42"]
    correct_indices = [0, 1, 2, 3]
    explanation = "Each listed number ends in 2." 
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Writing Numbers Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which number word matches 54?"
    choices = ["Fifty-four", "Forty-five", "Sixty-four", "Fifty-five"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "54 is written as fifty-four.",
            test_name,
            f"Writing Numbers Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def ordering_numbers_questions():
    test_name = "Chapter 2: Number Writing and Recognition"
    path = "Chapter 2/Ordering Numbers"
    rows = []
    sequences = [
        ([67, 45, 89], "smallest to largest", [45, 67, 89]),
        ([12, 21, 18], "smallest to largest", [12, 18, 21]),
        ([93, 72, 85], "largest to smallest", [93, 85, 72]),
        ([34, 43, 41], "largest to smallest", [43, 41, 34]),
    ]
    for idx, (nums, order, correct_seq) in enumerate(sequences, 1):
        question = f"Order the numbers {nums[0]}, {nums[1]}, {nums[2]} from {order}."
        choice1 = ", ".join(str(n) for n in correct_seq)
        choice2 = ", ".join(str(n) for n in correct_seq[::-1])
        choice3 = ", ".join(str(n) for n in sorted(nums))
        choice4 = ", ".join(str(n) for n in sorted(nums, reverse=True))
        choices = [choice1, choice2, choice3, choice4]
        explanation = f"Comparing the numbers gives the order: {choice1}."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                0,
                explanation,
                test_name,
                f"Ordering Numbers Q{idx}",
                path,
            )
        )
    question_sets = [
        [14, 18, 16, 12],
        [55, 52, 59, 57],
        [81, 74, 79, 76],
        [23, 32, 28, 26],
    ]
    for numbers in question_sets:
        sorted_numbers = sorted(numbers)
        question = f"Which list shows the numbers {numbers} in order from least to greatest?"
        choices = [
            ", ".join(str(n) for n in sorted_numbers),
            ", ".join(str(n) for n in sorted_numbers[::-1]),
            ", ".join(str(n) for n in numbers),
            ", ".join(str(n) for n in numbers[::-1]),
        ]
        explanation = f"The numbers increase from {sorted_numbers[0]} to {sorted_numbers[-1]} in the correct list."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                0,
                explanation,
                test_name,
                f"Ordering Numbers Q{len(rows) + 1}",
                path,
            )
        )
    question = "Select all lists that are in order from greatest to least."
    choices = ["90, 80, 70", "31, 33, 35", "65, 60, 55", "42, 40, 50"]
    correct_indices = [0, 2]
    explanation = "Greatest to least means the numbers go down, which happens in 90, 80, 70 and 65, 60, 55."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Ordering Numbers Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which number would come between 44 and 46 on a number line?"
    choices = ["43", "45", "47", "49"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            1,
            "45 is between 44 and 46.",
            test_name,
            f"Ordering Numbers Q{len(rows) + 1}",
            path,
        )
    )
    question = "Order these numbers from least to greatest: 32, 28, 35."
    choices = ["28, 32, 35", "35, 32, 28", "32, 28, 35", "28, 35, 32"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "The numbers increase as 28, 32, 35.",
            test_name,
            f"Ordering Numbers Q{len(rows) + 1}",
            path,
        )
    )
    question = "Order these numbers from greatest to least: 91, 85, 88."
    choices = ["91, 88, 85", "85, 88, 91", "88, 91, 85", "91, 85, 88"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Greatest to least is 91, 88, 85.",
            test_name,
            f"Ordering Numbers Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all lists that are in order from least to greatest."
    choices = ["12, 18, 24", "24, 18, 12", "31, 35, 39", "39, 35, 31"]
    correct_indices = [0, 2]
    explanation = "Numbers increase in the least-to-greatest lists."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Ordering Numbers Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which number comes first when counting backward: 50, 49, 48?"
    choices = ["50", "49", "48", "47"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Counting backward starts at 50, then 49, 48.",
            test_name,
            f"Ordering Numbers Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all numbers that fit between 30 and 40."
    choices = ["33", "28", "37", "41"]
    correct_indices = [0, 2]
    explanation = "Numbers between 30 and 40 include 33 and 37."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Ordering Numbers Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def add_within_20_questions():
    test_name = "Chapter 3: Addition"
    path = "Chapter 3/Adding Within 20"
    rows = []
    problems = [
        (8, 6, 14),
        (9, 7, 16),
        (5, 4, 9),
        (12, 3, 15),
        (6, 8, 14),
        (7, 5, 12),
        (11, 6, 17),
        (13, 4, 17),
        (10, 9, 19),
    ]
    for idx, (a, b, total) in enumerate(problems, 1):
        question = f"What is {a} + {b}?"
        choices = [str(total), str(total - 1), str(total + 1), str(total - 2)]
        explanation = f"Adding {a} and {b} gives {total}."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                0,
                explanation,
                test_name,
                f"Addition Within 20 Q{idx}",
                path,
            )
        )
    question_sets = [
        ("Find the sum: 4 + 4 + 2", 10),
        ("Find the sum: 3 + 7 + 5", 15),
        ("Find the sum: 2 + 9 + 6", 17),
    ]
    for prompt, total in question_sets:
        choices = [str(total), str(total - 2), str(total + 2), str(total - 1)]
        explanation = f"Adding the numbers together gives {total}."
        rows.append(
            build_multiple_choice(
                prompt,
                choices,
                0,
                explanation,
                test_name,
                f"Addition Within 20 Q{len(rows) + 1}",
                path,
            )
        )
    question = "Select all number sentences that equal 12."
    choices = ["6 + 6", "9 + 2", "8 + 4", "5 + 7"]
    correct_indices = [0, 2, 3]
    explanation = "6 + 6, 8 + 4, and 5 + 7 each add to 12; 9 + 2 equals 11."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Addition Within 20 Q{len(rows) + 1}",
            path,
        )
    )
    question = "What number makes this true: 8 + __ = 15?"
    choices = ["7", "6", "8", "5"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            1,
            "15 - 8 = 7, so adding 7 makes 15.",
            test_name,
            f"Addition Within 20 Q{len(rows) + 1}",
            path,
        )
    )
    question = "What is 14 + 5?"
    choices = ["19", "18", "17", "20"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "14 plus 5 equals 19.",
            test_name,
            f"Addition Within 20 Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def fact_families_addition_questions():
    test_name = "Chapter 3: Addition"
    path = "Chapter 3/Addition Fact Families"
    rows = []
    families = [
        (5, 3, 8),
        (4, 6, 10),
        (7, 2, 9),
        (9, 1, 10),
        (8, 5, 13),
    ]
    for idx, (a, b, total) in enumerate(families, 1):
        question = f"Which fact belongs to the {a}, {b}, {total} family?"
        choices = [
            f"{a} + {b} = {total}",
            f"{total} + {a} = {b}",
            f"{b} - {a} = {total}",
            f"{a} + {total} = {b}",
        ]
        explanation = f"In the fact family, {a} + {b} = {total} is true."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                0,
                explanation,
                test_name,
                f"Addition Fact Family Q{idx}",
                path,
            )
        )
    question = "Select all number sentences in the 4, 5, 9 fact family."
    choices = [
        "4 + 5 = 9",
        "5 + 4 = 9",
        "9 + 4 = 5",
        "9 - 4 = 5",
    ]
    correct_indices = [0, 1, 3]
    explanation = "A fact family uses the same three numbers: 4 + 5 = 9, 5 + 4 = 9, and 9 - 4 = 5 fit."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Addition Fact Family Q{len(rows) + 1}",
            path,
        )
    )
    more_questions = [
        ("Which equation belongs to the 6, 7, 13 fact family?", [
            "6 + 7 = 13",
            "13 + 6 = 7",
            "7 - 6 = 13",
            "6 - 7 = 13",
        ], 0, "In the fact family, 6 + 7 = 13 is a true addition sentence."),
        ("Which number sentence is part of the 2, 8, 10 family?", [
            "2 + 8 = 10",
            "10 + 2 = 8",
            "8 - 2 = 10",
            "2 - 8 = 10",
        ], 0, "2 + 8 = 10 uses the numbers 2, 8, and 10 correctly."),
        ("In the 3, 9, 12 fact family, which subtraction sentence is true?", [
            "12 - 9 = 3",
            "12 - 3 = 10",
            "9 - 3 = 12",
            "3 - 12 = 9",
        ], 0, "12 - 9 = 3 uses the same family of numbers."),
        ("Which fact completes the 1, 7, 8 fact family?", [
            "7 + 1 = 8",
            "8 + 1 = 7",
            "8 - 7 = 1",
            "7 - 1 = 8",
        ], 0, "7 + 1 = 8 is the missing addition fact."),
    ]
    for prompt, choices, correct_index, explanation in more_questions:
        rows.append(
            build_multiple_choice(
                prompt,
                choices,
                correct_index,
                explanation,
                test_name,
                f"Addition Fact Family Q{len(rows) + 1}",
                path,
            )
        )
    question = "Which fact family do 9 + 0 = 9 and 9 - 9 = 0 belong to?"
    choices = ["0, 9, 9", "1, 8, 9", "4, 5, 9", "2, 7, 9"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Both sentences use the numbers 0, 9, and 9.",
            test_name,
            f"Addition Fact Family Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all true statements about the 5, 2, 7 fact family."
    choices = ["5 + 2 = 7", "7 - 5 = 2", "2 + 5 = 6", "7 - 2 = 5"]
    correct_indices = [0, 1, 3]
    explanation = "In the 5, 2, 7 family, the two addition and two subtraction facts are 5 + 2 = 7, 2 + 5 = 7, 7 - 5 = 2, and 7 - 2 = 5."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Addition Fact Family Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which fact belongs to the 3, 4, 7 fact family?"
    choices = ["3 + 4 = 7", "7 + 4 = 3", "4 - 3 = 7", "7 + 3 = 10"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "3 + 4 = 7 uses the numbers 3, 4, and 7.",
            test_name,
            f"Addition Fact Family Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all facts in the 2, 9, 11 fact family."
    choices = ["2 + 9 = 11", "9 + 2 = 11", "11 - 9 = 2", "11 + 2 = 13"]
    correct_indices = [0, 1, 2]
    explanation = "These addition and subtraction facts use 2, 9, and 11."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Addition Fact Family Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which subtraction sentence fits the 4, 1, 5 fact family?"
    choices = ["5 - 4 = 1", "5 - 1 = 4", "4 - 1 = 5", "1 - 5 = 4"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "5 - 4 = 1 belongs to the 4, 1, 5 family.",
            test_name,
            f"Addition Fact Family Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def making_ten_questions():
    test_name = "Chapter 3: Addition"
    path = "Chapter 3/Making Ten"
    rows = []
    pairs = [
        (7, 3, 11),
        (6, 4, 13),
        (8, 2, 12),
        (5, 5, 12),
        (9, 1, 11),
        (4, 6, 14),
    ]
    for idx, (a, helper, total) in enumerate(pairs, 1):
        question = f"Use making ten to solve {a} + {helper + (10 - a)}. What is the sum?"
        new_addend = helper + (10 - a)
        choices = [str(total), str(total - 1), str(total + 1), str(total - 2)]
        explanation = f"Make ten with {a} and {10 - a}, then add the rest to get {total}."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                0,
                explanation,
                test_name,
                f"Making Ten Q{idx}",
                path,
            )
        )
    question_sets = [
        ("Which pair makes a ten?", ["7 and 3", "6 and 5", "8 and 1", "4 and 7"], 0,
         "7 + 3 = 10."),
        ("To solve 9 + 5, which helper fact makes a ten?", ["9 + 1", "9 + 2", "9 + 3", "9 + 4"], 0,
         "Use 9 + 1 = 10, then add the rest of 5."),
        ("Which number combines with 2 to make 10?", ["8", "7", "6", "5"], 0,
         "2 + 8 = 10."),
        ("Which addition sentence uses making ten?", [
            "6 + 4 = 10, then 10 + 5 = 15",
            "6 + 2 = 9, then 9 + 5 = 14",
            "4 + 4 = 8, then 8 + 5 = 13",
            "7 + 7 = 14, then 14 + 1 = 15",
        ], 0, "6 + 4 makes 10, then add the rest."),
    ]
    for prompt, choices, correct_index, explanation in question_sets:
        rows.append(
            build_multiple_choice(
                prompt,
                choices,
                correct_index,
                explanation,
                test_name,
                f"Making Ten Q{len(rows) + 1}",
                path,
            )
        )
    question = "Select all pairs that add to 10."
    choices = ["1 and 9", "3 and 6", "4 and 6", "8 and 2"]
    correct_indices = [0, 3]
    explanation = "1 + 9 and 8 + 2 both equal 10."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Making Ten Q{len(rows) + 1}",
            path,
        )
    )
    question = "To solve 7 + 6, which step shows making ten?"
    choices = [
        "7 + 3 = 10, then 10 + 3 = 13",
        "7 + 7 = 14",
        "6 + 6 = 12",
        "7 + 2 = 9",
    ]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Use 7 + 3 to make 10, then add the leftover 3.",
            test_name,
            f"Making Ten Q{len(rows) + 1}",
            path,
        )
    )
    question = "What is 8 + 7 using making ten?"
    choices = ["15", "16", "14", "17"]
    explanation = "8 needs 2 to make 10. Split 7 into 2 and 5. 10 + 5 = 15."
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            explanation,
            test_name,
            f"Making Ten Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all numbers that pair with 9 to make 10."
    choices = ["1", "2", "3", "4"]
    correct_indices = [0]
    explanation = "Only 1 added to 9 makes 10."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Making Ten Q{len(rows) + 1}",
            path,
        )
    )
    question = "Using making ten, what is 6 + 8?"
    choices = ["14", "13", "15", "16"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "6 needs 4 to make 10. Split 8 into 4 and 4. 10 + 4 = 14.",
            test_name,
            f"Making Ten Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def addition_word_problem_questions():
    test_name = "Chapter 3: Addition"
    path = "Chapter 3/Addition Word Problems"
    rows = []
    scenarios = [
        ("Sally has 6 apples and buys 4 more. How many apples does she have now?", 10),
        ("There are 8 birds on a tree. 5 more birds join them. How many birds are there now?", 13),
        ("Mark has 7 cars and gets 6 more. How many cars does he have?", 13),
        ("A class has 9 boys and 8 girls. How many students are in the class?", 17),
        ("Lily collects 5 shells in the morning and 7 more in the afternoon. How many shells does she have?", 12),
        ("The library lent 4 books on Monday and 9 books on Tuesday. How many books were lent?", 13),
    ]
    for idx, (question, total) in enumerate(scenarios, 1):
        choices = [str(total), str(total - 1), str(total + 1), str(total - 2)]
        explanation = f"Adding the two amounts gives {total}."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                0,
                explanation,
                test_name,
                f"Addition Word Problem Q{idx}",
                path,
            )
        )
    more = [
        ("Mia sees 3 red birds and 6 blue birds. How many birds does she see?", 9),
        ("Tom has 5 stickers and wins 8 more. How many stickers does he have?", 13),
        ("A basket holds 7 green apples and 5 yellow apples. How many apples are in the basket?", 12),
        ("The art table has 4 paint brushes and 7 markers. How many tools are there?", 11),
        ("Dad baked 2 muffins in the morning and 9 in the afternoon. How many muffins did he bake?", 11),
        ("There are 6 kids on the swing and 5 more run over. How many kids are on the swing now?", 11),
    ]
    for question, total in more:
        choices = [str(total), str(total + 2), str(total - 1), str(total - 2)]
        explanation = f"Add the two parts to get {total}."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                0,
                explanation,
                test_name,
                f"Addition Word Problem Q{len(rows) + 1}",
                path,
            )
        )
    question = "Select all problems that need addition to solve."
    choices = [
        "You have 4 balloons and find 3 more.",
        "You have 8 crayons and give away 2.",
        "There are 5 cats and 5 kittens in a room.",
        "You start with 9 marbles and lose 4.",
    ]
    correct_indices = [0, 2]
    explanation = "Adding is used when combining amounts, like finding more balloons or total cats."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Addition Word Problem Q{len(rows) + 1}",
            path,
        )
    )
    question = "Maya picks 4 flowers and her friend picks 6. How many flowers do they have together?"
    choices = ["10", "9", "8", "12"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "4 + 6 = 10 flowers in all.",
            test_name,
            f"Addition Word Problem Q{len(rows) + 1}",
            path,
        )
    )
    question = "The class sees 7 butterflies and 5 more fly by. How many butterflies did they see?"
    choices = ["12", "11", "13", "14"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "7 + 5 = 12 butterflies.",
            test_name,
            f"Addition Word Problem Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def subtraction_within_20_questions():
    test_name = "Chapter 4: Subtraction"
    path = "Chapter 4/Subtraction Within 20"
    rows = []
    problems = [
        (17, 5, 12),
        (19, 7, 12),
        (15, 8, 7),
        (14, 6, 8),
        (13, 9, 4),
        (16, 4, 12),
        (12, 3, 9),
        (11, 6, 5),
        (18, 9, 9),
    ]
    for idx, (a, b, result) in enumerate(problems, 1):
        question = f"What is {a} - {b}?"
        choices = [str(result), str(result + 1), str(result - 1), str(result + 2)]
        explanation = f"Subtracting {b} from {a} leaves {result}."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                0,
                explanation,
                test_name,
                f"Subtraction Within 20 Q{idx}",
                path,
            )
        )
    multi_step = [
        ("Solve: 18 - 6 - 3", 9),
        ("Solve: 20 - 5 - 4", 11),
        ("Solve: 15 - 7 - 2", 6),
    ]
    for prompt, result in multi_step:
        choices = [str(result), str(result + 1), str(result - 1), str(result + 2)]
        explanation = f"Subtract each step to get {result}."
        rows.append(
            build_multiple_choice(
                prompt,
                choices,
                0,
                explanation,
                test_name,
                f"Subtraction Within 20 Q{len(rows) + 1}",
                path,
            )
        )
    question = "Select all differences that equal 8."
    choices = ["12 - 4", "15 - 7", "10 - 2", "18 - 10"]
    correct_indices = [0, 1]
    explanation = "12 - 4 and 15 - 7 each equal 8; the others do not."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Subtraction Within 20 Q{len(rows) + 1}",
            path,
        )
    )
    question = "What number makes this true: 14 - __ = 6?"
    choices = ["6", "8", "10", "4"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            1,
            "14 - 8 = 6 because 14 - 6 would be 8.",
            test_name,
            f"Subtraction Within 20 Q{len(rows) + 1}",
            path,
        )
    )
    question = "What is 20 - 11?"
    choices = ["9", "8", "10", "11"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Taking 11 away from 20 leaves 9.",
            test_name,
            f"Subtraction Within 20 Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def subtraction_fact_family_questions():
    test_name = "Chapter 4: Subtraction"
    path = "Chapter 4/Subtraction Fact Families"
    rows = []
    families = [
        (8, 3, 5),
        (9, 4, 5),
        (10, 6, 4),
        (12, 7, 5),
        (11, 2, 9),
    ]
    for idx, (whole, part1, part2) in enumerate(families, 1):
        question = f"Which subtraction fact belongs to the {part1}, {part2}, {whole} family?"
        choices = [
            f"{whole} - {part1} = {part2}",
            f"{part1} - {part2} = {whole}",
            f"{part2} - {whole} = {part1}",
            f"{whole} + {part1} = {part2}",
        ]
        explanation = f"In this fact family, {whole} - {part1} = {part2} is true."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                0,
                explanation,
                test_name,
                f"Subtraction Fact Family Q{idx}",
                path,
            )
        )
    question = "Select all facts in the 7, 4, 3 family."
    choices = [
        "7 - 4 = 3",
        "7 - 3 = 4",
        "4 + 3 = 8",
        "3 + 4 = 7",
    ]
    correct_indices = [0, 1, 3]
    explanation = "The family uses the numbers 7, 4, and 3 in both addition and subtraction."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Subtraction Fact Family Q{len(rows) + 1}",
            path,
        )
    )
    more = [
        ("Which equation belongs to the 10, 3, 7 fact family?", [
            "10 - 3 = 7",
            "7 - 3 = 10",
            "3 - 7 = 10",
            "10 + 7 = 3",
        ], 0, "10 - 3 = 7 uses the numbers correctly."),
        ("Which subtraction sentence fits the 9, 2, 7 family?", [
            "9 - 2 = 7",
            "7 - 2 = 9",
            "9 - 7 = 1",
            "2 - 9 = 7",
        ], 0, "In the 9, 2, 7 family, 9 - 2 = 7 is correct."),
        ("Which fact completes the 6, 1, 5 fact family?", [
            "6 - 1 = 5",
            "5 - 1 = 6",
            "1 - 6 = 5",
            "6 + 1 = 5",
        ], 0, "6 - 1 = 5 is the related subtraction fact."),
        ("In the 8, 6, 2 fact family, which addition sentence is true?", [
            "6 + 2 = 8",
            "8 + 2 = 6",
            "6 - 2 = 8",
            "2 - 6 = 8",
        ], 0, "6 + 2 = 8 uses all three numbers."),
        ("Which set of numbers could be a fact family?", [
            "5, 4, 9",
            "6, 6, 12",
            "7, 1, 9",
            "8, 0, 8",
        ], 3, "8, 0, 8 works because 8 - 0 = 8 and 8 - 8 = 0."),
        ("Which subtraction sentence belongs to the 13, 5, 8 family?", [
            "13 - 5 = 8",
            "8 - 5 = 13",
            "5 - 8 = 13",
            "13 + 5 = 8",
        ], 0, "13 - 5 = 8 uses all three numbers correctly."),
        ("What addition fact matches the 9, 6, 3 family?", [
            "6 + 3 = 9",
            "9 + 3 = 6",
            "3 + 9 = 12",
            "9 - 6 = 3",
        ], 0, "6 + 3 = 9 is part of the fact family."),
        ("Which equation is missing from the 4, 2, 6 fact family?", [
            "6 - 2 = 4",
            "4 - 2 = 2",
            "6 + 2 = 4",
            "2 - 4 = 6",
        ], 0, "6 - 2 = 4 completes the family."),
    ]
    for prompt, choices, correct_index, explanation in more:
        rows.append(
            build_multiple_choice(
                prompt,
                choices,
                correct_index,
                explanation,
                test_name,
                f"Subtraction Fact Family Q{len(rows) + 1}",
                path,
            )
        )
    question = "Select all true statements about the 12, 5, 7 fact family."
    choices = ["12 - 5 = 7", "7 + 5 = 12", "5 + 7 = 11", "12 - 7 = 5"]
    correct_indices = [0, 1, 3]
    explanation = "The family uses 12, 5, and 7 in both addition and subtraction correctly."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Subtraction Fact Family Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def subtraction_word_problem_questions():
    test_name = "Chapter 4: Subtraction"
    path = "Chapter 4/Subtraction Word Problems"
    rows = []
    scenarios = [
        ("There were 10 birds. 3 flew away. How many are left?", 7),
        ("Jake had 15 balloons. 6 popped. How many balloons remain?", 9),
        ("A basket held 12 apples. 5 were eaten. How many apples are still there?", 7),
        ("Rosa had 18 stickers and gave 9 to her friend. How many stickers does she have now?", 9),
        ("A gardener planted 16 flowers. 4 wilted. How many flowers still bloom?", 12),
        ("A shelf had 14 books. 7 were checked out. How many books are on the shelf now?", 7),
    ]
    for idx, (question, result) in enumerate(scenarios, 1):
        choices = [str(result), str(result + 1), str(result - 1), str(result + 2)]
        explanation = f"Take away to find {result}."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                0,
                explanation,
                test_name,
                f"Subtraction Word Problem Q{idx}",
                path,
            )
        )
    more = [
        ("Ella baked 9 cookies and gave 4 to friends. How many cookies does she have?", 5),
        ("There are 13 fish in a tank. 5 are moved to another tank. How many remain?", 8),
        ("A park had 17 swings. 8 were taken down. How many swings are left?", 9),
        ("Liam had 11 crayons. He lost 6 of them. How many crayons does he still have?", 5),
        ("The class had 20 glue sticks. They used 9. How many are left?", 11),
        ("There were 18 cupcakes. 7 were eaten. How many cupcakes remain?", 11),
        ("A jar held 16 candies. 8 were given away. How many candies are still in the jar?", 8),
        ("A train started with 14 passengers. 5 got off at the next stop. How many passengers remain?", 9),
    ]
    for question, result in more:
        choices = [str(result), str(result + 2), str(result - 2), str(result + 1)]
        explanation = f"Subtract to find that {result} remain."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                0,
                explanation,
                test_name,
                f"Subtraction Word Problem Q{len(rows) + 1}",
                path,
            )
        )
    question = "Select all stories that use subtraction."
    choices = [
        "You pick 5 flowers and then pick 3 more.",
        "You have 12 balloons and 4 float away.",
        "There are 7 apples and 6 more are delivered.",
        "You start with 14 marbles and give 5 away.",
    ]
    correct_indices = [1, 3]
    explanation = "Subtraction is used when taking away, like losing balloons or giving away marbles."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Subtraction Word Problem Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def adding_tens_questions():
    test_name = "Chapter 5: Addition & Subtraction to 100"
    path = "Chapter 5/Adding Tens"
    rows = []
    tens_problems = [
        (30, 20, 50),
        (40, 30, 70),
        (10, 60, 70),
        (50, 40, 90),
        (20, 20, 40),
        (60, 30, 90),
        (70, 10, 80),
    ]
    for idx, (a, b, total) in enumerate(tens_problems, 1):
        question = f"What is {a} + {b}?"
        choices = [str(total), str(total - 10), str(total + 10), str(total - 20)]
        explanation = f"Add the tens: {a} + {b} = {total}."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                0,
                explanation,
                test_name,
                f"Adding Tens Q{idx}",
                path,
            )
        )
    question_sets = [
        ("Which equation shows adding tens?", [
            "30 + 40 = 70",
            "35 + 4 = 39",
            "27 + 10 = 37",
            "16 + 3 = 19",
        ], 0, "Adding tens means both addends are tens."),
        ("Add 20 + 50.", ["70", "60", "80", "90"], 0, "20 plus 50 equals 70."),
        ("Add 80 + 10.", ["90", "70", "100", "95"], 0, "80 + 10 = 90."),
        ("Select all sums that equal 100.", ["60 + 40", "70 + 20", "80 + 30", "50 + 50"], [0, 3],
         "60 + 40 and 50 + 50 each equal 100."),
    ]
    for item in question_sets:
        if isinstance(item[2], list):
            prompt, choices, correct_indices, explanation = item
            rows.append(
                build_select_all(
                    prompt,
                    choices,
                    correct_indices,
                    explanation,
                    test_name,
                    f"Adding Tens Q{len(rows) + 1}",
                    path,
                )
            )
        else:
            prompt, choices, correct_index, explanation = item
            rows.append(
                build_multiple_choice(
                    prompt,
                    choices,
                    correct_index,
                    explanation,
                    test_name,
                    f"Adding Tens Q{len(rows) + 1}",
                    path,
                )
            )
    question = "What is 90 + 10?"
    choices = ["100", "90", "110", "80"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Adding another ten to 90 makes 100.",
            test_name,
            f"Adding Tens Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all equations that add only tens."
    choices = ["40 + 20", "25 + 10", "70 + 30", "18 + 12"]
    correct_indices = [0, 2]
    explanation = "40 + 20 and 70 + 30 use only tens."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Adding Tens Q{len(rows) + 1}",
            path,
        )
    )
    question = "Find the sum: 60 + 20."
    choices = ["80", "70", "90", "100"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "60 plus 20 equals 80.",
            test_name,
            f"Adding Tens Q{len(rows) + 1}",
            path,
        )
    )
    question = "What is 30 + 50?"
    choices = ["80", "70", "60", "90"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Adding three tens and five tens equals 80.",
            test_name,
            f"Adding Tens Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def subtracting_tens_questions():
    test_name = "Chapter 5: Addition & Subtraction to 100"
    path = "Chapter 5/Subtracting Tens"
    rows = []
    problems = [
        (90, 40, 50),
        (80, 30, 50),
        (70, 20, 50),
        (60, 10, 50),
        (100, 30, 70),
        (50, 20, 30),
        (90, 60, 30),
    ]
    for idx, (a, b, result) in enumerate(problems, 1):
        question = f"What is {a} - {b}?"
        choices = [str(result), str(result + 10), str(result - 10), str(result + 20)]
        explanation = f"Subtract the tens: {a} - {b} = {result}."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                0,
                explanation,
                test_name,
                f"Subtracting Tens Q{idx}",
                path,
            )
        )
    question_sets = [
        ("Which equation shows subtracting tens?", [
            "80 - 20 = 60",
            "82 - 2 = 80",
            "54 - 4 = 50",
            "37 - 7 = 30",
        ], 0, "Subtracting tens uses multiples of ten."),
        ("What is 60 - 50?", ["10", "15", "5", "20"], 0, "60 minus 50 equals 10."),
        ("Subtract 40 from 70.", ["30", "40", "20", "50"], 0, "70 - 40 = 30."),
        ("Select all differences that equal 20.", ["50 - 30", "80 - 60", "70 - 40", "90 - 80"], [0, 1, 2],
         "The differences of 50 - 30, 80 - 60, and 70 - 40 are each 20."),
    ]
    for item in question_sets:
        if isinstance(item[2], list):
            prompt, choices, correct_indices, explanation = item
            rows.append(
                build_select_all(
                    prompt,
                    choices,
                    correct_indices,
                    explanation,
                    test_name,
                    f"Subtracting Tens Q{len(rows) + 1}",
                    path,
                )
            )
        else:
            prompt, choices, correct_index, explanation = item
            rows.append(
                build_multiple_choice(
                    prompt,
                    choices,
                    correct_index,
                    explanation,
                    test_name,
                    f"Subtracting Tens Q{len(rows) + 1}",
                    path,
                )
            )
    question = "What is 100 - 40?"
    choices = ["60", "70", "80", "90"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Taking away 40 from 100 leaves 60.",
            test_name,
            f"Subtracting Tens Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all subtraction problems that use only tens."
    choices = ["70 - 30", "65 - 5", "90 - 40", "82 - 12"]
    correct_indices = [0, 2]
    explanation = "70 - 30 and 90 - 40 both subtract multiples of ten."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Subtracting Tens Q{len(rows) + 1}",
            path,
        )
    )
    question = "Find the difference: 120 - 50."
    choices = ["70", "60", "80", "90"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Subtracting 50 tens from 120 leaves 70.",
            test_name,
            f"Subtracting Tens Q{len(rows) + 1}",
            path,
        )
    )
    question = "What is 60 - 20?"
    choices = ["40", "50", "30", "20"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "60 minus 20 leaves 40.",
            test_name,
            f"Subtracting Tens Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def two_digit_plus_one_digit_questions():
    test_name = "Chapter 5: Addition & Subtraction to 100"
    path = "Chapter 5/Two-Digit Plus One-Digit"
    rows = []
    problems = [
        (43, 6, 49),
        (58, 7, 65),
        (67, 5, 72),
        (24, 9, 33),
        (35, 8, 43),
        (72, 4, 76),
        (86, 3, 89),
        (49, 2, 51),
    ]
    for idx, (a, b, total) in enumerate(problems, 1):
        question = f"What is {a} + {b}?"
        choices = [str(total), str(total - 1), str(total + 1), str(total - 2)]
        explanation = f"Add the ones to get {total}."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                0,
                explanation,
                test_name,
                f"Two-Digit Plus One-Digit Q{idx}",
                path,
            )
        )
    regroup = [
        ("Solve: 57 + 6", 63),
        ("Solve: 68 + 5", 73),
        ("Solve: 29 + 8", 37),
    ]
    for prompt, total in regroup:
        choices = [str(total), str(total - 1), str(total + 1), str(total - 2)]
        explanation = f"Add the one-digit number to the ones place to get {total}."
        rows.append(
            build_multiple_choice(
                prompt,
                choices,
                0,
                explanation,
                test_name,
                f"Two-Digit Plus One-Digit Q{len(rows) + 1}",
                path,
            )
        )
    question = "Select all sums greater than 70."
    choices = ["64 + 7", "52 + 4", "68 + 5", "45 + 9"]
    correct_indices = [0, 2]
    explanation = "64 + 7 = 71 and 68 + 5 = 73 are greater than 70."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Two-Digit Plus One-Digit Q{len(rows) + 1}",
            path,
        )
    )
    question = "What is 34 + 7?"
    choices = ["41", "39", "42", "40"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Add 7 ones to 34 to get 41.",
            test_name,
            f"Two-Digit Plus One-Digit Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which equation shows a two-digit number plus a one-digit number?"
    choices = ["43 + 5", "30 + 40", "18 + 12", "55 + 20"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "43 is a two-digit number and 5 is a one-digit number.",
            test_name,
            f"Two-Digit Plus One-Digit Q{len(rows) + 1}",
            path,
        )
    )
    question = "Find the sum: 75 + 4."
    choices = ["79", "78", "80", "81"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Add 4 ones to 75 to get 79.",
            test_name,
            f"Two-Digit Plus One-Digit Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def shapes_2d_questions():
    test_name = "Chapter 6: Geometry"
    path = "Chapter 6/2D Shapes"
    rows = []
    questions = [
        ("Which shape has 3 sides?", ["Triangle", "Square", "Circle", "Rectangle"], 0,
         "A triangle has exactly three sides."),
        ("Which shape has 4 equal sides?", ["Square", "Rectangle", "Triangle", "Hexagon"], 0,
         "A square has four equal sides."),
        ("Which shape is round with no corners?", ["Circle", "Triangle", "Rectangle", "Hexagon"], 0,
         "A circle is round with no corners."),
        ("Which shape has 6 sides?", ["Hexagon", "Square", "Triangle", "Circle"], 0,
         "A hexagon has six sides."),
        ("Which shape has two long sides and two short sides?", ["Rectangle", "Square", "Triangle", "Circle"], 0,
         "A rectangle has two long and two short sides."),
        ("Which shape has only one curved side?", ["Circle", "Triangle", "Rectangle", "Square"], 0,
         "A circle has one continuous curved side."),
        ("How many corners does a triangle have?", ["3", "4", "5", "6"], 0,
         "A triangle has three corners."),
        ("How many sides does a rectangle have?", ["4", "3", "5", "6"], 0,
         "A rectangle has four sides."),
        ("Which shape has no straight sides?", ["Circle", "Triangle", "Square", "Rectangle"], 0,
         "A circle has no straight sides."),
        ("Which shape is shown by a stop sign?", ["Octagon", "Hexagon", "Square", "Triangle"], 0,
         "A stop sign is an octagon."),
    ]
    for idx, (question, choices, correct_index, explanation) in enumerate(questions, 1):
        rows.append(
            build_multiple_choice(
                question,
                choices,
                correct_index,
                explanation,
                test_name,
                f"2D Shapes Q{idx}",
                path,
            )
        )
    question = "Select all shapes that have 4 sides."
    choices = ["Square", "Rectangle", "Triangle", "Circle"]
    correct_indices = [0, 1]
    explanation = "Squares and rectangles both have four sides."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"2D Shapes Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which shape has 5 sides?"
    choices = ["Pentagon", "Hexagon", "Square", "Triangle"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "A pentagon has five sides.",
            test_name,
            f"2D Shapes Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all shapes that have corners."
    choices = ["Triangle", "Circle", "Rectangle", "Oval"]
    correct_indices = [0, 2]
    explanation = "Triangles and rectangles have corners; circles and ovals do not."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"2D Shapes Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which shape can be split into two equal triangles?"
    choices = ["Square", "Circle", "Pentagon", "Oval"]
    explanation = "Cutting a square along a diagonal makes two equal triangles."
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            explanation,
            test_name,
            f"2D Shapes Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which shape looks like a slice of pizza?"
    choices = ["Triangle", "Rectangle", "Circle", "Square"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "A pizza slice is shaped like a triangle.",
            test_name,
            f"2D Shapes Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def shapes_3d_questions():
    test_name = "Chapter 6: Geometry"
    path = "Chapter 6/3D Shapes"
    rows = []
    questions = [
        ("Which 3D shape rolls easily?", ["Sphere", "Cube", "Cylinder", "Cone"], 0,
         "A sphere rolls because it is round."),
        ("Which shape has flat square faces?", ["Cube", "Sphere", "Cone", "Cylinder"], 0,
         "A cube has six square faces."),
        ("Which shape has a circular base and a point?", ["Cone", "Cylinder", "Sphere", "Cube"], 0,
         "A cone has a circular base and a vertex at the top."),
        ("Which shape looks like a can?", ["Cylinder", "Cube", "Cone", "Sphere"], 0,
         "A can is shaped like a cylinder."),
        ("Which shape has 6 faces, 8 vertices, and 12 edges?", ["Rectangular prism", "Sphere", "Cone", "Cylinder"], 0,
         "A rectangular prism has those features."),
        ("Which shape has no edges or vertices?", ["Sphere", "Cube", "Cylinder", "Cone"], 0,
         "A sphere has no edges or corners."),
        ("Which shape has two circular faces?", ["Cylinder", "Cone", "Cube", "Rectangular prism"], 0,
         "A cylinder has two circular faces."),
        ("Which shape looks like a box?", ["Rectangular prism", "Sphere", "Cone", "Cylinder"], 0,
         "Boxes are shaped like rectangular prisms."),
        ("Which shape has a curved surface and a flat circle face?", ["Cone", "Cube", "Sphere", "Cylinder"], 0,
         "A cone has one curved surface and one circular face."),
        ("Which shape is shaped like a dice?", ["Cube", "Sphere", "Cone", "Cylinder"], 0,
         "A die is a cube."),
    ]
    for idx, (question, choices, correct_index, explanation) in enumerate(questions, 1):
        rows.append(
            build_multiple_choice(
                question,
                choices,
                correct_index,
                explanation,
                test_name,
                f"3D Shapes Q{idx}",
                path,
            )
        )
    question = "Select all shapes that stack without rolling."
    choices = ["Cube", "Sphere", "Cylinder", "Rectangular prism"]
    correct_indices = [0, 3]
    explanation = "Cubes and rectangular prisms have flat faces that stack easily."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"3D Shapes Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which shape looks like an ice cream cone?"
    choices = ["Cone", "Sphere", "Cylinder", "Cube"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Ice cream cones are shaped like cones.",
            test_name,
            f"3D Shapes Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all shapes with curved surfaces."
    choices = ["Sphere", "Cube", "Cone", "Cylinder"]
    correct_indices = [0, 2, 3]
    explanation = "Spheres, cones, and cylinders each have curved surfaces."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"3D Shapes Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which shape has all faces shaped like rectangles?"
    choices = ["Rectangular prism", "Cube", "Sphere", "Cone"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "A rectangular prism has rectangular faces.",
            test_name,
            f"3D Shapes Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which 3D shape matches a basketball?"
    choices = ["Sphere", "Cube", "Cylinder", "Cone"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "A basketball is a sphere.",
            test_name,
            f"3D Shapes Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def partitioning_shapes_questions():
    test_name = "Chapter 6: Geometry"
    path = "Chapter 6/Partitioning Shapes"
    rows = []
    questions = [
        ("Cutting a square into 2 equal pieces makes what?", ["Halves", "Quarters", "Thirds", "Sixths"], 0,
         "Two equal pieces are halves."),
        ("If a circle is split into 4 equal parts, what are the parts called?", ["Quarters", "Halves", "Thirds", "Eighths"], 0,
         "Four equal parts are quarters."),
        ("Which picture shows a shape partitioned into halves?", ["2 equal parts", "3 equal parts", "4 equal parts", "5 equal parts"], 0,
         "Halves means 2 equal parts."),
        ("How many pieces are there when a rectangle is cut into quarters?", ["4", "2", "3", "5"], 0,
         "Quarters means 4 pieces."),
        ("If a pizza is cut into 2 equal slices, what fraction is each slice?", ["1/2", "1/4", "1/3", "1/8"], 0,
         "Each slice is one half."),
        ("If a square is cut into 4 equal parts, what fraction is one part?", ["1/4", "1/2", "1/3", "1/6"], 0,
         "One out of four equal parts is one quarter."),
        ("Which fraction shows two halves of a shape?", ["2/2", "1/2", "1/4", "3/4"], 0,
         "Two halves make the whole, written 2/2."),
        ("How many halves make a whole?", ["2", "3", "4", "5"], 0,
         "Two halves equal one whole."),
        ("How many quarters make a whole?", ["4", "2", "3", "5"], 0,
         "Four quarters equal one whole."),
        ("If you shade 2 of the 4 equal parts, what fraction is shaded?", ["2/4", "1/4", "1/2", "3/4"], 0,
         "Two out of four parts is 2/4, equal to 1/2."),
    ]
    for idx, (question, choices, correct_index, explanation) in enumerate(questions, 1):
        rows.append(
            build_multiple_choice(
                question,
                choices,
                correct_index,
                explanation,
                test_name,
                f"Partitioning Shapes Q{idx}",
                path,
            )
        )
    question = "Select all shapes that are divided into equal halves."
    choices = ["Two equal rectangles", "Two different-sized parts", "Two equal circles", "One large and one small part"]
    correct_indices = [0, 2]
    explanation = "Equal halves must be the same size."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Partitioning Shapes Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all shapes that show quarters."
    choices = ["4 equal squares", "3 equal parts", "4 equal triangles", "2 equal parts"]
    correct_indices = [0, 2]
    explanation = "Quarters mean four equal parts."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Partitioning Shapes Q{len(rows) + 1}",
            path,
        )
    )
    question = "If you eat 1 of 2 equal pieces of cake, what fraction did you eat?"
    choices = ["1/2", "1/4", "2/4", "2/2"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Eating 1 of 2 equal pieces is one half.",
            test_name,
            f"Partitioning Shapes Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which sentence is true about halves?"
    choices = ["Two halves make a whole", "One half is bigger than the whole", "Halves mean three parts", "Halves are uneven parts"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Two halves make one whole.",
            test_name,
            f"Partitioning Shapes Q{len(rows) + 1}",
            path,
        )
    )
    question = "What fraction of a shape is shaded if 3 of 4 equal parts are colored?"
    choices = ["3/4", "1/4", "1/2", "4/4"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Three parts out of four equal parts is 3/4.",
            test_name,
            f"Partitioning Shapes Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def length_measurement_questions():
    test_name = "Chapter 7: Measurement"
    path = "Chapter 7/Length"
    rows = []
    questions = [
        ("Which object is longer?", ["Jump rope", "Eraser", "Paper clip", "Button"], 0,
         "A jump rope is longer than small items."),
        ("Which tool measures length best?", ["Ruler", "Clock", "Scale", "Thermometer"], 0,
         "A ruler measures length."),
        ("Which line is longer?", ["Line A", "Line B", "Line C", "Line D"], 0,
         "Line A is the longest line shown."),
        ("Which object is shorter?", ["Crayon", "Baseball bat", "Jump rope", "Garden hose"], 0,
         "A crayon is shorter than the other items."),
        ("What word describes a stick that measures more distance?", ["Longer", "Shorter", "Heavier", "Lighter"], 0,
         "A stick measuring more distance is longer."),
        ("If a pencil is longer than a crayon, which is shorter?", ["Crayon", "Pencil", "They are the same", "Both are longer"], 0,
         "The crayon is shorter."),
        ("Which object would be best to measure with a meter stick?", ["Classroom wall", "Paper clip", "Sticker", "Coin"], 0,
         "A meter stick measures longer objects like walls."),
        ("Which animal has the longer tail?", ["Squirrel", "Mouse", "Hamster", "Chipmunk"], 0,
         "A squirrel has a longer tail than the others listed."),
        ("When something measures fewer units, what word describes it?", ["Shorter", "Longer", "Heavier", "Taller"], 0,
         "Fewer units means it is shorter."),
        ("Which comparison is true?", ["A book is longer than a bookmark", "A bookmark is longer than a book", "A pencil is longer than a desk", "A desk is shorter than a pencil"], 0,
         "A book is longer than a bookmark."),
    ]
    for idx, (question, choices, correct_index, explanation) in enumerate(questions, 1):
        rows.append(
            build_multiple_choice(
                question,
                choices,
                correct_index,
                explanation,
                test_name,
                f"Length Q{idx}",
                path,
            )
        )
    question = "Select all objects that are longer than a pencil."
    choices = ["Baseball bat", "Crayon", "Jump rope", "Sticker"]
    correct_indices = [0, 2]
    explanation = "A bat and jump rope are longer than a pencil."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Length Q{len(rows) + 1}",
            path,
        )
    )
    question = "How many paper clips long is the pencil?"
    choices = ["5", "3", "7", "9"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "The pencil measures 5 paper clips in the example.",
            test_name,
            f"Length Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all comparisons that show shorter."
    choices = ["The ribbon is shorter than the rope", "The rope is shorter than the ribbon", "The pencil is shorter than the marker", "The marker is shorter than the pencil"]
    correct_indices = [0, 2]
    explanation = "Statements using 'shorter than' correctly compare items." 
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Length Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which tool would you use to compare the length of two sticks?"
    choices = ["Ruler", "Clock", "Scale", "Measuring cup"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "A ruler helps compare lengths of sticks.",
            test_name,
            f"Length Q{len(rows) + 1}",
            path,
        )
    )
    question = "If a ribbon measures 12 inches and a string measures 15 inches, which is longer?"
    choices = ["String", "Ribbon", "They are equal", "Cannot tell"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "15 inches is longer than 12 inches, so the string is longer.",
            test_name,
            f"Length Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def height_measurement_questions():
    test_name = "Chapter 7: Measurement"
    path = "Chapter 7/Height"
    rows = []
    questions = [
        ("Which child is taller?", ["Child A", "Child B", "Child C", "Child D"], 0,
         "Child A is the tallest in the picture."),
        ("Which word describes someone who is not tall?", ["Shorter", "Taller", "Heavier", "Longer"], 0,
         "Someone who is not tall is shorter."),
        ("Which object is the tallest?", ["Lamp", "Book", "Pencil", "Cup"], 0,
         "A lamp is taller than the other objects listed."),
        ("Which tool would measure height best?", ["Yardstick", "Clock", "Scale", "Thermometer"], 0,
         "A yardstick measures height."),
        ("If a plant grows taller each day, what happens to its height?", ["It increases", "It decreases", "It stays the same", "It disappears"], 0,
         "Growing taller means the height increases."),
        ("Which animal is shorter?", ["Cat", "Giraffe", "Horse", "Cow"], 0,
         "A cat is shorter than the other animals listed."),
        ("When measuring height, where do you start?", ["At the bottom", "In the middle", "At the top", "Wherever you want"], 0,
         "You start measuring from the bottom."),
        ("Which word compares height correctly?", ["The tree is taller than the bush", "The bush is taller than the tree", "The flower is taller than the house", "The house is shorter than the ant"], 0,
         "The tree is taller than the bush."),
        ("Which object would you describe as short?", ["Stool", "Flagpole", "Streetlight", "Skyscraper"], 0,
         "A stool is short compared to the others."),
        ("Which comparison is true about height?", ["A chair is shorter than a door", "A door is shorter than a chair", "A bookshelf is shorter than a pencil", "A giraffe is shorter than a rabbit"], 0,
         "A chair is shorter than a door."),
    ]
    for idx, (question, choices, correct_index, explanation) in enumerate(questions, 1):
        rows.append(
            build_multiple_choice(
                question,
                choices,
                correct_index,
                explanation,
                test_name,
                f"Height Q{idx}",
                path,
            )
        )
    question = "Select all things that are tall."
    choices = ["Tree", "Pencil", "Skyscraper", "Cup"]
    correct_indices = [0, 2]
    explanation = "Trees and skyscrapers are tall objects."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Height Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all comparisons that show shorter."
    choices = ["The bush is shorter than the tree", "The tree is shorter than the bush", "The chair is shorter than the table", "The table is shorter than the chair"]
    correct_indices = [0, 2]
    explanation = "Correct statements use 'shorter than' properly."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Height Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which tool helps measure a student's height?"
    choices = ["Measuring tape", "Clock", "Thermometer", "Scale"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "A measuring tape can check a student's height.",
            test_name,
            f"Height Q{len(rows) + 1}",
            path,
        )
    )
    question = "If Sam is taller than Ana and shorter than Luis, who is the tallest?"
    choices = ["Luis", "Sam", "Ana", "Sam and Ana"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Luis is taller than Sam and Ana.",
            test_name,
            f"Height Q{len(rows) + 1}",
            path,
        )
    )
    question = "If a tree is 20 feet tall and a bush is 6 feet tall, which is shorter?"
    choices = ["Bush", "Tree", "They are the same", "Cannot tell"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "6 feet is shorter than 20 feet, so the bush is shorter.",
            test_name,
            f"Height Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def weight_measurement_questions():
    test_name = "Chapter 7: Measurement"
    path = "Chapter 7/Weight"
    rows = []
    questions = [
        ("Which object is heavier?", ["Bowling ball", "Feather", "Paper", "Leaf"], 0,
         "A bowling ball is heavier than a feather, paper, or leaf."),
        ("Which tool measures weight?", ["Scale", "Ruler", "Clock", "Thermometer"], 0,
         "A scale measures weight."),
        ("Which is lighter?", ["Balloon", "Rock", "Brick", "Book"], 0,
         "A balloon is lighter than the other items listed."),
        ("If two bags weigh the same, what are they?", ["Equal", "Heavier", "Lighter", "Shorter"], 0,
         "When weights match, they are equal."),
        ("Which animal is heavier?", ["Elephant", "Rabbit", "Cat", "Dog"], 0,
         "An elephant is heavier than the others listed."),
        ("Which food is lighter?", ["Lettuce leaf", "Watermelon", "Pumpkin", "Melon"], 0,
         "A lettuce leaf is lighter."),
        ("Which description is true?", ["A backpack is heavier than a pencil", "A pencil is heavier than a backpack", "A feather is heavier than a brick", "A cloud is heavier than a rock"], 0,
         "A backpack weighs more than a pencil."),
        ("Which tool shows that two objects balance?", ["Balance scale", "Ruler", "Timer", "Measuring cup"], 0,
         "A balance scale shows equal weight."),
        ("Which object would be light to carry?", ["Book", "Feather", "Brick", "Basketball"], 1,
         "A feather is very light."),
        ("Which comparison is correct about weight?", ["A rock is heavier than a leaf", "A leaf is heavier than a rock", "A coin is heavier than a bowling ball", "A pillow is heavier than a table"], 0,
         "A rock weighs more than a leaf."),
    ]
    for idx, (question, choices, correct_index, explanation) in enumerate(questions, 1):
        rows.append(
            build_multiple_choice(
                question,
                choices,
                correct_index,
                explanation,
                test_name,
                f"Weight Q{idx}",
                path,
            )
        )
    question = "Select all objects that are heavy."
    choices = ["Boulder", "Feather", "Elephant", "Paper clip"]
    correct_indices = [0, 2]
    explanation = "A boulder and elephant are heavy objects."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Weight Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all objects that are light."
    choices = ["Balloon", "Bowling ball", "Leaf", "Brick"]
    correct_indices = [0, 2]
    explanation = "Balloons and leaves are light." 
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Weight Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which tool helps compare the weight of two toys?"
    choices = ["Balance scale", "Ruler", "Clock", "Thermometer"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "A balance scale compares weights.",
            test_name,
            f"Weight Q{len(rows) + 1}",
            path,
        )
    )
    question = "If one box feels lighter than another, which is heavier?"
    choices = ["The other box", "The first box", "They are equal", "Neither box"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "If one box is lighter, the other is heavier.",
            test_name,
            f"Weight Q{len(rows) + 1}",
            path,
        )
    )
    question = "If a pumpkin weighs 10 pounds and an apple weighs 1 pound, which is lighter?"
    choices = ["Apple", "Pumpkin", "They weigh the same", "Cannot tell"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "1 pound is lighter than 10 pounds.",
            test_name,
            f"Weight Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def nonstandard_units_questions():
    test_name = "Chapter 7: Measurement"
    path = "Chapter 7/Non-standard Units"
    rows = []
    questions = [
        ("Which item is best for measuring a desk using non-standard units?", ["Paper clips", "Marbles", "Buttons", "Coins"], 0,
         "Paper clips can line up along a desk."),
        ("How many blocks long is the book?", ["4", "5", "6", "7"], 1,
         "The book measures 5 blocks in the example."),
        ("Which unit would you use to measure a classroom door without a ruler?", ["Linking cubes", "Stickers", "Beans", "Beads"], 0,
         "Linking cubes stack to measure height."),
        ("When using paper clips to measure, where should they touch?", ["End to end", "On top", "Far apart", "Stacked"], 0,
         "Paper clips must be end to end."),
        ("If a pencil measures 6 cubes and an eraser measures 3 cubes, which is longer?", ["Pencil", "Eraser", "They are equal", "Cannot tell"], 0,
         "6 cubes is longer than 3 cubes."),
        ("Which word describes counting how many footsteps long the hallway is?", ["Measuring", "Drawing", "Reading", "Writing"], 0,
         "Counting footsteps is measuring length."),
        ("Which objects work best for measuring length without standard tools?", ["Paper clips", "Lego bricks", "Crayons", "All of the above"], 3,
         "Different small items can be used as units."),
        ("Why should the units be the same size?", ["To make fair comparisons", "To go faster", "To use more colors", "To make it harder"], 0,
         "Equal units keep measurements fair."),
        ("Which action shows careful measuring?", ["Placing cubes straight", "Leaving spaces", "Using different sizes", "Stacking randomly"], 0,
         "Units should be straight with no gaps."),
        ("If a line measures 8 buttons, how many buttons is half the line?", ["4", "2", "6", "8"], 0,
         "Half of 8 buttons is 4 buttons."),
    ]
    for idx, (question, choices, correct_index, explanation) in enumerate(questions, 1):
        rows.append(
            build_multiple_choice(
                question,
                choices,
                correct_index,
                explanation,
                test_name,
                f"Non-standard Units Q{idx}",
                path,
            )
        )
    question = "Select all good non-standard units."
    choices = ["Paper clips", "Different-sized sticks", "Connecting cubes", "Leaves of all sizes"]
    correct_indices = [0, 2]
    explanation = "Units should be the same size like paper clips or cubes."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Non-standard Units Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all steps for measuring with paper clips."
    choices = ["Place clips end to end", "Leave gaps", "Start at zero", "Mix clip sizes"]
    correct_indices = [0, 2]
    explanation = "End-to-end clips and starting at zero give accurate measurements."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Non-standard Units Q{len(rows) + 1}",
            path,
        )
    )
    question = "If a plant measures 9 cubes and grows 2 more cubes, how many cubes tall is it now?"
    choices = ["11", "10", "12", "9"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Adding 2 cubes to 9 cubes equals 11 cubes.",
            test_name,
            f"Non-standard Units Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which sentence is true about non-standard units?"
    choices = ["They must be the same size", "They should change size", "They work best when mixed", "They are only for weight"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Same-sized units make fair measurements.",
            test_name,
            f"Non-standard Units Q{len(rows) + 1}",
            path,
        )
    )
    question = "If a desk measures 15 paper clips and a chair measures 10 paper clips, which is longer?"
    choices = ["Desk", "Chair", "They are equal", "Cannot tell"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "15 paper clips is more than 10, so the desk is longer.",
            test_name,
            f"Non-standard Units Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def time_to_hour_questions():
    test_name = "Chapter 8: Time"
    path = "Chapter 8/Reading Clocks to Hour"
    rows = []
    descriptions = [
        ("The hour hand points to 3 and the minute hand points to 12.", "3:00"),
        ("The hour hand is on 7 and the minute hand is on 12.", "7:00"),
        ("The hour hand is on 11 and the minute hand is on 12.", "11:00"),
        ("The hour hand is on 5 and the minute hand is on 12.", "5:00"),
        ("The hour hand points to 9 with the minute hand on 12.", "9:00"),
        ("The hour hand is on 2 with the minute hand on 12.", "2:00"),
        ("The hour hand points to 8 with the minute hand at 12.", "8:00"),
        ("The hour hand is on 10 with the minute hand on 12.", "10:00"),
        ("The hour hand points to 4 and the minute hand points to 12.", "4:00"),
        ("The hour hand is on 6 with the minute hand on 12.", "6:00"),
    ]
    for idx, (description, correct_time) in enumerate(descriptions, 1):
        question = f"What time is shown? {description}"
        choices = [correct_time, "3:30", "12:00", "6:30"]
        explanation = f"When the minute hand is on 12, the time is on the hour, so it is {correct_time}."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                0,
                explanation,
                test_name,
                f"Time to Hour Q{idx}",
                path,
            )
        )
    question = "Select all clocks that show 1:00."
    choices = ["Hour hand on 1, minute hand on 12", "Hour hand on 12, minute hand on 1", "Hour hand on 1, minute hand on 6", "Hour hand on 5, minute hand on 12"]
    correct_indices = [0]
    explanation = "At 1:00 the hour hand points to 1 and the minute hand to 12."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Time to Hour Q{len(rows) + 1}",
            path,
        )
    )
    question = "If the hour hand is on 12 and minute hand on 12, what time is it?"
    choices = ["12:00", "6:00", "3:00", "9:00"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Both hands at 12 show 12:00.",
            test_name,
            f"Time to Hour Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all times that show the hour exactly."
    choices = ["4:00", "4:30", "7:00", "7:15"]
    correct_indices = [0, 2]
    explanation = "Times ending in :00 are on the hour."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Time to Hour Q{len(rows) + 1}",
            path,
        )
    )
    question = "When the clock shows 1:00, where is the minute hand?"
    choices = ["On 12", "On 1", "On 6", "On 3"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "On the hour, the minute hand is on 12.",
            test_name,
            f"Time to Hour Q{len(rows) + 1}",
            path,
        )
    )
    question = "If it is 4:00 now, what time will it be one hour later?"
    choices = ["5:00", "4:30", "6:00", "3:00"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Adding one hour to 4:00 gives 5:00.",
            test_name,
            f"Time to Hour Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def time_to_half_hour_questions():
    test_name = "Chapter 8: Time"
    path = "Chapter 8/Reading Clocks to Half-Hour"
    rows = []
    descriptions = [
        ("Hour hand between 3 and 4, minute hand on 6.", "3:30"),
        ("Hour hand between 6 and 7, minute hand on 6.", "6:30"),
        ("Hour hand between 1 and 2, minute hand on 6.", "1:30"),
        ("Hour hand between 9 and 10, minute hand on 6.", "9:30"),
        ("Hour hand between 4 and 5, minute hand on 6.", "4:30"),
        ("Hour hand between 7 and 8, minute hand on 6.", "7:30"),
        ("Hour hand between 10 and 11, minute hand on 6.", "10:30"),
        ("Hour hand between 2 and 3, minute hand on 6.", "2:30"),
        ("Hour hand between 11 and 12, minute hand on 6.", "11:30"),
        ("Hour hand between 5 and 6, minute hand on 6.", "5:30"),
    ]
    for idx, (description, correct_time) in enumerate(descriptions, 1):
        question = f"What time is shown? {description}"
        choices = [correct_time, f"{correct_time.split(':')[0]}:00", "12:30", "8:30"]
        explanation = f"When the minute hand is on 6, the time is half past the hour, so it is {correct_time}."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                0,
                explanation,
                test_name,
                f"Time to Half-Hour Q{idx}",
                path,
            )
        )
    question = "Select all times that are half past the hour."
    choices = ["2:30", "2:00", "5:30", "5:00"]
    correct_indices = [0, 2]
    explanation = "Half past uses :30 minutes."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Time to Half-Hour Q{len(rows) + 1}",
            path,
        )
    )
    question = "Where is the minute hand at 8:30?"
    choices = ["On 6", "On 8", "On 12", "On 3"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "At :30 the minute hand is on 6.",
            test_name,
            f"Time to Half-Hour Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all clocks that show 12:30."
    choices = ["Hour hand between 12 and 1, minute hand on 6", "Hour hand on 12, minute hand on 12", "Hour hand between 1 and 2, minute hand on 6", "Hour hand between 12 and 1, minute hand on 3"]
    correct_indices = [0]
    explanation = "At 12:30, the hour hand is between 12 and 1 and the minute hand is on 6."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Time to Half-Hour Q{len(rows) + 1}",
            path,
        )
    )
    question = "If the clock shows 3:30, which hour is it halfway past?"
    choices = ["3", "4", "1", "6"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "3:30 is halfway past 3 o'clock.",
            test_name,
            f"Time to Half-Hour Q{len(rows) + 1}",
            path,
        )
    )
    question = "How many minutes are in half an hour?"
    choices = ["30", "15", "45", "60"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Half an hour equals 30 minutes.",
            test_name,
            f"Time to Half-Hour Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def day_period_questions():
    test_name = "Chapter 8: Time"
    path = "Chapter 8/Morning Afternoon Evening"
    rows = []
    questions = [
        ("When do you usually eat breakfast?", ["Morning", "Afternoon", "Evening", "Midnight"], 0,
         "Breakfast is eaten in the morning."),
        ("When do you go to bed?", ["Evening", "Morning", "Afternoon", "Noon"], 0,
         "Bedtime is usually in the evening."),
        ("When does school usually start?", ["Morning", "Evening", "Midnight", "Late night"], 0,
         "School starts in the morning."),
        ("When do you eat lunch?", ["Afternoon", "Morning", "Evening", "Late night"], 0,
         "Lunch is in the afternoon."),
        ("When do you see stars in the sky?", ["Evening", "Morning", "Afternoon", "Midday"], 0,
         "Stars are visible in the evening."),
        ("When do you usually play outside after school?", ["Afternoon", "Morning", "Midnight", "Late evening"], 0,
         "After school play happens in the afternoon."),
        ("When do you brush your teeth before bed?", ["Evening", "Morning", "Afternoon", "Noon"], 0,
         "You brush before bed in the evening."),
        ("When do you watch the sunrise?", ["Morning", "Afternoon", "Evening", "Night"], 0,
         "Sunrise happens in the morning."),
        ("When do you eat dinner?", ["Evening", "Morning", "Afternoon", "Midnight"], 0,
         "Dinner is in the evening."),
        ("When do you pack your backpack for school?", ["Morning", "Evening", "Afternoon", "Midnight"], 0,
         "You get ready in the morning."),
    ]
    for idx, (question, choices, correct_index, explanation) in enumerate(questions, 1):
        rows.append(
            build_multiple_choice(
                question,
                choices,
                correct_index,
                explanation,
                test_name,
                f"Time of Day Q{idx}",
                path,
            )
        )
    question = "Select all activities that happen in the morning."
    choices = ["Eat breakfast", "Do homework at night", "Brush teeth before bed", "Go to school"]
    correct_indices = [0, 3]
    explanation = "Breakfast and going to school are morning activities."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Time of Day Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all activities that happen in the evening."
    choices = ["Eat dinner", "Eat lunch", "Go to bed", "Brush teeth in the morning"]
    correct_indices = [0, 2]
    explanation = "Dinner and going to bed happen in the evening."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Time of Day Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which part of the day comes after morning?"
    choices = ["Afternoon", "Evening", "Night", "Midnight"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Afternoon comes after morning.",
            test_name,
            f"Time of Day Q{len(rows) + 1}",
            path,
        )
    )
    question = "When would you see the moon?"
    choices = ["Evening", "Morning", "Afternoon", "Noon"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "The moon is often seen in the evening or night.",
            test_name,
            f"Time of Day Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which part of the day comes before evening?"
    choices = ["Afternoon", "Morning", "Night", "Midnight"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Afternoon happens right before evening.",
            test_name,
            f"Time of Day Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def coin_recognition_questions():
    test_name = "Chapter 9: Money"
    path = "Chapter 9/Recognizing Coins"
    rows = []
    questions = [
        ("Which coin is worth 1 cent?", ["Penny", "Nickel", "Dime", "Quarter"], 0,
         "A penny is worth 1 cent."),
        ("Which coin is worth 5 cents?", ["Nickel", "Penny", "Dime", "Quarter"], 0,
         "A nickel is worth 5 cents."),
        ("Which coin is worth 10 cents?", ["Dime", "Nickel", "Penny", "Quarter"], 0,
         "A dime is worth 10 cents."),
        ("Which coin is worth 25 cents?", ["Quarter", "Nickel", "Penny", "Dime"], 0,
         "A quarter is worth 25 cents."),
        ("Which coin is the smallest in size?", ["Dime", "Penny", "Nickel", "Quarter"], 0,
         "The dime is the smallest coin."),
        ("Which coin is the largest in size?", ["Quarter", "Penny", "Nickel", "Dime"], 0,
         "A quarter is the largest coin."),
        ("Which coin is brown or copper-colored?", ["Penny", "Nickel", "Dime", "Quarter"], 0,
         "Pennies are copper colored."),
        ("Which coin has George Washington on the front?", ["Quarter", "Penny", "Nickel", "Dime"], 0,
         "George Washington is on the quarter."),
        ("Which coin has Thomas Jefferson on it?", ["Nickel", "Penny", "Dime", "Quarter"], 0,
         "Thomas Jefferson is on the nickel."),
        ("Which coin has Franklin D. Roosevelt on it?", ["Dime", "Penny", "Quarter", "Nickel"], 0,
         "Franklin D. Roosevelt is on the dime."),
    ]
    for idx, (question, choices, correct_index, explanation) in enumerate(questions, 1):
        rows.append(
            build_multiple_choice(
                question,
                choices,
                correct_index,
                explanation,
                test_name,
                f"Coin Recognition Q{idx}",
                path,
            )
        )
    question = "Select all coins worth less than 10 cents."
    choices = ["Penny", "Nickel", "Dime", "Quarter"]
    correct_indices = [0, 1]
    explanation = "Pennies and nickels are worth less than 10 cents."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Coin Recognition Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all coins that are silver-colored."
    choices = ["Penny", "Nickel", "Dime", "Quarter"]
    correct_indices = [1, 2, 3]
    explanation = "Nickels, dimes, and quarters are silver-colored."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Coin Recognition Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which coin is worth the most money?"
    choices = ["Quarter", "Dime", "Nickel", "Penny"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "A quarter is worth 25 cents, the highest value listed.",
            test_name,
            f"Coin Recognition Q{len(rows) + 1}",
            path,
        )
    )
    question = "How many pennies equal one nickel?"
    choices = ["5", "10", "25", "2"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Five pennies equal one nickel.",
            test_name,
            f"Coin Recognition Q{len(rows) + 1}",
            path,
        )
    )
    question = "How many nickels equal one quarter?"
    choices = ["5", "4", "3", "2"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Five nickels equal 25 cents, the same as a quarter.",
            test_name,
            f"Coin Recognition Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def counting_coins_questions():
    test_name = "Chapter 9: Money"
    path = "Chapter 9/Counting Coins"
    rows = []
    scenarios = [
        ("You have 2 dimes. How much money is that?", "20¢"),
        ("You have 3 nickels. How much money is that?", "15¢"),
        ("You have 4 pennies and 1 nickel. How much money is that?", "9¢"),
        ("You have 1 quarter and 1 nickel. How much money is that?", "30¢"),
        ("You have 2 quarters. How much money is that?", "50¢"),
        ("You have 1 dime and 3 pennies. How much money is that?", "13¢"),
        ("You have 1 nickel and 2 pennies. How much money is that?", "7¢"),
        ("You have 3 dimes. How much money is that?", "30¢"),
        ("You have 1 quarter and 2 dimes. How much money is that?", "45¢"),
        ("You have 4 nickels. How much money is that?", "20¢"),
    ]
    for idx, (question, correct_value) in enumerate(scenarios, 1):
        choices = [correct_value, "25¢", "40¢", "10¢"]
        explanation = f"Counting the coins totals {correct_value}."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                0,
                explanation,
                test_name,
                f"Counting Coins Q{idx}",
                path,
            )
        )
    question = "Select all sets worth 10¢."
    choices = ["1 dime", "2 nickels", "10 pennies", "1 quarter"]
    correct_indices = [0, 1, 2]
    explanation = "A dime, two nickels, or ten pennies equal 10¢."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Counting Coins Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all sets worth 25¢."
    choices = ["1 quarter", "2 dimes and 1 nickel", "5 nickels", "2 nickels and 5 pennies"]
    correct_indices = [0, 1, 2]
    explanation = "Each of these combinations totals 25¢."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Counting Coins Q{len(rows) + 1}",
            path,
        )
    )
    question = "You have 1 quarter, 1 dime, and 4 pennies. How much money is that?"
    choices = ["39¢", "34¢", "41¢", "29¢"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "25¢ + 10¢ + 4¢ = 39¢.",
            test_name,
            f"Counting Coins Q{len(rows) + 1}",
            path,
        )
    )
    question = "How many dimes make $1.00?"
    choices = ["10", "5", "4", "2"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Ten dimes equal $1.00.",
            test_name,
            f"Counting Coins Q{len(rows) + 1}",
            path,
        )
    )
    question = "You have 2 dimes and 5 pennies. How much money is that?"
    choices = ["25¢", "20¢", "15¢", "30¢"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "20¢ + 5¢ equals 25¢.",
            test_name,
            f"Counting Coins Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def money_word_problem_questions():
    test_name = "Chapter 9: Money"
    path = "Chapter 9/Money Word Problems"
    rows = []
    problems = [
        ("A toy costs 15¢. You have a dime and a nickel. Do you have enough money?", "Yes"),
        ("A sticker costs 12¢. You have a dime and 3 pennies. Do you have enough money?", "Yes"),
        ("A ball costs 20¢. You have 3 nickels. Do you have enough money?", "No"),
        ("A pencil costs 8¢. You have 8 pennies. Do you have enough money?", "Yes"),
        ("A snack costs 25¢. You have 2 dimes and 1 nickel. Do you have enough money?", "Yes"),
        ("A book costs 40¢. You have 1 quarter and 1 dime. Do you have enough money?", "No"),
        ("A toy car costs 30¢. You have 1 quarter and 2 nickels. Do you have enough money?", "Yes"),
        ("A bracelet costs 18¢. You have 1 dime, 1 nickel, and 3 pennies. Do you have enough money?", "Yes"),
        ("A keychain costs 22¢. You have 2 dimes and 2 pennies. Do you have enough money?", "Yes"),
        ("A comic costs 35¢. You have 1 quarter and 1 dime. Do you have enough money?", "Yes"),
    ]
    for idx, (question, answer) in enumerate(problems, 1):
        choices = ["Yes", "No", "Maybe", "Not sure"]
        explanation = "Count the coins to decide if it is enough money."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                0 if answer == "Yes" else 1,
                explanation,
                test_name,
                f"Money Word Problem Q{idx}",
                path,
            )
        )
    question = "Select all purchases you can make with 50¢."
    choices = ["A 45¢ yo-yo", "A 55¢ book", "A 30¢ ball", "A 70¢ puzzle"]
    correct_indices = [0, 2]
    explanation = "Only the yo-yo and ball cost 50¢ or less."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Money Word Problem Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all ways to make 30¢."
    choices = ["3 dimes", "1 quarter and 1 nickel", "6 nickels", "1 dime and 2 nickels"]
    correct_indices = [0, 1, 2]
    explanation = "These combinations total 30¢."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Money Word Problem Q{len(rows) + 1}",
            path,
        )
    )
    question = "If you spend 18¢ from 25¢, how much money is left?"
    choices = ["7¢", "8¢", "10¢", "5¢"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "25¢ - 18¢ = 7¢ remain.",
            test_name,
            f"Money Word Problem Q{len(rows) + 1}",
            path,
        )
    )
    question = "If a toy costs 32¢ and you have 1 quarter, 1 nickel, and 2 pennies, do you have enough?"
    choices = ["Yes", "No", "Maybe", "Not sure"]
    explanation = "25¢ + 5¢ + 2¢ = 32¢, which is the exact amount."
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            explanation,
            test_name,
            f"Money Word Problem Q{len(rows) + 1}",
            path,
        )
    )
    question = "You have 1 quarter and 3 nickels. What is the total value?"
    choices = ["40¢", "45¢", "50¢", "35¢"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "25¢ + 15¢ = 40¢.",
            test_name,
            f"Money Word Problem Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def collecting_data_questions():
    test_name = "Chapter 10: Data and Graphing"
    path = "Chapter 10/Collecting Data"
    rows = []
    questions = [
        ("What question could you ask to find favorite fruits?", ["What is your favorite fruit?", "How tall are you?", "What time is it?", "How many shoes do you have?"], 0,
         "To find favorite fruits, ask about fruit preferences."),
        ("When you count how many students like each color, what are you collecting?", ["Data", "Stories", "Songs", "Books"], 0,
         "You are collecting data."),
        ("Which tool helps record data during a survey?", ["Tally chart", "Clock", "Scale", "Thermometer"], 0,
         "Tally charts help organize data."),
        ("If five students like blue and three like red, which color is more popular?", ["Blue", "Red", "Both", "Neither"], 0,
         "More students chose blue."),
        ("What do you call information you collect from questions?", ["Data", "Weather", "Music", "Stories"], 0,
         "Information from questions is data."),
        ("Which survey question would give yes or no answers?", ["Do you like apples?", "What is your favorite number?", "Which day is your birthday?", "What is your address?"], 0,
         "Do you like apples? has yes or no answers."),
        ("If you survey 10 classmates, how many pieces of data do you collect?", ["10", "5", "15", "20"], 0,
         "Each classmate gives one piece of data."),
        ("Which question helps collect data about pets?", ["How many pets do you have?", "What color is the sky?", "What is 2 + 2?", "How old are you?"], 0,
         "Ask how many pets to collect pet data."),
        ("Which method helps you remember results while surveying?", ["Making tally marks", "Jumping", "Clapping", "Reading"], 0,
         "Tally marks keep track of answers."),
        ("If four students choose dogs and two choose cats, which is less popular?", ["Cats", "Dogs", "Both", "Neither"], 0,
         "Fewer students chose cats."),
    ]
    for idx, (question, choices, correct_index, explanation) in enumerate(questions, 1):
        rows.append(
            build_multiple_choice(
                question,
                choices,
                correct_index,
                explanation,
                test_name,
                f"Collecting Data Q{idx}",
                path,
            )
        )
    question = "Select all good survey questions."
    choices = ["What is your favorite game?", "How tall is the tree?", "Do you like pizza?", "What time is bedtime?"]
    correct_indices = [0, 2]
    explanation = "Good survey questions ask about opinions or likes."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Collecting Data Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all ways to collect data in class."
    choices = ["Ask a question", "Flip a coin", "Use a tally chart", "Shout answers"]
    correct_indices = [0, 2]
    explanation = "Asking questions and using tally charts collect data." 
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Collecting Data Q{len(rows) + 1}",
            path,
        )
    )
    question = "If six students like red and four like blue, how many were asked in all?"
    choices = ["10", "6", "4", "8"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "6 + 4 = 10 students.",
            test_name,
            f"Collecting Data Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which sentence describes data collection?"
    choices = ["We asked 12 friends their favorite sport", "We guessed the weather", "We listened to music", "We drew a picture"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Asking friends their favorite sport gathers data.",
            test_name,
            f"Collecting Data Q{len(rows) + 1}",
            path,
        )
    )
    question = "If three students like cats, four like dogs, and two like fish, how many students were asked?"
    choices = ["9", "7", "5", "6"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "3 + 4 + 2 = 9 students.",
            test_name,
            f"Collecting Data Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def making_graphs_questions():
    test_name = "Chapter 10: Data and Graphing"
    path = "Chapter 10/Making Graphs"
    rows = []
    questions = [
        ("What do you need before making a graph?", ["Data", "Glue", "Paint", "Music"], 0,
         "Graphs show data."),
        ("Which graph uses pictures to show amounts?", ["Picture graph", "Line graph", "Circle graph", "Number line"], 0,
         "Picture graphs use pictures."),
        ("Which graph uses bars to show data?", ["Bar graph", "Picture graph", "Circle graph", "Calendar"], 0,
         "Bar graphs use bars."),
        ("If 5 students like apples and 3 like bananas, how many pictures should the apple column have if each picture means 1 student?", ["5", "3", "4", "6"], 0,
         "Use one picture per student."),
        ("When making a bar graph, what must each bar be labeled with?", ["Category name", "Favorite color", "Random numbers", "Weather"], 0,
         "Each bar is labeled by category."),
        ("If each picture stands for 2 votes and you need to show 6 votes, how many pictures do you draw?", ["3", "6", "2", "12"], 0,
         "6 votes ÷ 2 per picture = 3 pictures."),
        ("Which title fits a graph about favorite sports?", ["Favorite Sports", "Weather Today", "Homework Chart", "Class Schedule"], 0,
         "A graph needs a matching title."),
        ("When creating a graph, why do you count carefully?", ["To show correct data", "To decorate", "To make music", "To draw animals"], 0,
         "Counting carefully keeps the graph correct."),
        ("What do you put along the bottom of a bar graph?", ["Categories", "Heights", "Weights", "Songs"], 0,
         "Categories go along the bottom axis."),
        ("What goes along the side of a bar graph?", ["Numbers", "Letters", "Stories", "Shapes"], 0,
         "Numbers show how many for each bar."),
    ]
    for idx, (question, choices, correct_index, explanation) in enumerate(questions, 1):
        rows.append(
            build_multiple_choice(
                question,
                choices,
                correct_index,
                explanation,
                test_name,
                f"Making Graphs Q{idx}",
                path,
            )
        )
    question = "Select all graphs that can show class favorites."
    choices = ["Bar graph", "Picture graph", "Circle graph", "Thermometer"]
    correct_indices = [0, 1, 2]
    explanation = "Bar, picture, and circle graphs show data." 
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Making Graphs Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all parts needed for a graph."
    choices = ["Title", "Data", "Labels", "Snacks"]
    correct_indices = [0, 1, 2]
    explanation = "Graphs need a title, data, and labels." 
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Making Graphs Q{len(rows) + 1}",
            path,
        )
    )
    question = "If each bar on a graph is colored differently, what does that help with?"
    choices = ["Reading the categories", "Making noise", "Counting backwards", "Telling stories"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Different colors make categories easy to see.",
            test_name,
            f"Making Graphs Q{len(rows) + 1}",
            path,
        )
    )
    question = "How many bars are needed if you have 4 categories?"
    choices = ["4", "2", "6", "8"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Each category needs one bar, so 4 categories need 4 bars.",
            test_name,
            f"Making Graphs Q{len(rows) + 1}",
            path,
        )
    )
    question = "If each bar stands for 2 students and a bar reaches up to 5 marks, how many students is that?"
    choices = ["10", "5", "7", "8"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "5 marks × 2 students each = 10 students.",
            test_name,
            f"Making Graphs Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def reading_graphs_questions():
    test_name = "Chapter 10: Data and Graphing"
    path = "Chapter 10/Reading Graphs"
    rows = []
    scenarios = [
        ("In a graph, 5 students like blue and 3 like red. Which color has more votes?", "Blue"),
        ("If a bar graph shows 7 cats and 2 dogs, which animal is less popular?", "Dogs"),
        ("If a picture graph shows 4 stars for books and 6 stars for movies, which has more?", "Movies"),
        ("If the tallest bar is for apples, which fruit do most students like?", "Apples"),
        ("If two bars are the same height, what does that mean?", "They are equal"),
        ("If a graph shows 8 votes for recess and 4 for reading, how many more votes for recess?", "4"),
        ("If a graph shows 6 votes for soccer and 1 for tennis, which has fewer votes?", "Tennis"),
        ("If there are 3 pictures for cats and 3 for dogs, what can you say?", "They are equal"),
        ("If a bar graph shows 9 tallies for pizza and 5 for tacos, which is less?", "Tacos"),
        ("If a graph shows 2 more votes for science than math, which subject has more votes?", "Science"),
    ]
    for idx, (prompt, answer) in enumerate(scenarios, 1):
        question = prompt
        choices = [answer, "Not enough information", "The other option", "Both"]
        explanation = f"Reading the graph shows the correct answer is {answer}."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                0,
                explanation,
                test_name,
                f"Reading Graphs Q{idx}",
                path,
            )
        )
    question = "Select all statements that describe the tallest bar."
    choices = ["It shows the most votes", "It shows the fewest votes", "It is the longest bar", "It means everyone chose it"]
    correct_indices = [0, 2]
    explanation = "The tallest bar shows the most votes and is the longest bar."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Reading Graphs Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all facts you can read from a graph."
    choices = ["How many votes each choice has", "Who is the tallest student", "Which category has the least", "What time it is"]
    correct_indices = [0, 2]
    explanation = "Graphs show how many for each category and which has the least."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Reading Graphs Q{len(rows) + 1}",
            path,
        )
    )
    question = "If a graph shows 3 more votes for cats than dogs, and dogs have 5 votes, how many votes do cats have?"
    choices = ["8", "5", "3", "10"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "5 + 3 = 8 votes for cats.",
            test_name,
            f"Reading Graphs Q{len(rows) + 1}",
            path,
        )
    )
    question = "If a bar graph shows 4 students like green and 4 like orange, how many students like those colors in total?"
    choices = ["8", "4", "6", "10"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "4 + 4 = 8 students.",
            test_name,
            f"Reading Graphs Q{len(rows) + 1}",
            path,
        )
    )
    question = "If a graph shows 5 votes for apples, 3 for bananas, and 2 for grapes, how many votes are shown?"
    choices = ["10", "8", "9", "7"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "5 + 3 + 2 = 10 votes.",
            test_name,
            f"Reading Graphs Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def fractions_halves_questions():
    test_name = "Chapter 11: Fractions (Intro)"
    path = "Chapter 11/Halves"
    rows = []
    questions = [
        ("What do you call two equal parts of a whole?", ["Halves", "Thirds", "Quarters", "Eighths"], 0,
         "Two equal parts are halves."),
        ("If you cut an apple into 2 equal pieces, what is each piece?", ["Half", "Quarter", "Whole", "Third"], 0,
         "Each piece is a half."),
        ("How many halves make a whole?", ["2", "3", "4", "5"], 0,
         "Two halves make a whole."),
        ("If you shade 1 of 2 equal parts, what fraction is shaded?", ["1/2", "1/4", "2/2", "3/4"], 0,
         "One of two equal parts is 1/2."),
        ("If 1/2 of a pizza is eaten, how much is left?", ["1/2", "1/4", "2/2", "0"], 0,
         "Half remains."),
        ("Which symbol shows one half?", ["1/2", "1/4", "2/4", "3/4"], 0,
         "1/2 represents one half."),
        ("If you share a sandwich equally with a friend, how much does each get?", ["Half", "Quarter", "Whole", "None"], 0,
         "Each friend gets half."),
        ("If a rectangle is divided into two equal parts, what is each part called?", ["Half", "Third", "Quarter", "Eighth"], 0,
         "Two equal parts are halves."),
        ("If you shade both halves of a shape, what fraction is shaded?", ["2/2", "1/2", "1/4", "3/4"], 0,
         "Both halves shaded make 2/2 or the whole."),
        ("If you eat one of two equal apple slices, what fraction did you eat?", ["1/2", "1/3", "1/4", "2/2"], 0,
         "You ate half the apple."),
    ]
    for idx, (question, choices, correct_index, explanation) in enumerate(questions, 1):
        rows.append(
            build_multiple_choice(
                question,
                choices,
                correct_index,
                explanation,
                test_name,
                f"Halves Q{idx}",
                path,
            )
        )
    question = "Select all shapes that are split into halves."
    choices = ["Two equal parts", "Three equal parts", "Two different parts", "One large, one small"]
    correct_indices = [0]
    explanation = "Only two equal parts show halves."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Halves Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all fractions equal to one half."
    choices = ["1/2", "2/4", "3/6", "4/4"]
    correct_indices = [0, 1, 2]
    explanation = "1/2, 2/4, and 3/6 each equal one half."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Halves Q{len(rows) + 1}",
            path,
        )
    )
    question = "If a shape is divided into two equal parts and you shade one, what fraction is shaded?"
    choices = ["1/2", "1/4", "2/2", "3/4"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "One of two equal parts is 1/2.",
            test_name,
            f"Halves Q{len(rows) + 1}",
            path,
        )
    )
    question = "If you fold a paper in half, how many equal parts does it have?"
    choices = ["2", "3", "4", "5"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Folding in half makes two equal parts.",
            test_name,
            f"Halves Q{len(rows) + 1}",
            path,
        )
    )
    question = "If you have 12 grapes and eat half, how many grapes did you eat?"
    choices = ["6", "4", "8", "10"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Half of 12 is 6.",
            test_name,
            f"Halves Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def fractions_quarters_questions():
    test_name = "Chapter 11: Fractions (Intro)"
    path = "Chapter 11/Quarters"
    rows = []
    questions = [
        ("What do you call four equal parts of a whole?", ["Quarters", "Halves", "Thirds", "Eighths"], 0,
         "Four equal parts are quarters."),
        ("If a pizza is cut into 4 equal slices, what is one slice called?", ["Quarter", "Half", "Whole", "Third"], 0,
         "Each slice is a quarter."),
        ("How many quarters make a whole?", ["4", "2", "3", "5"], 0,
         "Four quarters equal one whole."),
        ("Which fraction shows one quarter?", ["1/4", "1/2", "2/4", "3/4"], 0,
         "1/4 represents a quarter."),
        ("If you shade 1 of 4 equal parts, what fraction is shaded?", ["1/4", "1/2", "3/4", "4/4"], 0,
         "One out of four equal parts is 1/4."),
        ("If you eat 3 slices of a pizza cut into 4 equal slices, what fraction did you eat?", ["3/4", "1/4", "1/2", "4/4"], 0,
         "Three slices out of four is 3/4."),
        ("If a square is divided into 4 equal parts and you shade all, what fraction is shaded?", ["4/4", "1/4", "1/2", "3/4"], 0,
         "All four quarters make 4/4 or the whole."),
        ("If you shade two quarters, what fraction is shaded?", ["2/4", "1/4", "3/4", "1/2"], 0,
         "Two quarters equal 2/4 or 1/2."),
        ("If you have 4 equal pieces of a cookie and eat one, how much is left?", ["3/4", "1/4", "1/2", "4/4"], 0,
         "Three quarters remain."),
        ("If a circle is cut into 4 equal pieces, how many pieces make up one half?", ["2", "3", "4", "1"], 0,
         "Two quarters make one half."),
    ]
    for idx, (question, choices, correct_index, explanation) in enumerate(questions, 1):
        rows.append(
            build_multiple_choice(
                question,
                choices,
                correct_index,
                explanation,
                test_name,
                f"Quarters Q{idx}",
                path,
            )
        )
    question = "Select all shapes divided into quarters."
    choices = ["Four equal pieces", "Two equal pieces", "Four different pieces", "Three equal pieces"]
    correct_indices = [0]
    explanation = "Quarters require four equal pieces."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Quarters Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all fractions equal to 3/4."
    choices = ["3/4", "6/8", "9/12", "1/4"]
    correct_indices = [0, 1, 2]
    explanation = "3/4, 6/8, and 9/12 represent three quarters."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Quarters Q{len(rows) + 1}",
            path,
        )
    )
    question = "If you shade three out of four equal parts, what fraction is shaded?"
    choices = ["3/4", "1/4", "1/2", "4/4"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Three quarters shaded is 3/4.",
            test_name,
            f"Quarters Q{len(rows) + 1}",
            path,
        )
    )
    question = "If you divide a rectangle into four equal strips and color one, what fraction is colored?"
    choices = ["1/4", "1/2", "3/4", "4/4"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "One of four strips is 1/4.",
            test_name,
            f"Quarters Q{len(rows) + 1}",
            path,
        )
    )
    question = "If you share 8 crackers equally with 4 friends, what fraction does each friend get?"
    choices = ["1/4", "1/2", "3/4", "1/8"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Each friend receives one quarter of the crackers.",
            test_name,
            f"Quarters Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def problem_solving_add_sub_questions():
    test_name = "Chapter 12: Problem Solving & Review"
    path = "Chapter 12/Addition and Subtraction Problems"
    rows = []
    scenarios = [
        ("Mia has 9 stickers and gets 7 more. How many stickers does she have now?", 16),
        ("Luis has 14 marbles and gives 5 away. How many marbles remain?", 9),
        ("The class baked 8 muffins and 6 more. How many muffins in all?", 14),
        ("There are 12 birds on a fence. 4 fly away. How many stay?", 8),
        ("A basket holds 7 apples and 9 oranges. How many fruits?", 16),
        ("Sara read 5 pages in the morning and 8 at night. How many pages did she read?", 13),
        ("A box has 15 crayons. 6 are used. How many are left?", 9),
        ("There are 10 balloons. 7 pop. How many remain?", 3),
        ("Lila collects 11 shells and finds 3 more. How many shells now?", 14),
        ("Ben has 18 toy cars and gives 9 to his friend. How many cars remain?", 9),
    ]
    for idx, (question, result) in enumerate(scenarios, 1):
        choices = [str(result), str(result + 1), str(result - 1), str(result + 2)]
        explanation = f"Solving the word problem gives {result}."
        rows.append(
            build_multiple_choice(
                question,
                choices,
                0,
                explanation,
                test_name,
                f"Problem Solving Q{idx}",
                path,
            )
        )
    question = "Select all problems that need addition."
    choices = [
        "A child has 4 blocks and gets 3 more",
        "A child has 7 stickers and gives away 2",
        "A class has 6 girls and 5 boys",
        "A jar has 10 cookies and 4 are eaten",
    ]
    correct_indices = [0, 2]
    explanation = "Addition is used when combining amounts."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Problem Solving Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all problems that need subtraction."
    choices = [
        "A basket has 12 apples and 5 are eaten",
        "A shelf has 4 books and gets 3 more",
        "A pool has 9 swimmers and 4 get out",
        "A class gets 2 new students",
    ]
    correct_indices = [0, 2]
    explanation = "Subtraction is used when taking away."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Problem Solving Q{len(rows) + 1}",
            path,
        )
    )
    question = "If you have 13 pencils and give away 6, how many do you have left?"
    choices = ["7", "6", "8", "9"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "13 - 6 = 7 pencils remain.",
            test_name,
            f"Problem Solving Q{len(rows) + 1}",
            path,
        )
    )
    question = "If you find 4 shells and later find 6 more, how many shells do you have?"
    choices = ["10", "9", "8", "7"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "4 + 6 = 10 shells.",
            test_name,
            f"Problem Solving Q{len(rows) + 1}",
            path,
        )
    )
    question = "A jar has 20 candies. 9 are eaten. How many candies are left?"
    choices = ["11", "10", "9", "8"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "20 - 9 = 11 candies remain.",
            test_name,
            f"Problem Solving Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def mixed_review_questions():
    test_name = "Chapter 12: Problem Solving & Review"
    path = "Chapter 12/Mixed Review"
    rows = []
    questions = [
        ("Which shape has 4 equal sides?", ["Square", "Triangle", "Circle", "Rectangle"], 0,
         "A square has four equal sides."),
        ("What time is shown when the hour hand is on 8 and the minute hand on 12?", ["8:00", "8:30", "12:30", "6:00"], 0,
         "Hands at 8 and 12 show 8:00."),
        ("How many cents are in 3 nickels?", ["15¢", "10¢", "25¢", "5¢"], 0,
         "Three nickels equal 15¢."),
        ("Which is longer: a pencil or a jump rope?", ["Jump rope", "Pencil", "They are equal", "Not sure"], 0,
         "A jump rope is longer."),
        ("What fraction of a pizza is one out of two equal slices?", ["1/2", "1/4", "2/2", "3/4"], 0,
         "One of two equal slices is 1/2."),
        ("If you have 6 apples and eat 2, how many remain?", ["4", "3", "5", "2"], 0,
         "6 - 2 = 4 apples remain."),
        ("Which coin is worth 10 cents?", ["Dime", "Penny", "Nickel", "Quarter"], 0,
         "A dime is worth 10 cents."),
        ("If the clock shows 3:30, where is the minute hand?", ["On 6", "On 3", "On 12", "On 9"], 0,
         "At :30 the minute hand is on 6."),
        ("Which object is heavier: a rock or a feather?", ["Rock", "Feather", "They weigh the same", "Cannot tell"], 0,
         "A rock is heavier."),
        ("How many quarters make $1.00?", ["4", "3", "5", "2"], 0,
         "Four quarters equal one dollar."),
    ]
    for idx, (question, choices, correct_index, explanation) in enumerate(questions, 1):
        rows.append(
            build_multiple_choice(
                question,
                choices,
                correct_index,
                explanation,
                test_name,
                f"Mixed Review Q{idx}",
                path,
            )
        )
    question = "Select all activities that happen in the morning."
    choices = ["Eat breakfast", "Brush teeth before bed", "Go to school", "See stars"]
    correct_indices = [0, 2]
    explanation = "Breakfast and going to school are morning activities."
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Mixed Review Q{len(rows) + 1}",
            path,
        )
    )
    question = "Select all shapes with corners."
    choices = ["Rectangle", "Circle", "Triangle", "Oval"]
    correct_indices = [0, 2]
    explanation = "Rectangles and triangles have corners." 
    rows.append(
        build_select_all(
            question,
            choices,
            correct_indices,
            explanation,
            test_name,
            f"Mixed Review Q{len(rows) + 1}",
            path,
        )
    )
    question = "If you add 7 + 5, what is the sum?"
    choices = ["12", "11", "13", "10"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "7 + 5 = 12.",
            test_name,
            f"Mixed Review Q{len(rows) + 1}",
            path,
        )
    )
    question = "If a picture graph shows 4 suns for summer and 2 for winter, which season has more votes?"
    choices = ["Summer", "Winter", "They are equal", "Cannot tell"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "Summer has more votes.",
            test_name,
            f"Mixed Review Q{len(rows) + 1}",
            path,
        )
    )
    question = "Which tool would you use to measure how long a book is?"
    choices = ["Ruler", "Clock", "Scale", "Thermometer"]
    rows.append(
        build_multiple_choice(
            question,
            choices,
            0,
            "A ruler measures the length of a book.",
            test_name,
            f"Mixed Review Q{len(rows) + 1}",
            path,
        )
    )
    return rows[:15]


def main():
    datasets = [
        ("chapter01_numbers_and_place_value", "counting_sequences.csv", counting_questions),
        ("chapter01_numbers_and_place_value", "tens_and_ones.csv", tens_and_ones_questions),
        ("chapter01_numbers_and_place_value", "comparing_numbers.csv", comparing_numbers_questions),
        ("chapter02_number_writing_and_recognition", "writing_numbers.csv", writing_numbers_questions),
        ("chapter02_number_writing_and_recognition", "ordering_numbers.csv", ordering_numbers_questions),
        ("chapter03_addition", "adding_within_20.csv", add_within_20_questions),
        ("chapter03_addition", "addition_fact_families.csv", fact_families_addition_questions),
        ("chapter03_addition", "making_ten_strategy.csv", making_ten_questions),
        ("chapter03_addition", "addition_word_problems.csv", addition_word_problem_questions),
        ("chapter04_subtraction", "subtraction_within_20.csv", subtraction_within_20_questions),
        ("chapter04_subtraction", "subtraction_fact_families.csv", subtraction_fact_family_questions),
        ("chapter04_subtraction", "subtraction_word_problems.csv", subtraction_word_problem_questions),
        ("chapter05_addition_subtraction_to_100", "adding_tens.csv", adding_tens_questions),
        ("chapter05_addition_subtraction_to_100", "subtracting_tens.csv", subtracting_tens_questions),
        ("chapter05_addition_subtraction_to_100", "two_digit_plus_one_digit.csv", two_digit_plus_one_digit_questions),
        ("chapter06_geometry", "shapes_2d.csv", shapes_2d_questions),
        ("chapter06_geometry", "shapes_3d.csv", shapes_3d_questions),
        ("chapter06_geometry", "partitioning_shapes.csv", partitioning_shapes_questions),
        ("chapter07_measurement", "length_comparisons.csv", length_measurement_questions),
        ("chapter07_measurement", "height_comparisons.csv", height_measurement_questions),
        ("chapter07_measurement", "weight_comparisons.csv", weight_measurement_questions),
        ("chapter07_measurement", "nonstandard_units.csv", nonstandard_units_questions),
        ("chapter08_time", "time_to_hour.csv", time_to_hour_questions),
        ("chapter08_time", "time_to_half_hour.csv", time_to_half_hour_questions),
        ("chapter08_time", "time_of_day.csv", day_period_questions),
        ("chapter09_money", "coin_recognition.csv", coin_recognition_questions),
        ("chapter09_money", "counting_coins.csv", counting_coins_questions),
        ("chapter09_money", "money_word_problems.csv", money_word_problem_questions),
        ("chapter10_data_and_graphing", "collecting_data.csv", collecting_data_questions),
        ("chapter10_data_and_graphing", "making_graphs.csv", making_graphs_questions),
        ("chapter10_data_and_graphing", "reading_graphs.csv", reading_graphs_questions),
        ("chapter11_fractions_intro", "halves.csv", fractions_halves_questions),
        ("chapter11_fractions_intro", "quarters.csv", fractions_quarters_questions),
        ("chapter12_problem_solving_review", "addition_subtraction_word_problems.csv", problem_solving_add_sub_questions),
        ("chapter12_problem_solving_review", "mixed_review.csv", mixed_review_questions),
    ]

    for directory, filename, builder in datasets:
        rows = builder()
        if len(rows) != 15:
            raise ValueError(f"{filename} does not have 15 questions (found {len(rows)}).")
        write_csv(rows, directory, filename)


if __name__ == "__main__":
    main()

