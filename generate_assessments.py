from __future__ import annotations

import csv
import os
from dataclasses import dataclass
from itertools import cycle
from pathlib import Path
from typing import Callable, Iterable, List, Sequence

HEADER = [
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


NUMBER_WORDS = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen",
    20: "twenty",
}


COUNTING_SMALL_OBJECTS = [
    ("ladybug", "🐞"),
    ("star", "⭐"),
    ("balloon", "🎈"),
    ("car", "🚗"),
    ("flower", "🌼"),
    ("book", "📘"),
    ("cookie", "🍪"),
    ("heart", "❤️"),
    ("drum", "🥁"),
    ("rocket", "🚀"),
]

COUNTING_MEDIUM_OBJECTS = [
    ("pencil", "✏️"),
    ("balloon", "🎈"),
    ("shell", "🐚"),
    ("crayon", "🖍️"),
    ("block", "🧱"),
    ("button", "🔘"),
    ("kite", "🪁"),
    ("book", "📕"),
    ("drum", "🥁"),
    ("star", "⭐"),
]

COUNTING_LARGE_OBJECTS = [
    ("marble", "🔵"),
    ("sticker", "🏷️"),
    ("pencil", "✏️"),
    ("block", "🧱"),
    ("stone", "🪨"),
    ("bead", "🔹"),
    ("card", "🃏"),
    ("toy", "🧸"),
    ("bookmark", "📑"),
    ("button", "🔘"),
]


@dataclass
class TestInfo:
    chapter: str
    subtopic: str
    path: str

    @property
    def title_prefix(self) -> str:
        return self.subtopic


def pad_options(options: List[str]) -> List[str]:
    padded = list(options)
    while len(padded) < 7:
        padded.append("")
    return padded


def make_row(
    *,
    question: str,
    explanation: str,
    options: List[str],
    correct_indices: Iterable[int],
    test_info: TestInfo,
    title_item: str,
    qtype: str = "Multiple Choice",
    picture_url: str = "",
) -> List[str]:
    answer_letters = ",".join(
        chr(ord("A") + idx) for idx in sorted(set(correct_indices))
    )
    option_values = pad_options(options)
    return [
        question,
        answer_letters,
        explanation,
        picture_url,
        *option_values,
        test_info.chapter,
        "Question",
        title_item,
        qtype,
        test_info.path,
    ]


Generator = Callable[[TestInfo], List[List[str]]]


def arrange_numeric_options(
    correct: int,
    *,
    pool: Sequence[int],
    correct_index: int,
) -> List[str]:
    """Return four options placing the correct value at the desired index."""

    unique_values: List[int] = []
    seen = set()
    for value in pool:
        if value < 0:
            continue
        if value in seen:
            continue
        unique_values.append(value)
        seen.add(value)

    if correct not in seen:
        unique_values.insert(0, correct)
        seen.add(correct)

    filler = 0
    while len(unique_values) < 4:
        if filler not in seen:
            unique_values.append(filler)
            seen.add(filler)
        filler += 1

    trimmed = unique_values[:4]
    if correct not in trimmed:
        trimmed[-1] = correct

    # Place the correct value at the requested index by swapping.
    current_index = trimmed.index(correct)
    trimmed[current_index], trimmed[correct_index] = (
        trimmed[correct_index],
        trimmed[current_index],
    )

    return [str(value) for value in trimmed]


# Generators for different subtopics will be added below.


def pluralize(noun: str, count: int) -> str:
    if count == 1:
        return noun
    if noun.endswith("y") and not noun.endswith("ay"):
        return noun[:-1] + "ies"
    if noun.endswith("s"):
        return noun
    return noun + "s"


def format_count_set(count: int, noun: str, emoji: str | None = None) -> str:
    label = pluralize(noun, count)
    if emoji and count <= 10:
        return f"{emoji * count} ({count} {label})"
    return f"{count} {label}"


def generate_counting_questions(
    test_info: TestInfo,
    *,
    numbers: Sequence[int],
    objects: Sequence[tuple[str, str]],
    show_emoji: bool = True,
) -> List[List[str]]:
    rows: List[List[str]] = []
    templates = [
        "Count the {label}: {display} How many {plural} are there?",
        "How many {plural} do you see here: {display}?",
        "What number tells how many {plural} are shown: {display}?",
    ]

    for idx in range(12):
        number = numbers[idx % len(numbers)]
        noun, emoji = objects[idx % len(objects)]
        count_label = pluralize(noun, number)
        question_plural = pluralize(noun, max(number, 2))
        display: str
        if show_emoji and number <= 10:
            display = emoji * number
        else:
            display = f"{number} {count_label}"
        template = templates[idx % len(templates)]
        question = template.format(
            label=question_plural,
            plural=question_plural,
            display=display,
        )
        correct_index = idx % 4
        option_pool = [
            number,
            number - 1,
            number + 1,
            number + 2,
            number - 2,
            number + 3,
        ]
        options = arrange_numeric_options(
            number,
            pool=option_pool,
            correct_index=correct_index,
        )
        explanation = (
            f"The set shows {number} {count_label}, so {number} is the matching number."
        )
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=options,
                correct_indices=[correct_index],
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{idx + 1}",
            )
        )

    for extra_idx in range(3):
        number = numbers[(12 + extra_idx) % len(numbers)]
        noun, emoji = objects[(12 + extra_idx) % len(objects)]
        count_label = pluralize(noun, number)
        question_plural = pluralize(noun, max(number, 2))
        option_sets: List[str] = []
        correct_indices: List[int] = []
        counts = [
            number,
            number + 1,
            number - 1,
            number,
            number + 2,
        ]
        for opt_idx, count in enumerate(counts):
            display = format_count_set(count, noun, emoji if show_emoji else None)
            option_sets.append(display)
            if count == number:
                correct_indices.append(opt_idx)
        question = f"Select each option that shows exactly {number} {question_plural}."
        explanation = (
            f"Any option with {number} {count_label} is correct; the others show different amounts."
        )
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=option_sets,
                correct_indices=correct_indices,
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{12 + extra_idx + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def generate_comparing_questions(test_info: TestInfo) -> List[List[str]]:
    rows: List[List[str]] = []
    pairs = [
        (3, 5),
        (7, 2),
        (6, 6),
        (9, 4),
        (2, 2),
        (8, 10),
        (5, 3),
        (4, 4),
        (1, 3),
        (10, 7),
        (6, 8),
        (9, 9),
        (7, 5),
        (3, 3),
        (2, 4),
    ]
    objects = [
        "apples",
        "pencils",
        "shells",
        "stickers",
        "blocks",
        "cars",
        "marbles",
        "books",
        "balloons",
        "cookies",
        "ducks",
        "crayons",
        "gems",
        "turtles",
        "coins",
    ]

    for idx in range(12):
        a, b = pairs[idx]
        noun = objects[idx]
        plural = pluralize(noun, 2)
        if idx % 3 == 0:
            if a == b:
                question = (
                    f"Team A and Team B each sorted {a} {plural}. How do the amounts compare?"
                )
                options = [
                    "Team A has more",
                    "Team B has more",
                    "They have the same number",
                    "Team B has two more",
                ]
                correct_index = 2
                explanation = "Both teams have the same count, so their amounts are equal."
            else:
                question = (
                    f"Group A has {a} {plural} and Group B has {b} {plural}. Which group has more?"
                )
                options = [
                    "Group A",
                    "Group B",
                    "They are equal",
                    "Not enough information",
                ]
                if a > b:
                    correct_index = 0
                    explanation = (
                        f"{a} is greater than {b}, so Group A has more {plural}."
                    )
                else:
                    correct_index = 1
                    explanation = (
                        f"{b} is greater than {a}, so Group B has more {plural}."
                    )
        elif idx % 3 == 1:
            question = f"Which symbol makes this comparison true: {a} __ {b}?"
            options = ["<", ">", "=", "+"]
            if a > b:
                correct_index = 1
                explanation = f"{a} is greater than {b}, so > makes the sentence true."
            elif a < b:
                correct_index = 0
                explanation = f"{a} is less than {b}, so < makes the sentence true."
            else:
                correct_index = 2
                explanation = f"{a} equals {b}, so = is correct."
        else:
            question = "Which statement about the numbers is true?"
            statements = [
                f"{a} > {b}",
                f"{a} < {b}",
                f"{a} = {b}",
                "They cannot be compared",
            ]
            if a > b:
                correct_index = 0
                explanation = f"{a} is greater than {b}, so {a} > {b} is true."
            elif a < b:
                correct_index = 1
                explanation = f"{a} is less than {b}, so {a} < {b} is true."
            else:
                correct_index = 2
                explanation = f"The two numbers match, so {a} = {b} is true."
            options = statements

        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=options,
                correct_indices=[correct_index],
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{idx + 1}",
            )
        )

    for extra_idx in range(3):
        a, b = pairs[12 + extra_idx]
        noun = objects[12 + extra_idx]
        plural = pluralize(noun, 2)
        statements = [
            f"{a} is greater than {b}",
            f"{a} is less than {b}",
            f"{a} equals {b}",
            f"{b} is greater than {a}",
            "They have the same amount",
        ]
        truth_map = []
        if a > b:
            truth_map = [True, False, False, False, False]
        elif a < b:
            truth_map = [False, True, False, True, False]
        else:
            truth_map = [False, False, True, False, True]
        correct_indices = [idx for idx, truth in enumerate(truth_map) if truth]
        question = (
            f"Select each true statement about {a} and {b} {plural}."
        )
        explanation = "Choose the statements that correctly describe how the two numbers compare."
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=statements,
                correct_indices=correct_indices,
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{12 + extra_idx + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def generate_number_recognition_questions(
    test_info: TestInfo,
    *,
    numbers: Sequence[int],
) -> List[List[str]]:
    rows: List[List[str]] = []
    for idx in range(12):
        number = numbers[idx % len(numbers)]
        word = NUMBER_WORDS[number]
        if idx % 2 == 0:
            question = f"Which numeral matches the word \"{word}\"?"
            option_pool = [
                number,
                number + 1,
                number - 1,
                number + 2,
                number - 2,
            ]
            correct_index = idx % 4
            options = arrange_numeric_options(
                number,
                pool=option_pool,
                correct_index=correct_index,
            )
            explanation = f"The word {word} stands for the numeral {number}."
        else:
            question = f"Which word names the numeral {number}?"
            distractors = [
                NUMBER_WORDS.get((number + 1) % 21, "twenty"),
                NUMBER_WORDS.get(abs(number - 1), NUMBER_WORDS[number]),
                NUMBER_WORDS.get((number + 2) % 21, "zero"),
            ]
            options = [word] + [d for d in distractors if d != word]
            while len(options) < 4:
                options.append(NUMBER_WORDS[(number + len(options)) % 21])
            options = options[:4]
            correct_index = 0
            options[0], options[idx % 4] = options[idx % 4], options[0]
            correct_index = idx % 4
            explanation = f"The numeral {number} is written with the word {word}."
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=options,
                correct_indices=[correct_index],
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{idx + 1}",
            )
        )

    select_prompts = [
        (
            "Select each numeral that is less than 5.",
            ["2", "7", "4", "9", "1"],
            {0, 2, 4},
        ),
        (
            "Select each word that names an even number.",
            ["three", "six", "ten", "five", "eight"],
            {1, 2, 4},
        ),
        (
            "Select each number word that is greater than 8.",
            ["nine", "four", "eleven", "seven", "ten"],
            {0, 2, 4},
        ),
    ]
    for offset, (prompt, opts, correct_set) in enumerate(select_prompts):
        rows.append(
            make_row(
                question=prompt,
                explanation="Choose every option that fits the rule in the prompt.",
                options=opts,
                correct_indices=sorted(correct_set),
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{12 + offset + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def generate_writing_numbers_questions(test_info: TestInfo) -> List[List[str]]:
    rows: List[List[str]] = []
    prompts = [
        (
            7,
            "You trace the word 'seven' on dotted lines. Which numeral do you write?",
            "Writing the word seven produces the numeral 7.",
        ),
        (
            11,
            "You draw a straight line down, lift your pencil, and draw another straight line right beside it. What number did you make?",
            "Two straight lines side by side make the numeral 11.",
        ),
        (
            4,
            "You trace a square corner pattern that looks like an open chair. Which numeral are you forming?",
            "The open chair pattern describes how you write the numeral 4.",
        ),
        (
            8,
            "You write a small circle on top of a bigger circle. What number does that create?",
            "A stacked pair of circles is how you write the numeral 8.",
        ),
        (
            15,
            "You write a 1 and then a 5 right next to it. Which number did you write?",
            "A 1 followed by a 5 makes the numeral 15.",
        ),
        (
            0,
            "You carefully trace an oval without any corners. Which numeral are you practicing?",
            "An oval loop is how you write the numeral 0.",
        ),
        (
            12,
            "You trace a 1 and then a 2 to show a dozen. What number is that?",
            "A 1 with a 2 beside it is the numeral 12.",
        ),
        (
            3,
            "You draw two smooth curves stacked on each other without lifting your pencil. Which number did you write?",
            "Two stacked curves describe the numeral 3.",
        ),
        (
            6,
            "You start with a small loop and close it with a curved tail. Which numeral does that make?",
            "A loop with a tail is how you write the numeral 6.",
        ),
        (
            9,
            "You make a small circle on top and draw a straight line down. What number did you write?",
            "A circle with a straight line below forms the numeral 9.",
        ),
        (
            14,
            "You write a 1 and then a 4 to show a teen number. Which numeral is that?",
            "A 1 followed by a 4 makes the numeral 14.",
        ),
        (
            2,
            "You write a curved top, slide down, and finish with a straight line. What numeral did you finish?",
            "That writing motion describes the numeral 2.",
        ),
    ]

    for idx, (number, question, explanation) in enumerate(prompts):
        option_pool = [
            number,
            number + 1,
            number - 1,
            number + 2,
            number - 2,
        ]
        correct_index = idx % 4
        options = arrange_numeric_options(
            number,
            pool=option_pool,
            correct_index=correct_index,
        )
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=options,
                correct_indices=[correct_index],
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{idx + 1}",
            )
        )

    select_sets = [
        (
            "Select each numeral that uses only straight lines when you write it.",
            ["1", "3", "4", "8", "11"],
            {0, 2, 4},
        ),
        (
            "Select each way to write the number twelve.",
            ["12", "twenty-one", "1 and 2", "21", "twelve"],
            {0, 2, 4},
        ),
        (
            "Select each number that needs two digits when you write it.",
            ["6", "15", "8", "20", "3"],
            {1, 3},
        ),
    ]
    for offset, (prompt, opts, correct) in enumerate(select_sets):
        rows.append(
            make_row(
                question=prompt,
                explanation="Mark every option that matches the description for writing numbers.",
                options=opts,
                correct_indices=sorted(correct),
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{len(prompts) + offset + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def build_mc_rows(
    test_info: TestInfo,
    prompts: Sequence[tuple[str, Sequence[str], int, str]],
    *,
    start_index: int = 1,
) -> List[List[str]]:
    rows: List[List[str]] = []
    for offset, (question, options, correct_index, explanation) in enumerate(prompts):
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=list(options),
                correct_indices=[correct_index],
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{start_index + offset}",
            )
        )
    return rows


def generate_2d_shapes_questions(test_info: TestInfo) -> List[List[str]]:
    mc_prompts = [
        (
            "Which 2D shape has no corners?",
            ["Circle", "Square", "Triangle", "Rectangle"],
            0,
            "A circle is round with no corners.",
        ),
        (
            "Which shape has exactly three straight sides?",
            ["Triangle", "Circle", "Oval", "Square"],
            0,
            "A triangle is the only option with three straight sides.",
        ),
        (
            "Which shape has four equal sides and four corners?",
            ["Rectangle", "Oval", "Square", "Triangle"],
            2,
            "A square has four equal sides and four corners.",
        ),
        (
            "Which shape looks most like a door?",
            ["Rectangle", "Triangle", "Circle", "Oval"],
            0,
            "Doors are usually rectangles with four right angles.",
        ),
        (
            "Which shape is a stretched circle?",
            ["Oval", "Square", "Triangle", "Rectangle"],
            0,
            "An oval is a stretched-out circle.",
        ),
        (
            "Which shape has four sides where two are longer than the others?",
            ["Rectangle", "Square", "Triangle", "Circle"],
            0,
            "A rectangle has opposite sides that can be different lengths.",
        ),
        (
            "Which shape matches a slice of pizza with three points?",
            ["Triangle", "Circle", "Rectangle", "Oval"],
            0,
            "A pizza slice often looks like a triangle.",
        ),
        (
            "Which shape would work best for a clock face?",
            ["Circle", "Triangle", "Square", "Oval"],
            0,
            "Most clocks are circles so the hands can turn easily.",
        ),
        (
            "Which shape could you use to draw a window with all sides equal?",
            ["Square", "Rectangle", "Triangle", "Oval"],
            0,
            "A square has four sides the same length, perfect for a window with equal sides.",
        ),
        (
            "Which shape is curved all around but longer than it is wide?",
            ["Oval", "Circle", "Rectangle", "Triangle"],
            0,
            "An oval is longer in one direction but still curved all the way around.",
        ),
        (
            "Which shape has three corners and three sides?",
            ["Triangle", "Circle", "Square", "Oval"],
            0,
            "A triangle always has three corners and three sides.",
        ),
        (
            "Which shape has four right angles and straight sides?",
            ["Rectangle", "Circle", "Triangle", "Oval"],
            0,
            "A rectangle has four right angles.",
        ),
    ]

    rows = build_mc_rows(test_info, mc_prompts)

    select_sets = [
        (
            "Select each shape that has straight sides.",
            ["Circle", "Square", "Triangle", "Oval", "Rectangle"],
            {1, 2, 4},
            "Square, triangle, and rectangle all have straight sides.",
        ),
        (
            "Select each shape with four corners.",
            ["Triangle", "Circle", "Rectangle", "Square", "Oval"],
            {2, 3},
            "Rectangles and squares have four corners.",
        ),
        (
            "Select each shape that is round.",
            ["Triangle", "Circle", "Square", "Oval", "Rectangle"],
            {1, 3},
            "Circle and oval are round shapes.",
        ),
    ]

    for offset, (question, options, correct, explanation) in enumerate(select_sets):
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=list(options),
                correct_indices=sorted(correct),
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{12 + offset + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def generate_3d_shapes_questions(test_info: TestInfo) -> List[List[str]]:
    mc_prompts = [
        (
            "Which 3D shape can roll because it is round on every side?",
            ["Sphere", "Cube", "Cylinder", "Cone"],
            0,
            "A sphere is round all over so it rolls easily.",
        ),
        (
            "Which shape looks like a can of soup?",
            ["Cylinder", "Cone", "Sphere", "Cube"],
            0,
            "A cylinder has two circle bases like a can.",
        ),
        (
            "Which shape has flat square faces on every side?",
            ["Cube", "Sphere", "Cone", "Cylinder"],
            0,
            "A cube is made of square faces.",
        ),
        (
            "Which shape comes to a point and has a circle base?",
            ["Cone", "Sphere", "Cube", "Cylinder"],
            0,
            "A cone has a circle base and a point at the top.",
        ),
        (
            "Which shape would match an ice-cream scoop?",
            ["Sphere", "Cube", "Cone", "Cylinder"],
            0,
            "An ice-cream scoop is sphere-shaped.",
        ),
        (
            "Which shape is best for stacking like boxes?",
            ["Cube", "Sphere", "Cone", "Cylinder"],
            0,
            "Cubes have flat faces that stack neatly.",
        ),
        (
            "Which shape has two circle faces and one curved side?",
            ["Cylinder", "Cube", "Sphere", "Cone"],
            0,
            "A cylinder has two circles and a curved surface.",
        ),
        (
            "Which shape could be the body of a party hat?",
            ["Cone", "Sphere", "Cylinder", "Cube"],
            0,
            "Party hats are cones with pointed tops.",
        ),
        (
            "Which shape has only curved surfaces and no edges?",
            ["Sphere", "Cylinder", "Cube", "Cone"],
            0,
            "A sphere has no edges or flat faces.",
        ),
        (
            "Which shape would match a cardboard box?",
            ["Cube", "Sphere", "Cone", "Cylinder"],
            0,
            "A box is shaped like a cube or rectangular prism; the cube choice fits here.",
        ),
        (
            "Which shape stands on a circle but has a point on top?",
            ["Cone", "Cylinder", "Sphere", "Cube"],
            0,
            "A cone stands on a circle base with a point above it.",
        ),
        (
            "Which shape is most like a drum?",
            ["Cylinder", "Sphere", "Cube", "Cone"],
            0,
            "Drums are cylinder-shaped with circle tops and bottoms.",
        ),
    ]

    rows = build_mc_rows(test_info, mc_prompts)

    select_sets = [
        (
            "Select each shape that can roll easily.",
            ["Cube", "Sphere", "Cylinder", "Cone", "Pyramid"],
            {1, 2, 3},
            "Spheres, cylinders, and cones all roll.",
        ),
        (
            "Select each shape that has flat faces.",
            ["Sphere", "Cube", "Cylinder", "Cone", "Prism"],
            {1, 2, 3, 4},
            "Cube, cylinder, cone, and prism have at least one flat face; the sphere does not.",
        ),
        (
            "Select each shape with a circle base.",
            ["Cube", "Cone", "Sphere", "Cylinder", "Rectangular prism"],
            {1, 3},
            "Cones and cylinders have circle bases.",
        ),
    ]

    for offset, (question, options, correct, explanation) in enumerate(select_sets):
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=list(options),
                correct_indices=sorted(correct),
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{12 + offset + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def generate_shape_sorting_questions(test_info: TestInfo) -> List[List[str]]:
    mc_prompts = [
        (
            "Which shape belongs with the group of red triangles?",
            [
                "Small red triangle",
                "Red circle",
                "Blue triangle",
                "Green square",
            ],
            0,
            "Only the red triangle matches both the color and shape.",
        ),
        (
            "Which shape fits with the large green circles?",
            [
                "Large green circle",
                "Small green circle",
                "Large blue circle",
                "Large green square",
            ],
            0,
            "Large, green, and circular matches the group.",
        ),
        (
            "Which shape should go with the small blue squares?",
            [
                "Small blue square",
                "Large blue square",
                "Small blue triangle",
                "Small red square",
            ],
            0,
            "Only the small blue square matches size, color, and shape.",
        ),
        (
            "Which item belongs in the set of tall yellow rectangles?",
            [
                "Tall yellow rectangle",
                "Short yellow rectangle",
                "Tall yellow triangle",
                "Tall blue rectangle",
            ],
            0,
            "Tall, yellow, and rectangle matches the rule.",
        ),
        (
            "Which shape matches the group of wide orange ovals?",
            [
                "Wide orange oval",
                "Tall orange oval",
                "Wide orange circle",
                "Wide blue oval",
            ],
            0,
            "Only the wide orange oval fits the description.",
        ),
        (
            "Which piece belongs with skinny purple rectangles?",
            [
                "Skinny purple rectangle",
                "Wide purple rectangle",
                "Skinny purple triangle",
                "Skinny green rectangle",
            ],
            0,
            "It must be skinny, purple, and a rectangle.",
        ),
        (
            "Which card goes with the round blue shapes?",
            [
                "Blue circle",
                "Blue square",
                "Red circle",
                "Blue triangle",
            ],
            0,
            "Round and blue describes the circle.",
        ),
        (
            "Which shape joins the stack of medium green triangles?",
            [
                "Medium green triangle",
                "Medium green square",
                "Medium blue triangle",
                "Small green triangle",
            ],
            0,
            "It must be medium, green, and triangular.",
        ),
        (
            "Which tile belongs with the tiny red circles?",
            [
                "Tiny red circle",
                "Tiny red square",
                "Tiny blue circle",
                "Big red circle",
            ],
            0,
            "Only the tiny red circle fits all three traits.",
        ),
        (
            "Which piece fits the group of large yellow stars?",
            [
                "Large yellow star",
                "Small yellow star",
                "Large yellow triangle",
                "Large green star",
            ],
            0,
            "The group asks for large, yellow stars.",
        ),
        (
            "Which block matches the short orange rectangles?",
            [
                "Short orange rectangle",
                "Tall orange rectangle",
                "Short orange triangle",
                "Short blue rectangle",
            ],
            0,
            "It must be short, orange, and a rectangle.",
        ),
        (
            "Which piece goes with the blue triangles with stripes?",
            [
                "Striped blue triangle",
                "Striped blue square",
                "Solid blue triangle",
                "Striped red triangle",
            ],
            0,
            "It needs to be striped, blue, and a triangle.",
        ),
    ]

    rows = build_mc_rows(test_info, mc_prompts)

    select_sets = [
        (
            "Select each description that belongs with small purple circles.",
            [
                "Small purple circle",
                "Small purple square",
                "Tiny purple circle",
                "Small blue circle",
                "Small purple oval",
            ],
            {0, 2},
            "Only the options that are circles and purple fit; size must be small or tiny.",
        ),
        (
            "Select each option that should join the group of red squares.",
            [
                "Large red square",
                "Small blue square",
                "Red rectangle",
                "Medium red square",
                "Large red circle",
            ],
            {0, 3},
            "Only the red squares belong in the group.",
        ),
        (
            "Select each item that belongs with the tall green triangles.",
            [
                "Tall green triangle",
                "Tall green rectangle",
                "Tall blue triangle",
                "Tall green triangle with dots",
                "Short green triangle",
            ],
            {0, 3},
            "The shape must be a tall green triangle; decorated versions still fit.",
        ),
    ]

    for offset, (question, options, correct, explanation) in enumerate(select_sets):
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=list(options),
                correct_indices=sorted(correct),
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{12 + offset + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def generate_ab_patterns_questions(test_info: TestInfo) -> List[List[str]]:
    mc_prompts = [
        (
            "Pattern: 🔴🔵🔴🔵 __. What comes next to continue the AB pattern?",
            ["🔴", "🔵", "🟢", "⚪"],
            0,
            "The pattern alternates red, blue, so red comes next.",
        ),
        (
            "Pattern: 🟩⬜🟩⬜ __. Which tile should come next?",
            ["🟩", "⬜", "⬛", "🟥"],
            0,
            "Green, white repeats, so green follows.",
        ),
        (
            "Pattern: 🍎🍌🍎🍌 __. Choose the next fruit.",
            ["🍎", "🍌", "🍇", "🍐"],
            0,
            "Apple, banana repeats so an apple comes next.",
        ),
        (
            "Pattern: 🐱🐶🐱🐶 __. What animal should come next?",
            ["🐱", "🐶", "🐰", "🐭"],
            0,
            "Cat, dog repeats with a cat next.",
        ),
        (
            "Pattern: ◻️▲◻️▲ __. Which shape completes the pattern?",
            ["◻️", "▲", "⚫", "⬢"],
            0,
            "Square, triangle repeats so the square returns.",
        ),
        (
            "Pattern: 🎵🎶🎵🎶 __. What music note comes next?",
            ["🎵", "🎶", "🎼", "🎤"],
            0,
            "The pattern alternates 🎵 and 🎶, so 🎵 is next.",
        ),
        (
            "Pattern: ☀️🌧️☀️🌧️ __. Which weather symbol continues the pattern?",
            ["☀️", "🌧️", "🌈", "❄️"],
            0,
            "Sun, rain repeats with sun next.",
        ),
        (
            "Pattern: 🚌🚗🚌🚗 __. What vehicle should come next?",
            ["🚌", "🚗", "🚲", "🚕"],
            0,
            "Bus, car repeats, so bus is next.",
        ),
        (
            "Pattern: 🔺⚪🔺⚪ __. Which shape keeps the AB pattern going?",
            ["🔺", "⚪", "🔻", "🟦"],
            0,
            "Triangle, circle repeats; a triangle is next.",
        ),
        (
            "Pattern: 🎈🎂🎈🎂 __. Which symbol comes next?",
            ["🎈", "🎂", "🎁", "🎉"],
            0,
            "Balloon, cake repeats with another balloon.",
        ),
        (
            "Pattern: 🟠🟣🟠🟣 __. Choose the next color.",
            ["🟠", "🟣", "🟡", "🔵"],
            0,
            "Orange, purple repeats with orange next.",
        ),
        (
            "Pattern: 🐟🌿🐟🌿 __. Which symbol continues the AB pattern?",
            ["🐟", "🌿", "🐚", "🍀"],
            0,
            "Fish, leaf repeats, so fish returns.",
        ),
    ]

    rows = build_mc_rows(test_info, mc_prompts)

    select_sets = [
        (
            "Select each pattern that shows an AB repetition.",
            [
                "🟥🟩🟥🟩",
                "🟦🟦🟧🟧",
                "⭐️🌙⭐️🌙",
                "🍓🍓🍇",
                "⚫⚪⚫",
            ],
            {0, 2},
            "Only the first and third options alternate two different items.",
        ),
        (
            "Select each sequence that would continue with a triangle next.",
            [
                "▲●▲●",
                "▲▲●▲",
                "●▲●▲",
                "▲●●▲",
                "▲●▲●▲",
            ],
            {0, 2, 4},
            "In those sequences the triangle returns after a circle.",
        ),
        (
            "Select each description that matches an AB color pattern.",
            [
                "Red, blue, red, blue",
                "Green, green, yellow",
                "Orange, purple, orange, purple",
                "Blue, blue, blue",
                "Pink, yellow, green",
            ],
            {0, 2},
            "Only the first and third descriptions alternate two colors.",
        ),
    ]

    for offset, (question, options, correct, explanation) in enumerate(select_sets):
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=list(options),
                correct_indices=sorted(correct),
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{12 + offset + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def generate_abc_patterns_questions(test_info: TestInfo) -> List[List[str]]:
    mc_prompts = [
        (
            "Pattern: 🔴🟢🔵🔴🟢 __. What color comes next in the ABC pattern?",
            ["🔵", "🔴", "🟢", "🟡"],
            0,
            "The pattern repeats red, green, blue; blue comes next.",
        ),
        (
            "Pattern: 🍎🍌🍇🍎🍌 __. Choose the next fruit.",
            ["🍇", "🍎", "🍌", "🍉"],
            0,
            "Apple, banana, grape repeats with grape next.",
        ),
        (
            "Pattern: 🟦⬜⬛🟦⬜ __. Which tile should follow?",
            ["⬛", "🟦", "⬜", "🟥"],
            0,
            "Blue, white, black repeats; black follows.",
        ),
        (
            "Pattern: 🐱🐶🐰🐱🐶 __. What animal comes next?",
            ["🐰", "🐱", "🐶", "🐭"],
            0,
            "Cat, dog, rabbit repeats; rabbit returns.",
        ),
        (
            "Pattern: 🎵🎶🎼🎵🎶 __. Choose the next note.",
            ["🎼", "🎵", "🎶", "🎤"],
            0,
            "The notes repeat 🎵, 🎶, 🎼; 🎼 comes next.",
        ),
        (
            "Pattern: ☀️🌧️❄️☀️🌧️ __. Which weather symbol continues the pattern?",
            ["❄️", "☀️", "🌧️", "🌈"],
            0,
            "Sun, rain, snow repeats with snow next.",
        ),
        (
            "Pattern: 🔺⚪🟫🔺⚪ __. What shape comes next?",
            ["🟫", "🔺", "⚪", "🔻"],
            0,
            "Triangle, circle, brown square repeats with brown square next.",
        ),
        (
            "Pattern: 🚌🚲🚗🚌🚲 __. Which vehicle should follow?",
            ["🚗", "🚌", "🚲", "🚕"],
            0,
            "Bus, bike, car repeats, so car comes next.",
        ),
        (
            "Pattern: 🎈🎁🎂🎈🎁 __. Choose the symbol that continues the pattern.",
            ["🎂", "🎈", "🎁", "🎉"],
            0,
            "Balloon, present, cake repeats; cake follows.",
        ),
        (
            "Pattern: 🐠🐢🐸🐠🐢 __. What animal should appear next?",
            ["🐸", "🐠", "🐢", "🐙"],
            0,
            "Fish, turtle, frog repeats with frog next.",
        ),
        (
            "Pattern: 🟠🟣🟢🟠🟣 __. Which color comes next?",
            ["🟢", "🟠", "🟣", "🔵"],
            0,
            "Orange, purple, green repeats with green next.",
        ),
        (
            "Pattern: 📗📘📙📗📘 __. Which book color should come next?",
            ["📙", "📗", "📘", "📕"],
            0,
            "Green, blue, orange repeats; orange book follows.",
        ),
    ]

    rows = build_mc_rows(test_info, mc_prompts)

    select_sets = [
        (
            "Select each pattern that shows an ABC repeat.",
            [
                "🔴🟢🔵🔴🟢",
                "🔵🔵🟡",
                "🟧🟪🟨🟧🟪",
                "🍎🍎🍌",
                "🐶🐱🐰🐶🐱",
            ],
            {0, 2, 4},
            "Options 1, 3, and 5 repeat three different items in order.",
        ),
        (
            "Select each description that matches an ABC pattern.",
            [
                "circle, square, triangle, circle, square",
                "red, red, blue",
                "cat, dog, bird, cat, dog",
                "sun, moon, star, sun, moon",
                "apple, banana, apple",
            ],
            {0, 2, 3},
            "Descriptions 1, 3, and 4 list three different items repeating in order.",
        ),
        (
            "Select each sequence that would continue with a snowflake next.",
            [
                "☀️🌧️❄️☀️🌧️",
                "❄️☀️🌧️❄️☀️",
                "🌧️❄️☀️🌧️❄️",
                "☀️☀️❄️☀️",
                "☀️🌧️☀️🌧️",
            ],
            {0, 2},
            "The first and third sequences follow a sun, rain, snow pattern, so snow is next.",
        ),
    ]

    for offset, (question, options, correct, explanation) in enumerate(select_sets):
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=list(options),
                correct_indices=sorted(correct),
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{12 + offset + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def generate_sorting_color_size_shape_questions(test_info: TestInfo) -> List[List[str]]:
    mc_prompts = [
        (
            "Which item belongs in the bin labeled red toys?",
            [
                "Red car",
                "Blue ball",
                "Yellow truck",
                "Green dinosaur",
            ],
            0,
            "Only the red car matches the red toys bin.",
        ),
        (
            "Which object should go with the group of large stuffed animals?",
            [
                "Big teddy bear",
                "Tiny kitten figurine",
                "Small stuffed turtle",
                "Medium rubber duck",
            ],
            0,
            "The big teddy bear matches large stuffed animals.",
        ),
        (
            "Which picture card belongs with the round shapes?",
            [
                "Circle button",
                "Square tile",
                "Triangle sign",
                "Rectangle card",
            ],
            0,
            "Only the circle button is round.",
        ),
        (
            "Which object fits the set of small blue blocks?",
            [
                "Small blue block",
                "Large blue block",
                "Small red block",
                "Small green block",
            ],
            0,
            "It must be small, blue, and a block.",
        ),
        (
            "Which sock goes with the striped socks pile?",
            [
                "Striped sock",
                "Polka-dot sock",
                "Plain blue sock",
                "Star sock",
            ],
            0,
            "Only the striped sock matches the striped pile.",
        ),
        (
            "Which leaf belongs in the group of long leaves?",
            [
                "Long green leaf",
                "Short green leaf",
                "Round leaf",
                "Tiny leaf",
            ],
            0,
            "The long green leaf fits the long leaves group.",
        ),
        (
            "Which button goes with the triangle buttons?",
            [
                "Triangle button",
                "Circle button",
                "Square button",
                "Oval button",
            ],
            0,
            "It must be a triangle button.",
        ),
        (
            "Which toy should join the heavy toys basket?",
            [
                "Metal dump truck",
                "Feather",
                "Foam ball",
                "Paper airplane",
            ],
            0,
            "The metal dump truck is heavy compared with the others.",
        ),
        (
            "Which crayon belongs with the warm color set?",
            [
                "Orange crayon",
                "Green crayon",
                "Blue crayon",
                "Purple crayon",
            ],
            0,
            "Orange is a warm color.",
        ),
        (
            "Which shoe fits the group of smallest shoes?",
            [
                "Baby shoe",
                "Teen shoe",
                "Adult shoe",
                "Boot",
            ],
            0,
            "The baby shoe is the smallest size.",
        ),
        (
            "Which hat belongs with the round hats?",
            [
                "Beanie hat",
                "Pointed party hat",
                "Sun visor",
                "Top hat",
            ],
            0,
            "A beanie is round and soft to match the group.",
        ),
        (
            "Which block should go in the stack of tall blocks?",
            [
                "Tall block",
                "Short block",
                "Flat block",
                "Wide block",
            ],
            0,
            "Only the tall block belongs in the tall stack.",
        ),
    ]

    rows = build_mc_rows(test_info, mc_prompts)

    select_sets = [
        (
            "Select each item that belongs with the red toys.",
            [
                "Red ball",
                "Blue truck",
                "Red kite",
                "Yellow doll",
                "Red puzzle piece",
            ],
            {0, 2, 4},
            "All red items belong with the red toys.",
        ),
        (
            "Select each object that should go with the light-weight items.",
            [
                "Feather",
                "Wooden block",
                "Paper leaf",
                "Metal car",
                "Balloon",
            ],
            {0, 2, 4},
            "Feather, paper leaf, and balloon are light-weight.",
        ),
        (
            "Select each description that matches the group of large triangles.",
            [
                "Large red triangle",
                "Small red triangle",
                "Large blue triangle",
                "Large red square",
                "Large green triangle",
            ],
            {0, 2, 4},
            "Any triangle that is large belongs, no matter the color.",
        ),
    ]

    for offset, (question, options, correct, explanation) in enumerate(select_sets):
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=list(options),
                correct_indices=sorted(correct),
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{12 + offset + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def generate_addition_numeric_questions(
    test_info: TestInfo,
    *,
    pairs: Sequence[tuple[int, int]],
    select_sets: Sequence[tuple[str, Sequence[str], Sequence[int], str]],
) -> List[List[str]]:
    rows: List[List[str]] = []
    templates = [
        "What is {a} + {b}?",
        "Solve: {a} + {b} = __",
        "Add {a} and {b}. What is the sum?",
    ]
    for idx, (a, b) in enumerate(pairs):
        total = a + b
        template = templates[idx % len(templates)]
        question = template.format(a=a, b=b)
        option_pool = [total, total + 1, total - 1, total + 2, total - 2]
        correct_index = idx % 4
        options = arrange_numeric_options(
            total,
            pool=option_pool,
            correct_index=correct_index,
        )
        explanation = f"{a} plus {b} equals {total}."
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=options,
                correct_indices=[correct_index],
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{idx + 1}",
            )
        )

    for offset, (question, options, correct_indices, explanation) in enumerate(select_sets):
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=list(options),
                correct_indices=correct_indices,
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{len(pairs) + offset + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def generate_addition_within_five_questions(test_info: TestInfo) -> List[List[str]]:
    pairs = [
        (0, 2),
        (1, 3),
        (2, 2),
        (4, 1),
        (3, 0),
        (1, 4),
        (2, 3),
        (5, 0),
        (0, 5),
        (3, 1),
        (0, 4),
        (2, 1),
    ]
    select_sets = [
        (
            "Select each equation that equals 4.",
            ["1 + 3", "2 + 2", "4 + 0", "3 + 2", "0 + 4"],
            [0, 1, 2, 4],
            "These equations make 4; 3 + 2 makes 5 instead.",
        ),
        (
            "Select each expression that has a sum of 5.",
            ["3 + 2", "4 + 1", "2 + 3", "1 + 1", "0 + 5"],
            [0, 1, 2, 4],
            "Any pair that totals 5 is correct.",
        ),
        (
            "Select each sum that is less than 3.",
            ["0 + 0", "1 + 1", "2 + 2", "1 + 0", "3 + 0"],
            [0, 1, 3],
            "The first, second, and fourth expressions are less than 3.",
        ),
    ]
    return generate_addition_numeric_questions(
        test_info,
        pairs=pairs,
        select_sets=select_sets,
    )


def generate_addition_within_ten_questions(test_info: TestInfo) -> List[List[str]]:
    pairs = [
        (3, 4),
        (5, 2),
        (6, 3),
        (7, 1),
        (4, 5),
        (8, 2),
        (9, 1),
        (6, 4),
        (2, 7),
        (10, 0),
        (3, 6),
        (5, 4),
    ]
    select_sets = [
        (
            "Select each expression that equals 8.",
            ["3 + 5", "6 + 2", "4 + 4", "7 + 1", "2 + 6"],
            [0, 1, 2, 3, 4],
            "All listed expressions total 8.",
        ),
        (
            "Select each equation with a sum of 10.",
            ["8 + 2", "7 + 2", "5 + 5", "6 + 4", "10 + 0"],
            [0, 2, 3, 4],
            "Those sums equal 10; 7 + 2 equals 9 so it does not belong.",
        ),
        (
            "Select each sum that is greater than 6.",
            ["3 + 3", "4 + 5", "2 + 6", "1 + 5", "5 + 4"],
            [1, 2, 4],
            "Only the highlighted expressions total more than 6.",
        ),
    ]
    return generate_addition_numeric_questions(
        test_info,
        pairs=pairs,
        select_sets=select_sets,
    )


def generate_addition_with_objects_questions(test_info: TestInfo) -> List[List[str]]:
    stories = [
        (2, 1, "apple", "on the table"),
        (3, 2, "shell", "by the shore"),
        (1, 4, "pencil", "in the cup"),
        (2, 3, "car", "on the rug"),
        (4, 1, "block", "in the tower"),
        (3, 1, "frog", "by the pond"),
        (2, 2, "book", "on the shelf"),
        (5, 2, "sticker", "on the chart"),
        (4, 3, "balloon", "at the party"),
        (1, 5, "flower", "in the vase"),
        (3, 4, "marble", "in the jar"),
        (2, 3, "cookie", "on the plate"),
    ]
    rows: List[List[str]] = []
    for idx, (first, second, noun, place) in enumerate(stories):
        total = first + second
        plural_noun = pluralize(noun, total)
        question = (
            f"There are {first} {pluralize(noun, first)} {place}. "
            f"You add {second} more {pluralize(noun, second)}. How many {plural_noun} are there now?"
        )
        option_pool = [total, total + 1, total - 1, total + 2, total - 2]
        correct_index = idx % 4
        options = arrange_numeric_options(
            total,
            pool=option_pool,
            correct_index=correct_index,
        )
        explanation = f"Adding {first} and {second} makes {total} {plural_noun}."
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=options,
                correct_indices=[correct_index],
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{idx + 1}",
            )
        )

    select_sets = [
        (
            "Select each story that shows a total of 5 objects.",
            [
                "2 bears and 3 more bears",
                "4 cars and 1 more car",
                "3 shells and 2 more shells",
                "2 birds and 4 more birds",
                "1 kite and 4 more kites",
            ],
            [0, 1, 2, 4],
            "Each of these stories totals 5 objects.",
        ),
        (
            "Select each description that makes 6 items in all.",
            [
                "3 crayons and 3 more crayons",
                "4 flowers and 2 more flowers",
                "2 marbles and 2 more marbles",
                "5 apples and 1 more apple",
                "1 cup and 5 more cups",
            ],
            [0, 1, 3, 4],
            "The matching stories add to 6.",
        ),
        (
            "Select each story that adds to more than 6.",
            [
                "4 balloons and 3 more balloons",
                "2 blocks and 2 more blocks",
                "5 stickers and 2 more stickers",
                "3 frogs and 1 more frog",
                "3 marbles and 4 more marbles",
            ],
            [0, 2, 4],
            "Those stories make totals larger than 6.",
        ),
    ]

    for offset, (question, options, correct_indices, explanation) in enumerate(select_sets):
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=list(options),
                correct_indices=correct_indices,
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{len(stories) + offset + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def generate_subtraction_numeric_questions(
    test_info: TestInfo,
    *,
    pairs: Sequence[tuple[int, int]],
    select_sets: Sequence[tuple[str, Sequence[str], Sequence[int], str]],
) -> List[List[str]]:
    rows: List[List[str]] = []
    templates = [
        "What is {a} - {b}?",
        "Solve: {a} - {b} = __",
        "Take away {b} from {a}. What is left?",
    ]
    for idx, (a, b) in enumerate(pairs):
        difference = a - b
        template = templates[idx % len(templates)]
        question = template.format(a=a, b=b)
        option_pool = [difference, difference + 1, difference - 1, difference + 2, difference - 2]
        correct_index = idx % 4
        options = arrange_numeric_options(
            difference,
            pool=option_pool,
            correct_index=correct_index,
        )
        explanation = f"{a} minus {b} equals {difference}."
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=options,
                correct_indices=[correct_index],
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{idx + 1}",
            )
        )

    for offset, (question, options, correct_indices, explanation) in enumerate(select_sets):
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=list(options),
                correct_indices=correct_indices,
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{len(pairs) + offset + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def generate_subtraction_within_five_questions(test_info: TestInfo) -> List[List[str]]:
    pairs = [
        (5, 1),
        (4, 2),
        (3, 1),
        (5, 3),
        (2, 2),
        (4, 1),
        (3, 0),
        (5, 4),
        (2, 1),
        (1, 1),
        (4, 3),
        (5, 0),
    ]
    select_sets = [
        (
            "Select each equation that equals 2.",
            ["5 - 3", "4 - 2", "3 - 1", "2 - 0", "5 - 2"],
            [0, 1, 2],
            "The first three expressions equal 2.",
        ),
        (
            "Select each subtraction sentence that equals 3.",
            ["5 - 2", "4 - 1", "3 - 0", "5 - 3", "2 - 1"],
            [0, 1, 2],
            "Those differences are 3.",
        ),
        (
            "Select each difference that is zero.",
            ["2 - 2", "1 - 1", "3 - 1", "5 - 4", "4 - 4"],
            [0, 1, 4],
            "Any expression subtracting the same number leaves zero.",
        ),
    ]
    return generate_subtraction_numeric_questions(
        test_info,
        pairs=pairs,
        select_sets=select_sets,
    )


def generate_subtraction_within_ten_questions(test_info: TestInfo) -> List[List[str]]:
    pairs = [
        (10, 2),
        (9, 4),
        (8, 3),
        (7, 5),
        (6, 2),
        (9, 1),
        (8, 6),
        (10, 5),
        (7, 2),
        (6, 4),
        (9, 7),
        (10, 3),
    ]
    select_sets = [
        (
            "Select each subtraction fact that equals 6.",
            ["9 - 3", "8 - 2", "10 - 4", "7 - 1", "6 - 0"],
            [0, 1, 2, 3, 4],
            "Each listed subtraction makes 6.",
        ),
        (
            "Select each expression that equals 4.",
            ["9 - 5", "7 - 3", "8 - 4", "10 - 7", "6 - 4"],
            [0, 1, 2, 4],
            "All but 10 - 7 equal 4; 10 - 7 equals 3.",
        ),
        (
            "Select each difference greater than 2.",
            ["8 - 5", "7 - 6", "9 - 4", "10 - 8", "6 - 3"],
            [0, 2, 4],
            "Those differences are more than 2.",
        ),
    ]
    return generate_subtraction_numeric_questions(
        test_info,
        pairs=pairs,
        select_sets=select_sets,
    )


def generate_subtraction_with_objects_questions(test_info: TestInfo) -> List[List[str]]:
    stories = [
        (5, 2, "apple", "from the basket"),
        (6, 1, "car", "in the toy garage"),
        (4, 3, "cookie", "on the plate"),
        (7, 2, "shell", "by the shore"),
        (5, 1, "book", "on the shelf"),
        (8, 3, "sticker", "on the chart"),
        (6, 4, "block", "in the tower"),
        (7, 5, "balloon", "at the party"),
        (5, 2, "frog", "near the pond"),
        (6, 3, "flower", "in the vase"),
        (9, 4, "marble", "in the jar"),
        (8, 2, "pencil", "in the cup"),
    ]
    rows: List[List[str]] = []
    for idx, (start, taken, noun, place) in enumerate(stories):
        remaining = start - taken
        question = (
            f"You have {start} {pluralize(noun, start)} {place}. "
            f"You take away {taken} {pluralize(noun, taken)}. How many {pluralize(noun, remaining)} are left?"
        )
        option_pool = [remaining, remaining + 1, remaining - 1, remaining + 2, remaining - 2]
        correct_index = idx % 4
        options = arrange_numeric_options(
            remaining,
            pool=option_pool,
            correct_index=correct_index,
        )
        explanation = f"Subtracting {taken} from {start} leaves {remaining} {pluralize(noun, remaining)}."
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=options,
                correct_indices=[correct_index],
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{idx + 1}",
            )
        )

    select_sets = [
        (
            "Select each story that ends with 3 items left.",
            [
                "5 apples take away 2",
                "6 cars take away 3",
                "4 cookies take away 1",
                "7 shells take away 4",
                "8 stickers take away 5",
            ],
            [0, 1, 3],
            "Those subtraction stories leave 3 items.",
        ),
        (
            "Select each description that leaves 2 items.",
            [
                "5 books take away 3",
                "6 flowers take away 4",
                "7 balloons take away 6",
                "4 frogs take away 2",
                "3 cars take away 1",
            ],
            [0, 1, 2, 3],
            "These stories all end with 2 items remaining.",
        ),
        (
            "Select each story that leaves more than 4 items.",
            [
                "9 marbles take away 4",
                "6 pencils take away 2",
                "5 cookies take away 2",
                "7 balloons take away 5",
                "8 stickers take away 3",
            ],
            [0, 1, 4],
            "Those stories leave more than 4 items after subtracting.",
        ),
    ]

    for offset, (question, options, correct_indices, explanation) in enumerate(select_sets):
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=list(options),
                correct_indices=correct_indices,
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{len(stories) + offset + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def generate_big_vs_small_questions(test_info: TestInfo) -> List[List[str]]:
    mc_prompts = [
        (
            "Which object is bigger? An elephant or a mouse?",
            ["Elephant", "Mouse", "They are the same", "Not sure"],
            0,
            "Elephants are much bigger than mice.",
        ),
        (
            "Which item is smaller? A pencil or a school bus?",
            ["Pencil", "School bus", "They are equal", "Both are big"],
            0,
            "A pencil is small compared with a school bus.",
        ),
        (
            "Which fruit is bigger? A watermelon or a grape?",
            ["Watermelon", "Grape", "Both the same", "Not enough information"],
            0,
            "Watermelons are larger than grapes.",
        ),
        (
            "Which toy is smaller? A teddy bear or a toy car?",
            ["Toy car", "Teddy bear", "They match", "Both tiny"],
            0,
            "Toy cars are usually smaller than teddy bears.",
        ),
        (
            "Which animal is smaller? A kitten or a lion?",
            ["Kitten", "Lion", "Same size", "They switch"],
            0,
            "Kittens are smaller than lions.",
        ),
        (
            "Which object is bigger? A house or a chair?",
            ["House", "Chair", "They are equal", "Not sure"],
            0,
            "Houses are much bigger than chairs.",
        ),
        (
            "Which item is smaller? A marble or a basketball?",
            ["Marble", "Basketball", "Same size", "Need to measure"],
            0,
            "Marbles are smaller than basketballs.",
        ),
        (
            "Which object is bigger? A tree or a flower pot?",
            ["Tree", "Flower pot", "They match", "Both tiny"],
            0,
            "Trees are bigger than flower pots.",
        ),
        (
            "Which pet is smaller? A hamster or a dog?",
            ["Hamster", "Dog", "Same size", "Both large"],
            0,
            "Hamsters are smaller than most dogs.",
        ),
        (
            "Which object is bigger? A refrigerator or a spoon?",
            ["Refrigerator", "Spoon", "Equal", "Need more data"],
            0,
            "A refrigerator is much bigger than a spoon.",
        ),
        (
            "Which item is smaller? A paperclip or a book?",
            ["Paperclip", "Book", "Same", "Not sure"],
            0,
            "A paperclip is smaller than a book.",
        ),
        (
            "Which animal is bigger? A whale or a dolphin?",
            ["Whale", "Dolphin", "They are equal", "Both small"],
            0,
            "Whales are bigger than dolphins.",
        ),
    ]

    rows = build_mc_rows(test_info, mc_prompts)

    select_sets = [
        (
            "Select each object that is small.",
            ["Feather", "House", "Pebble", "Mountain", "Paperclip"],
            {0, 2, 4},
            "Feather, pebble, and paperclip are small objects.",
        ),
        (
            "Select each thing that is big.",
            ["School bus", "Ant", "Tree", "Elephant", "Pencil"],
            {0, 2, 3},
            "School buses, trees, and elephants are big.",
        ),
        (
            "Select each pair where the first item is bigger than the second.",
            ["Whale and fish", "Mouse and cat", "Book and bookmark", "Planet and moon", "Cup and table"],
            {0, 2, 3},
            "In those pairs the first item is larger than the second.",
        ),
    ]

    for offset, (question, options, correct, explanation) in enumerate(select_sets):
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=list(options),
                correct_indices=sorted(correct),
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{12 + offset + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def generate_tall_vs_short_questions(test_info: TestInfo) -> List[List[str]]:
    mc_prompts = [
        (
            "Which is taller? A giraffe or a rabbit?",
            ["Giraffe", "Rabbit", "Same height", "Not sure"],
            0,
            "Giraffes are taller than rabbits.",
        ),
        (
            "Which building is shorter? A house or a skyscraper?",
            ["House", "Skyscraper", "They match", "Need more information"],
            0,
            "A house is shorter than a skyscraper.",
        ),
        (
            "Which tree is taller? One that reaches the roof or one that reaches your knee?",
            ["Tree reaching the roof", "Tree reaching your knee", "Equal", "Not sure"],
            0,
            "A tree that reaches the roof is taller.",
        ),
        (
            "Which person is shorter? A grown-up or a preschooler?",
            ["Preschooler", "Grown-up", "Same", "It changes"],
            0,
            "Preschoolers are shorter than grown-ups.",
        ),
        (
            "Which tower of blocks is taller? One with eight blocks or one with three blocks?",
            ["Eight-block tower", "Three-block tower", "Same", "Cannot tell"],
            0,
            "Eight blocks stacked make a taller tower.",
        ),
        (
            "Which plant is shorter? A sunflower or a small potted cactus?",
            ["Small potted cactus", "Sunflower", "They tie", "Need to measure"],
            0,
            "A small cactus is shorter than a sunflower.",
        ),
        (
            "Which object is taller? A ladder or a step stool?",
            ["Ladder", "Step stool", "Same height", "Unsure"],
            0,
            "Ladders are taller than step stools.",
        ),
        (
            "Which candle is shorter? The candle that just started burning or the candle that has melted halfway?",
            ["Candle melted halfway", "Candle that just started", "They match", "Not sure"],
            0,
            "The melted candle is shorter.",
        ),
        (
            "Which mountain is taller? One that touches the clouds or one that is a hill?",
            ["Mountain touching the clouds", "Hill", "Same", "Need to climb"],
            0,
            "A mountain touching the clouds is taller than a hill.",
        ),
        (
            "Which book stack is shorter? A stack of two books or a stack of five books?",
            ["Stack of two", "Stack of five", "Equal", "Need to weigh"],
            0,
            "Two books stacked is shorter than five.",
        ),
        (
            "Which tree is shorter? A young tree or a tall oak that has grown for years?",
            ["Young tree", "Tall oak", "Same", "Depends on season"],
            0,
            "A young tree is shorter than a tall oak.",
        ),
        (
            "Which child is taller? One standing on tiptoes or one sitting down?",
            ["Standing on tiptoes", "Sitting down", "Same", "Not sure"],
            0,
            "Standing on tiptoes makes the child taller.",
        ),
    ]

    rows = build_mc_rows(test_info, mc_prompts)

    select_sets = [
        (
            "Select each object that is tall.",
            ["Skyscraper", "Pencil", "Giraffe", "Chair", "Mountain"],
            {0, 2, 4},
            "Skyscraper, giraffe, and mountain are tall examples.",
        ),
        (
            "Select each object that is short.",
            ["Step stool", "Tree", "Cupcake", "Ladder", "Baby"],
            {0, 2, 4},
            "Step stool, cupcake, and baby are short compared with others.",
        ),
        (
            "Select each pair where the first item is shorter.",
            ["Cat and giraffe", "Tall oak and seedling", "Skateboard and bike", "Child and adult", "Cup and pitcher"],
            {0, 3, 4},
            "In those pairs, the first item is shorter than the second.",
        ),
    ]

    for offset, (question, options, correct, explanation) in enumerate(select_sets):
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=list(options),
                correct_indices=sorted(correct),
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{12 + offset + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def generate_heavy_vs_light_questions(test_info: TestInfo) -> List[List[str]]:
    mc_prompts = [
        (
            "Which object is heavier? A bowling ball or a feather?",
            ["Bowling ball", "Feather", "Same weight", "Not sure"],
            0,
            "Bowling balls are heavier than feathers.",
        ),
        (
            "Which item is lighter? A pillow or a rock?",
            ["Pillow", "Rock", "Equal", "Need scale"],
            0,
            "A pillow is lighter than a rock.",
        ),
        (
            "Which is heavier? A backpack full of books or an empty backpack?",
            ["Backpack with books", "Empty backpack", "They match", "Not sure"],
            0,
            "A backpack with books weighs more.",
        ),
        (
            "Which fruit is lighter? A bunch of grapes or a pumpkin?",
            ["Bunch of grapes", "Pumpkin", "Same", "Need to check"],
            0,
            "Grapes weigh less than a pumpkin.",
        ),
        (
            "Which object is heavier? A metal key or a sheet of paper?",
            ["Metal key", "Sheet of paper", "Equal", "Cannot tell"],
            0,
            "Metal keys are heavier than paper.",
        ),
        (
            "Which animal is lighter? A kitten or a cow?",
            ["Kitten", "Cow", "Same", "Depends on the day"],
            0,
            "Kittens weigh less than cows.",
        ),
        (
            "Which object is heavier? A bucket of water or an empty bucket?",
            ["Bucket of water", "Empty bucket", "They weigh the same", "Not sure"],
            0,
            "Water adds weight, so the bucket of water is heavier.",
        ),
        (
            "Which toy is lighter? A wooden train or a balloon?",
            ["Balloon", "Wooden train", "Same", "Need a scale"],
            0,
            "Balloons are lighter than wooden trains.",
        ),
        (
            "Which tool is heavier? A hammer or a pencil?",
            ["Hammer", "Pencil", "Equal", "Not sure"],
            0,
            "Hammers weigh more than pencils.",
        ),
        (
            "Which package is lighter? One marked 1 pound or one marked 5 pounds?",
            ["1-pound package", "5-pound package", "Same", "Need to open"],
            0,
            "One pound is lighter than five pounds.",
        ),
        (
            "Which item is heavier? A stack of books or a single book?",
            ["Stack of books", "Single book", "Equal", "Need to count"],
            0,
            "A stack weighs more than one book.",
        ),
        (
            "Which food is lighter? A slice of bread or a loaf of bread?",
            ["Slice of bread", "Loaf of bread", "Same", "Not sure"],
            0,
            "A slice is lighter than a whole loaf.",
        ),
    ]

    rows = build_mc_rows(test_info, mc_prompts)

    select_sets = [
        (
            "Select each object that is heavy.",
            ["Bowling ball", "Feather", "Rock", "Balloon", "Truck"],
            {0, 2, 4},
            "Bowling ball, rock, and truck are heavy items.",
        ),
        (
            "Select each item that is light.",
            ["Feather", "Brick", "Paperclip", "Watermelon", "Leaf"],
            {0, 2, 4},
            "Feather, paperclip, and leaf are light.",
        ),
        (
            "Select each pair where the first item is lighter than the second.",
            ["Balloon and baseball", "Train and toy car", "Feather and rock", "Loaf and slice", "Cupcake and cake"],
            {0, 2, 4},
            "In those pairs the first item weighs less than the second.",
        ),
    ]

    for offset, (question, options, correct, explanation) in enumerate(select_sets):
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=list(options),
                correct_indices=sorted(correct),
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{12 + offset + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def generate_longer_vs_shorter_questions(test_info: TestInfo) -> List[List[str]]:
    mc_prompts = [
        (
            "Which object is longer? A jump rope or a pencil?",
            ["Jump rope", "Pencil", "Same length", "Not sure"],
            0,
            "Jump ropes are longer than pencils.",
        ),
        (
            "Which line is shorter? A line that measures 3 inches or a line that measures 8 inches?",
            ["3-inch line", "8-inch line", "Equal", "Need a ruler"],
            0,
            "Three inches is shorter than eight inches.",
        ),
        (
            "Which river is longer? One that flows for 10 miles or one that flows for 2 miles?",
            ["River that flows 10 miles", "River that flows 2 miles", "Same", "Need more data"],
            0,
            "A river flowing 10 miles is longer.",
        ),
        (
            "Which pencil is shorter? One that was just sharpened or one that has been used all year?",
            ["Pencil used all year", "Just sharpened pencil", "Same", "It changes"],
            0,
            "A pencil used all year is shorter.",
        ),
        (
            "Which object is longer? A scarf or a mitten?",
            ["Scarf", "Mitten", "Equal", "Need to feel"],
            0,
            "Scarves are longer than mittens.",
        ),
        (
            "Which path is shorter? A path with 5 steps or a path with 12 steps?",
            ["Path with 5 steps", "Path with 12 steps", "Same", "Need to walk"],
            0,
            "Fewer steps means a shorter path.",
        ),
        (
            "Which snake is longer? One measuring 6 feet or one measuring 3 feet?",
            ["6-foot snake", "3-foot snake", "Same", "Need to measure"],
            0,
            "Six feet is longer than three feet.",
        ),
        (
            "Which ribbon is shorter? One labeled 2 yards or one labeled 4 yards?",
            ["2-yard ribbon", "4-yard ribbon", "Same", "Not sure"],
            0,
            "Two yards is shorter than four yards.",
        ),
        (
            "Which road is longer? One with five blocks or one with one block?",
            ["Road with five blocks", "Road with one block", "Same", "Need to drive"],
            0,
            "Five blocks is longer than one block.",
        ),
        (
            "Which piece of string is shorter? A piece cut to 4 inches or a piece cut to 9 inches?",
            ["4-inch string", "9-inch string", "Equal", "Need scissors"],
            0,
            "Four inches is shorter than nine inches.",
        ),
        (
            "Which book is longer? One with 50 pages or one with 20 pages?",
            ["50-page book", "20-page book", "Same", "Need to read"],
            0,
            "A 50-page book is longer than a 20-page book.",
        ),
        (
            "Which train is shorter? A train with 3 cars or a train with 10 cars?",
            ["Train with 3 cars", "Train with 10 cars", "Same", "Need to count"],
            0,
            "Three cars make a shorter train.",
        ),
    ]

    rows = build_mc_rows(test_info, mc_prompts)

    select_sets = [
        (
            "Select each object that is long.",
            ["Jump rope", "Marble", "Garden hose", "Crayon", "Train"],
            {0, 2, 4},
            "Jump rope, garden hose, and train are long objects.",
        ),
        (
            "Select each item that is short.",
            ["Pencil", "Scarf", "Paperclip", "Snake", "Thumb"],
            {0, 2, 4},
            "Pencil, paperclip, and thumb are short items.",
        ),
        (
            "Select each pair where the first item is longer than the second.",
            ["Scarf and mitten", "Cup and straw", "Train and car", "Book and chapter", "River and creek"],
            {0, 2, 4},
            "In those pairs the first item is longer than the second.",
        ),
    ]

    for offset, (question, options, correct, explanation) in enumerate(select_sets):
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=list(options),
                correct_indices=sorted(correct),
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{12 + offset + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def generate_time_of_day_questions(test_info: TestInfo) -> List[List[str]]:
    mc_prompts = [
        (
            "When do you usually eat breakfast?",
            ["Morning", "Afternoon", "Night", "Midnight"],
            0,
            "Breakfast happens in the morning.",
        ),
        (
            "When is the sun highest in the sky?",
            ["Afternoon", "Morning", "Night", "Early midnight"],
            0,
            "The sun is highest during the afternoon.",
        ),
        (
            "When do stars shine the brightest in the sky?",
            ["Night", "Morning", "Afternoon", "Lunch time"],
            0,
            "Stars appear brightest at night.",
        ),
        (
            "When do you get ready for bed?",
            ["Night", "Afternoon", "Morning", "Lunch"],
            0,
            "Bedtime happens at night.",
        ),
        (
            "When do you usually go to school?",
            ["Morning", "Night", "Late midnight", "Dawn"],
            0,
            "School starts in the morning.",
        ),
        (
            "When might you play outside after school?",
            ["Afternoon", "Night", "Midnight", "Early morning"],
            0,
            "After school playtime is in the afternoon.",
        ),
        (
            "When do you eat dinner?",
            ["Night", "Morning", "Afternoon", "Sunrise"],
            0,
            "Dinner is usually at night.",
        ),
        (
            "When is it dark outside and you use a flashlight?",
            ["Night", "Afternoon", "Morning", "Noon"],
            0,
            "We need flashlights at night when it's dark.",
        ),
        (
            "When do you see the school bus pick up students?",
            ["Morning", "Late night", "Midnight", "Evening"],
            0,
            "The school bus comes in the morning.",
        ),
        (
            "When do you see sunsets?",
            ["Night", "Morning", "Afternoon", "Midnight"],
            0,
            "Sunsets happen in the evening and lead into night.",
        ),
        (
            "When would you likely see the moon?",
            ["Night", "Morning", "Afternoon", "Noon"],
            0,
            "The moon is easiest to see at night.",
        ),
        (
            "When do you brush your teeth before school?",
            ["Morning", "Afternoon", "Night", "Midnight"],
            0,
            "Brushing before school happens in the morning.",
        ),
    ]

    rows = build_mc_rows(test_info, mc_prompts)

    select_sets = [
        (
            "Select each activity that happens in the morning.",
            [
                "Eat breakfast",
                "Go to sleep",
                "Brush teeth before school",
                "Watch stars",
                "Pack lunch",
            ],
            {0, 2, 4},
            "Eating breakfast, brushing before school, and packing lunch happen in the morning.",
        ),
        (
            "Select each activity that happens at night.",
            [
                "Go to bed",
                "See the moon",
                "Eat lunch",
                "Turn on a flashlight outside",
                "Ride the school bus",
            ],
            {0, 1, 3},
            "Bedtime, moon watching, and using a flashlight happen at night.",
        ),
        (
            "Select each activity that fits the afternoon.",
            [
                "Play after school",
                "Eat dinner",
                "Do homework",
                "Brush teeth for bed",
                "Watch sunset",
            ],
            {0, 2, 4},
            "Playing after school, doing homework, and watching sunsets fit afternoon or evening.",
        ),
    ]

    for offset, (question, options, correct, explanation) in enumerate(select_sets):
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=list(options),
                correct_indices=sorted(correct),
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{12 + offset + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def generate_days_of_week_questions(test_info: TestInfo) -> List[List[str]]:
    mc_prompts = [
        (
            "What day comes after Monday?",
            ["Tuesday", "Sunday", "Saturday", "Friday"],
            0,
            "Tuesday follows Monday.",
        ),
        (
            "What day comes before Friday?",
            ["Thursday", "Wednesday", "Saturday", "Sunday"],
            0,
            "Thursday is right before Friday.",
        ),
        (
            "What day starts the school week?",
            ["Monday", "Saturday", "Sunday", "Friday"],
            0,
            "School usually begins on Monday.",
        ),
        (
            "What day is part of the weekend?",
            ["Saturday", "Wednesday", "Thursday", "Monday"],
            0,
            "Saturday is on the weekend.",
        ),
        (
            "Which day comes after Sunday?",
            ["Monday", "Tuesday", "Saturday", "Friday"],
            0,
            "After Sunday the week returns to Monday.",
        ),
        (
            "What day comes before Tuesday?",
            ["Monday", "Wednesday", "Friday", "Sunday"],
            0,
            "Monday comes before Tuesday.",
        ),
        (
            "What day do many families rest or go to church?",
            ["Sunday", "Thursday", "Tuesday", "Friday"],
            0,
            "Sunday is often a rest day.",
        ),
        (
            "What day comes two days after Wednesday?",
            ["Friday", "Thursday", "Saturday", "Monday"],
            0,
            "Two days after Wednesday is Friday.",
        ),
        (
            "What day is right in the middle of the school week?",
            ["Wednesday", "Monday", "Friday", "Sunday"],
            0,
            "Wednesday is in the middle of the week.",
        ),
        (
            "Which day comes before the weekend?",
            ["Friday", "Sunday", "Monday", "Tuesday"],
            0,
            "Friday comes right before the weekend.",
        ),
        (
            "Which day is the last day of the weekend?",
            ["Sunday", "Saturday", "Friday", "Monday"],
            0,
            "Sunday is the last day of the weekend.",
        ),
        (
            "What day comes after Thursday?",
            ["Friday", "Wednesday", "Tuesday", "Monday"],
            0,
            "Friday follows Thursday.",
        ),
    ]

    rows = build_mc_rows(test_info, mc_prompts)

    select_sets = [
        (
            "Select each day that is part of the weekend.",
            ["Saturday", "Sunday", "Monday", "Tuesday", "Friday"],
            {0, 1},
            "Saturday and Sunday make the weekend.",
        ),
        (
            "Select each day that comes before Thursday.",
            ["Monday", "Tuesday", "Wednesday", "Friday", "Sunday"],
            {0, 1, 2, 4},
            "Days earlier in the week than Thursday include Sunday through Wednesday.",
        ),
        (
            "Select each pair where the second day comes right after the first.",
            ["Monday -> Tuesday", "Wednesday -> Friday", "Thursday -> Friday", "Saturday -> Sunday", "Sunday -> Monday"],
            {0, 2, 3, 4},
            "Those pairs show days that follow each other in order.",
        ),
    ]

    for offset, (question, options, correct, explanation) in enumerate(select_sets):
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=list(options),
                correct_indices=sorted(correct),
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{12 + offset + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def generate_reading_clock_questions(test_info: TestInfo) -> List[List[str]]:
    mc_prompts = [
        (
            "The hour hand points to 3 and the minute hand points to 12. What time is it?",
            ["3:00", "12:30", "6:00", "9:00"],
            0,
            "When the minute hand is on 12 it is o'clock; with the hour hand at 3 it is 3:00.",
        ),
        (
            "The hour hand is on 7 and the minute hand is on 12. What time does the clock show?",
            ["7:00", "12:00", "5:00", "2:00"],
            0,
            "Hour hand on 7 with minute hand on 12 is 7:00.",
        ),
        (
            "The hour hand is between 9 and 10, but closer to 9, and the minute hand is on 12. What time is it?",
            ["9:00", "10:00", "8:00", "11:00"],
            0,
            "Minute hand on 12 means o'clock and the hour hand near 9 shows 9:00.",
        ),
        (
            "The hour hand is on 6 and the minute hand points to 12. What time is it?",
            ["6:00", "12:00", "3:00", "9:00"],
            0,
            "That clock reads 6:00.",
        ),
        (
            "The hour hand is on 12 and the minute hand is on 12. What time is it?",
            ["12:00", "6:00", "3:00", "9:00"],
            0,
            "Both hands at 12 show 12:00.",
        ),
        (
            "The hour hand is on 1 and the minute hand is on 12. What time is it?",
            ["1:00", "11:00", "5:00", "7:00"],
            0,
            "Hour hand at 1 means it is 1:00.",
        ),
        (
            "The hour hand is on 4 and the minute hand is on 12. What time does the clock show?",
            ["4:00", "2:00", "8:00", "10:00"],
            0,
            "Hands show 4:00.",
        ),
        (
            "The hour hand is on 8 and the minute hand is on 12. What time is it?",
            ["8:00", "5:00", "2:00", "11:00"],
            0,
            "It is 8:00.",
        ),
        (
            "The hour hand is on 10 with the minute hand on 12. What time is shown?",
            ["10:00", "2:00", "7:00", "11:00"],
            0,
            "10:00 is shown.",
        ),
        (
            "The hour hand is on 5 and the minute hand points to 12. What time is it?",
            ["5:00", "3:00", "7:00", "1:00"],
            0,
            "Hands show 5:00.",
        ),
        (
            "The hour hand sits on 2 and the minute hand is on 12. What time is it?",
            ["2:00", "4:00", "6:00", "8:00"],
            0,
            "It is 2:00.",
        ),
        (
            "The hour hand is on 11 and the minute hand points to 12. What time does the clock show?",
            ["11:00", "1:00", "9:00", "7:00"],
            0,
            "Hands at 11 and 12 show 11:00.",
        ),
    ]

    rows = build_mc_rows(test_info, mc_prompts)

    select_sets = [
        (
            "Select each description that shows 7:00.",
            [
                "Hour hand on 7, minute hand on 12",
                "Hour hand on 12, minute hand on 7",
                "Hour hand on 7, minute hand on 1",
                "Hour hand between 7 and 8, minute hand on 12",
                "Hour hand on 5, minute hand on 12",
            ],
            {0, 3},
            "At 7:00 the hour hand is at 7 and minute hand at 12.",
        ),
        (
            "Select each clock that would read 3:00.",
            [
                "Hour hand on 3, minute hand on 12",
                "Hour hand on 3, minute hand on 6",
                "Hour hand between 2 and 3, minute hand on 12",
                "Hour hand on 9, minute hand on 12",
                "Hour hand on 3, minute hand on 12 and chimes ringing",
            ],
            {0, 2, 4},
            "Any clock with the minute hand on 12 and hour hand at 3 shows 3:00.",
        ),
        (
            "Select each time that means the minute hand points to 12.",
            ["6:00", "4:30", "9:00", "2:00", "5:30"],
            {0, 2, 3},
            "O'clock times like 6:00, 9:00, and 2:00 have the minute hand at 12.",
        ),
    ]

    for offset, (question, options, correct, explanation) in enumerate(select_sets):
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=list(options),
                correct_indices=sorted(correct),
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{12 + offset + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def generate_recognizing_coins_questions(test_info: TestInfo) -> List[List[str]]:
    mc_prompts = [
        (
            "Which coin is worth 1 cent?",
            ["Penny", "Nickel", "Dime", "Quarter"],
            0,
            "A penny is worth one cent.",
        ),
        (
            "Which coin is worth 5 cents?",
            ["Nickel", "Penny", "Dime", "Quarter"],
            0,
            "A nickel is worth five cents.",
        ),
        (
            "Which coin is worth 10 cents?",
            ["Dime", "Penny", "Nickel", "Quarter"],
            0,
            "A dime is worth ten cents.",
        ),
        (
            "Which coin is worth 25 cents?",
            ["Quarter", "Penny", "Dime", "Nickel"],
            0,
            "A quarter is worth twenty-five cents.",
        ),
        (
            "Which coin is the smallest in size?",
            ["Dime", "Penny", "Quarter", "Nickel"],
            0,
            "The dime is the smallest coin.",
        ),
        (
            "Which coin is the largest in size?",
            ["Quarter", "Penny", "Nickel", "Dime"],
            0,
            "The quarter is the largest coin listed.",
        ),
        (
            "Which coin has George Washington on the front?",
            ["Quarter", "Penny", "Nickel", "Dime"],
            0,
            "Washington appears on the quarter.",
        ),
        (
            "Which coin has Abraham Lincoln on the front?",
            ["Penny", "Nickel", "Dime", "Quarter"],
            0,
            "Lincoln is on the penny.",
        ),
        (
            "Which coin has smooth edges and is worth ten cents?",
            ["Dime", "Quarter", "Nickel", "Penny"],
            0,
            "Dimes often have smooth edges and equal ten cents.",
        ),
        (
            "Which coin shows Thomas Jefferson on the front?",
            ["Nickel", "Penny", "Quarter", "Dime"],
            0,
            "Jefferson is on the nickel.",
        ),
        (
            "Which coin has an eagle on the back and equals 25 cents?",
            ["Quarter", "Penny", "Dime", "Nickel"],
            0,
            "The quarter often shows an eagle and equals 25 cents.",
        ),
        (
            "Which coin is silver-colored and worth more than a nickel but less than a quarter?",
            ["Dime", "Penny", "Quarter", "Dollar"],
            0,
            "A dime is silver and worth 10 cents.",
        ),
    ]

    rows = build_mc_rows(test_info, mc_prompts)

    select_sets = [
        (
            "Select each coin worth more than five cents.",
            ["Penny", "Nickel", "Dime", "Quarter", "Half dollar"],
            {2, 3, 4},
            "Dimes, quarters, and half dollars are worth more than five cents.",
        ),
        (
            "Select each coin that is copper-colored.",
            ["Penny", "Nickel", "Dime", "Quarter", "Dollar coin"],
            {0},
            "Only the penny listed is copper-colored.",
        ),
        (
            "Select each set of coins that adds up to 10 cents.",
            ["Penny + Nickel + Nickel", "Dime", "Quarter", "Nickel + Nickel", "Penny + Penny + Nickel"],
            {1, 3},
            "A dime alone equals 10 cents, and two nickels equal 10 cents.",
        ),
    ]

    for offset, (question, options, correct, explanation) in enumerate(select_sets):
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=list(options),
                correct_indices=sorted(correct),
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{12 + offset + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def generate_money_purpose_questions(test_info: TestInfo) -> List[List[str]]:
    mc_prompts = [
        (
            "What do people use money for?",
            ["To buy things", "To eat", "To sleep", "To sing"],
            0,
            "Money is used to buy things.",
        ),
        (
            "If a toy costs 3 dollars, what do you need to get it?",
            ["Money", "Stickers", "Crayons", "Snacks"],
            0,
            "You need money to buy the toy.",
        ),
        (
            "What do you hand to the cashier when you want to buy a book?",
            ["Money", "Homework", "Tickets", "Notes"],
            0,
            "We hand the cashier money to buy items.",
        ),
        (
            "What happens when you spend money?",
            ["You get something you wanted", "You lose your shoes", "You go to bed", "You eat lunch"],
            0,
            "Spending money lets you get something.",
        ),
        (
            "If you save your coins in a jar, what can you do later?",
            ["Buy something later", "Lose the jar", "Forget numbers", "Eat the coins"],
            0,
            "Saving coins lets you buy something later.",
        ),
        (
            "Which is an example of using money wisely?",
            ["Paying for a book you want", "Throwing coins away", "Eating a dollar", "Coloring a coin"],
            0,
            "Buying a book uses money wisely.",
        ),
        (
            "Where might you spend money?",
            ["Store", "Playground slide", "Backyard", "Bus seat"],
            0,
            "You spend money at a store.",
        ),
        (
            "What do you give to a vending machine to get a snack?",
            ["Money", "Homework", "A hug", "A pencil"],
            0,
            "Vending machines take money.",
        ),
        (
            "Why do people work at jobs?",
            ["To earn money", "To collect crayons", "To take naps", "To fly"],
            0,
            "People work to earn money.",
        ),
        (
            "If you have no money, what should you do before buying a toy?",
            ["Save up or ask a grown-up", "Take it anyway", "Hide it", "Throw it"],
            0,
            "You need to save or ask before buying.",
        ),
        (
            "What do you call coins and bills together?",
            ["Money", "Snacks", "Toys", "Chores"],
            0,
            "Coins and bills are money.",
        ),
        (
            "If something costs 2 dollars and you hand the cashier 5 dollars, what should you get back?",
            ["Change", "Another toy", "Homework", "Shoes"],
            0,
            "You receive change when you pay more than the cost.",
        ),
    ]

    rows = build_mc_rows(test_info, mc_prompts)

    select_sets = [
        (
            "Select each example of spending money.",
            [
                "Buying lunch",
                "Playing tag",
                "Purchasing a book",
                "Saving coins in a piggy bank",
                "Paying for a bus ride",
            ],
            {0, 2, 4},
            "Buying lunch, a book, or a bus ride uses money.",
        ),
        (
            "Select each way to earn money.",
            [
                "Doing chores",
                "Sleeping late",
                "Helping in a store",
                "Watching TV",
                "Walking dogs",
            ],
            {0, 2, 4},
            "Doing chores, helping, and walking dogs can earn money.",
        ),
        (
            "Select each good idea for saving money.",
            [
                "Keep coins in a piggy bank",
                "Spend all your money right away",
                "Put dollar bills in a safe place",
                "Lose your wallet",
                "Save coins in a jar",
            ],
            {0, 2, 4},
            "Keeping money safe helps you save.",
        ),
    ]

    for offset, (question, options, correct, explanation) in enumerate(select_sets):
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=list(options),
                correct_indices=sorted(correct),
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{12 + offset + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def generate_sorting_favorite_fruits_questions(test_info: TestInfo) -> List[List[str]]:
    scenarios = [
        (4, 2, 3),
        (5, 5, 1),
        (2, 6, 4),
        (3, 1, 5),
        (6, 3, 3),
        (2, 2, 7),
        (5, 4, 4),
        (1, 5, 2),
        (4, 6, 2),
        (3, 3, 3),
        (7, 2, 1),
        (2, 5, 5),
    ]
    mc_prompts: List[tuple[str, List[str], int, str]] = []
    for idx, (apples, bananas, oranges) in enumerate(scenarios):
        if idx % 3 == 0:
            question = (
                f"In a class survey, {apples} chose apples, {bananas} chose bananas, and {oranges} chose oranges. Which fruit was most popular?"
            )
            counts = {"Apples": apples, "Bananas": bananas, "Oranges": oranges}
            max_fruit = max(counts, key=counts.get)
            options = ["Apples", "Bananas", "Oranges", "They tied"]
            if len({v for v in counts.values()}) < 3 and list(counts.values()).count(max(counts.values())) > 1:
                correct_index = 3
                explanation = "Two fruits tied for the highest count."
            else:
                correct_index = options.index(max_fruit)
                explanation = f"{max_fruit} had the largest number of votes."
        elif idx % 3 == 1:
            question = (
                f"During snack time, {apples} kids picked apples, {bananas} picked bananas, and {oranges} picked oranges. How many children chose bananas?"
            )
            options = [str(bananas), str(apples), str(oranges), str(apples + oranges)]
            correct_index = 0
            explanation = f"The survey says {bananas} chose bananas."
        else:
            total = apples + bananas + oranges
            question = (
                f"A chart shows {apples} apples, {bananas} bananas, and {oranges} oranges. How many more students chose apples than oranges?"
            )
            difference = apples - oranges
            options = [str(difference), str(oranges - apples), str(total), str(bananas)]
            correct_index = 0
            explanation = f"{apples} minus {oranges} equals {difference}."
        mc_prompts.append((question, options, correct_index, explanation))

    rows = build_mc_rows(test_info, mc_prompts)

    select_sets = [
        (
            "Select each statement that is true if 4 chose apples, 2 chose bananas, and 3 chose oranges.",
            [
                "Apples had the most votes",
                "Bananas had more votes than oranges",
                "Nine students were surveyed",
                "Oranges had the fewest votes",
                "Bananas and oranges tied",
            ],
            {0, 2, 3},
            "Apples had the most, total students were 9, and oranges were the fewest.",
        ),
        (
            "Select each true statement if 5 chose apples, 5 chose bananas, and 1 chose orange.",
            [
                "Apples and bananas tied",
                "Orange was the least popular",
                "Eleven students voted",
                "Bananas had more than apples",
                "Apples had fewer than bananas",
            ],
            {0, 1, 2},
            "Apples and bananas tied, orange was least, and total votes were 11.",
        ),
        (
            "Select each conclusion true when 2 chose apples, 6 chose bananas, and 4 chose oranges.",
            [
                "Bananas were most popular",
                "Apples were least popular",
                "Ten students were counted",
                "Oranges had more than bananas",
                "Bananas had more than oranges",
            ],
            {0, 1, 2, 4},
            "Bananas won with 6, apples were least with 2, total 12, and bananas beat oranges.",
        ),
    ]

    for offset, (question, options, correct, explanation) in enumerate(select_sets):
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=list(options),
                correct_indices=sorted(correct),
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{12 + offset + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def generate_picture_graph_questions(test_info: TestInfo) -> List[List[str]]:
    mc_prompts: List[tuple[str, List[str], int, str]] = []
    graphs = [
        ("🍎🍎🍎", "🍌🍌", "🍊🍊🍊🍊"),
        ("🍎🍎", "🍌", "🍊🍊"),
        ("🍎🍎🍎🍎", "🍌🍌🍌", "🍊"),
        ("🍎", "🍌🍌🍌🍌", "🍊🍊"),
        ("🍎🍎🍎🍎🍎", "🍌🍌", "🍊🍊🍊"),
        ("🍎🍎🍎", "🍌🍌🍌", "🍊🍊🍊"),
        ("🍎🍎", "🍌🍌🍌🍌", "🍊"),
        ("🍎🍎🍎🍎", "🍌🍌🍌🍌🍌", "🍊🍊"),
        ("🍎🍎🍎🍎🍎🍎", "🍌🍌🍌", "🍊🍊🍊🍊"),
        ("🍎🍎🍎", "🍌🍌", "🍊🍊🍊🍊🍊"),
        ("🍎🍎🍎🍎🍎", "🍌🍌🍌🍌", "🍊🍊"),
        ("🍎🍎🍎🍎", "🍌🍌🍌", "🍊🍊🍊"),
    ]
    descriptions = [
        "Each picture stands for one vote.",
        "Each picture stands for one fruit.",
        "Each picture equals one student.",
        "Each picture equals one vote.",
        "Each picture stands for one vote.",
        "Each picture equals one vote.",
        "Each picture equals one vote.",
        "Each picture equals one student.",
        "Each picture equals one vote.",
        "Each picture equals one vote.",
        "Each picture equals one vote.",
        "Each picture equals one vote.",
    ]
    for idx, ((apple_icons, banana_icons, orange_icons), desc) in enumerate(zip(graphs, descriptions)):
        apples = len(apple_icons)
        bananas = len(banana_icons)
        oranges = len(orange_icons)
        if idx % 3 == 0:
            question = (
                f"A picture graph shows apples {apple_icons}, bananas {banana_icons}, and oranges {orange_icons}. {desc} Which fruit has the most votes?"
            )
            counts = {"Apples": apples, "Bananas": bananas, "Oranges": oranges}
            options = ["Apples", "Bananas", "Oranges", "They all tie"]
            top = max(counts.values())
            if list(counts.values()).count(top) > 1:
                correct_index = 3
                explanation = "More than one fruit has the highest count, so they tie."
            else:
                best = max(counts, key=counts.get)
                correct_index = options.index(best)
                explanation = f"{best} shows the most pictures."
        elif idx % 3 == 1:
            question = (
                f"The graph shows apples {apple_icons}, bananas {banana_icons}, and oranges {orange_icons}. {desc} How many bananas are shown?"
            )
            options = [str(bananas), str(apples), str(oranges), str(apples + oranges)]
            correct_index = 0
            explanation = f"There are {bananas} banana pictures."
        else:
            question = (
                f"The picture graph displays apples {apple_icons}, bananas {banana_icons}, and oranges {orange_icons}. {desc} How many more oranges than bananas are there?"
            )
            difference = oranges - bananas
            options = [str(difference), str(bananas - oranges), str(apples - bananas), str(apples + oranges)]
            correct_index = 0
            explanation = f"There are {oranges} oranges and {bananas} bananas, so the difference is {difference}."
        mc_prompts.append((question, options, correct_index, explanation))

    rows = build_mc_rows(test_info, mc_prompts)

    select_sets = [
        (
            "Select each statement true for apples 🍎🍎🍎🍎 and bananas 🍌🍌🍌.",
            [
                "Apples have one more vote than bananas",
                "Bananas have more votes",
                "Seven votes were counted",
                "Bananas have the same as apples",
                "Apples have three votes",
            ],
            {0, 2},
            "There are 4 apples and 3 bananas, total 7, so apples have one more.",
        ),
        (
            "Select each conclusion true for apples 🍎🍎, bananas 🍌🍌🍌, oranges 🍊🍊🍊🍊.",
            [
                "Oranges have the most",
                "Bananas and oranges tie",
                "Apples have the fewest",
                "Nine votes were counted",
                "Apples and bananas match",
            ],
            {0, 2, 3},
            "Oranges have 4, bananas 3, apples 2, total 9.",
        ),
        (
            "Select each picture graph rule that would show 12 oranges if each 🍊 stands for 3 oranges.",
            [
                "🍊🍊🍊🍊",
                "🍊🍊🍊",
                "🍊🍊",
                "🍊🍊🍊🍊🍊",
                "🍊",
            ],
            {0},
            "Four symbols worth 3 each total 12 oranges.",
        ),
    ]

    for offset, (question, options, correct, explanation) in enumerate(select_sets):
        rows.append(
            make_row(
                question=question,
                explanation=explanation,
                options=list(options),
                correct_indices=sorted(correct),
                test_info=test_info,
                title_item=f"{test_info.title_prefix} Q{12 + offset + 1}",
                qtype="Select All That Apply",
            )
        )

    return rows


def write_csv(path: Path, rows: List[List[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        writer.writerows(rows)


def main() -> None:
    numbers_1_5 = [1, 2, 3, 4, 5, 2, 4, 1, 3, 5, 2, 4, 1, 3, 5]
    numbers_6_10 = [6, 7, 8, 9, 10, 7, 9, 6, 8, 10, 7, 9, 6, 8, 10]
    numbers_11_20 = list(range(11, 21)) + [11, 12, 13, 14, 15]

    definitions: List[tuple[Path, TestInfo, Callable[[TestInfo], List[List[str]]]]] = []

    def add_definition(
        relative_path: str,
        chapter: str,
        subtopic: str,
        generator: Callable[[TestInfo], List[List[str]]],
    ) -> None:
        path = Path("assessments") / relative_path
        info = TestInfo(chapter=chapter, subtopic=subtopic, path=f"{chapter.split(':')[0]}/{subtopic}")
        definitions.append((path, info, generator))

    chapter1 = "Chapter 1: Numbers and Counting"
    add_definition(
        "chapter01_numbers_and_counting/counting_1_5.csv",
        chapter1,
        "Counting 1-5",
        lambda info: generate_counting_questions(
            info,
            numbers=numbers_1_5,
            objects=COUNTING_SMALL_OBJECTS,
        ),
    )
    add_definition(
        "chapter01_numbers_and_counting/counting_6_10.csv",
        chapter1,
        "Counting 6-10",
        lambda info: generate_counting_questions(
            info,
            numbers=numbers_6_10,
            objects=COUNTING_MEDIUM_OBJECTS,
        ),
    )
    add_definition(
        "chapter01_numbers_and_counting/counting_11_20.csv",
        chapter1,
        "Counting 11-20",
        lambda info: generate_counting_questions(
            info,
            numbers=numbers_11_20,
            objects=COUNTING_LARGE_OBJECTS,
            show_emoji=False,
        ),
    )
    add_definition(
        "chapter01_numbers_and_counting/comparing_numbers.csv",
        chapter1,
        "Comparing Numbers",
        generate_comparing_questions,
    )

    chapter2 = "Chapter 2: Number Recognition and Writing"
    add_definition(
        "chapter02_number_recognition_and_writing/recognizing_numbers_0_10.csv",
        chapter2,
        "Recognizing Numbers 0-10",
        lambda info: generate_number_recognition_questions(
            info,
            numbers=list(range(0, 11)) + [0, 3, 5, 7],
        ),
    )
    add_definition(
        "chapter02_number_recognition_and_writing/recognizing_numbers_11_20.csv",
        chapter2,
        "Recognizing Numbers 11-20",
        lambda info: generate_number_recognition_questions(
            info,
            numbers=list(range(11, 21)) + [11, 13, 15, 19],
        ),
    )
    add_definition(
        "chapter02_number_recognition_and_writing/writing_numbers_0_20.csv",
        chapter2,
        "Writing Numbers 0-20",
        generate_writing_numbers_questions,
    )

    chapter3 = "Chapter 3: Shapes and Geometry"
    add_definition(
        "chapter03_shapes_and_geometry/2d_shapes.csv",
        chapter3,
        "2D Shapes",
        generate_2d_shapes_questions,
    )
    add_definition(
        "chapter03_shapes_and_geometry/3d_shapes.csv",
        chapter3,
        "3D Shapes",
        generate_3d_shapes_questions,
    )
    add_definition(
        "chapter03_shapes_and_geometry/shape_sorting.csv",
        chapter3,
        "Shape Sorting",
        generate_shape_sorting_questions,
    )

    chapter4 = "Chapter 4: Patterns and Sorting"
    add_definition(
        "chapter04_patterns_and_sorting/simple_ab_patterns.csv",
        chapter4,
        "Simple AB Patterns",
        generate_ab_patterns_questions,
    )
    add_definition(
        "chapter04_patterns_and_sorting/abc_patterns.csv",
        chapter4,
        "ABC Patterns",
        generate_abc_patterns_questions,
    )
    add_definition(
        "chapter04_patterns_and_sorting/sorting_by_color_size_shape.csv",
        chapter4,
        "Sorting by Color, Size, Shape",
        generate_sorting_color_size_shape_questions,
    )

    chapter5 = "Chapter 5: Addition Basics"
    add_definition(
        "chapter05_addition_basics/adding_within_5.csv",
        chapter5,
        "Adding within 5",
        generate_addition_within_five_questions,
    )
    add_definition(
        "chapter05_addition_basics/adding_within_10.csv",
        chapter5,
        "Adding within 10",
        generate_addition_within_ten_questions,
    )
    add_definition(
        "chapter05_addition_basics/using_objects_to_add.csv",
        chapter5,
        "Using Objects to Add",
        generate_addition_with_objects_questions,
    )

    chapter6 = "Chapter 6: Subtraction Basics"
    add_definition(
        "chapter06_subtraction_basics/taking_away_within_5.csv",
        chapter6,
        "Taking Away within 5",
        generate_subtraction_within_five_questions,
    )
    add_definition(
        "chapter06_subtraction_basics/subtracting_within_10.csv",
        chapter6,
        "Subtracting within 10",
        generate_subtraction_within_ten_questions,
    )
    add_definition(
        "chapter06_subtraction_basics/using_objects_to_subtract.csv",
        chapter6,
        "Using Objects to Subtract",
        generate_subtraction_with_objects_questions,
    )

    chapter7 = "Chapter 7: Measurement and Comparison"
    add_definition(
        "chapter07_measurement_and_comparison/big_vs_small.csv",
        chapter7,
        "Big vs Small",
        generate_big_vs_small_questions,
    )
    add_definition(
        "chapter07_measurement_and_comparison/tall_vs_short.csv",
        chapter7,
        "Tall vs Short",
        generate_tall_vs_short_questions,
    )
    add_definition(
        "chapter07_measurement_and_comparison/heavy_vs_light.csv",
        chapter7,
        "Heavy vs Light",
        generate_heavy_vs_light_questions,
    )
    add_definition(
        "chapter07_measurement_and_comparison/longer_vs_shorter.csv",
        chapter7,
        "Longer vs Shorter",
        generate_longer_vs_shorter_questions,
    )

    chapter8 = "Chapter 8: Time and Daily Routines"
    add_definition(
        "chapter08_time_and_daily_routines/morning_afternoon_night.csv",
        chapter8,
        "Morning, Afternoon, Night",
        generate_time_of_day_questions,
    )
    add_definition(
        "chapter08_time_and_daily_routines/days_of_the_week.csv",
        chapter8,
        "Days of the Week",
        generate_days_of_week_questions,
    )
    add_definition(
        "chapter08_time_and_daily_routines/reading_a_clock_to_the_hour.csv",
        chapter8,
        "Reading a Clock to the Hour",
        generate_reading_clock_questions,
    )

    chapter9 = "Chapter 9: Money (Introduction)"
    add_definition(
        "chapter09_money_introduction/recognizing_coins.csv",
        chapter9,
        "Recognizing Coins",
        generate_recognizing_coins_questions,
    )
    add_definition(
        "chapter09_money_introduction/understanding_money_buys_things.csv",
        chapter9,
        "Understanding that Money Buys Things",
        generate_money_purpose_questions,
    )

    chapter10 = "Chapter 10: Data and Graphs"
    add_definition(
        "chapter10_data_and_graphs/sorting_favorite_fruits.csv",
        chapter10,
        "Sorting Favorite Fruits",
        generate_sorting_favorite_fruits_questions,
    )
    add_definition(
        "chapter10_data_and_graphs/making_a_picture_graph.csv",
        chapter10,
        "Making a Picture Graph",
        generate_picture_graph_questions,
    )

    for path, info, generator in definitions:
        rows = generator(info)
        if len(rows) != 15:
            raise ValueError(f"Expected 15 questions for {info.subtopic}, got {len(rows)}")
        write_csv(path, rows)


if __name__ == "__main__":
    main()
