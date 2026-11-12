"""
FANTASY CHARACTER GENERATOR
A beginner-friendly Drafter website for the CS1 final project.

HOW TO RUN:
1. Save this file as fantasy_character_generator.py.
2. Make sure Drafter is installed in the Python environment used by Thonny.
3. Run this file. Drafter should open the website in a browser.

The website follows the project design document:
Home -> Fantasy Type -> Character Options -> Character Background
-> Generate Character -> Character Results -> Final Options.

The code uses two dataclasses, several routes, form inputs, conditionals,
random choices, and a loop through a list of Character objects.
"""

# random lets the program choose names, appearances, companions, and story details.
import random

# dataclass is used to create simple classes that store related information.
from dataclasses import dataclass

# Drafter provides the tools used to build pages, forms, buttons, and routes.
from drafter import *


# ---------------------------------------------------------------------------
# SECOND DATACLASS: CHARACTER
# ---------------------------------------------------------------------------
# Each Character object stores all the information for one generated character.
# The State dataclass below keeps a list of these objects so the user can make
# more than one character during the same visit to the website.
@dataclass
class Character:
    name: str
    fantasy_type: str
    gender: str
    character_class: str
    primary_ability: str
    homeland: str
    family_background: str
    social_status: str
    appearance: str
    companion: str
    rival: str
    backstory: str


# ---------------------------------------------------------------------------
# FIRST DATACLASS: STATE
# ---------------------------------------------------------------------------
# State is the website's memory. Drafter passes the same State object from one
# route to the next, which lets the website remember the user's choices.
#
# character_history is especially important: it is a list of Character
# dataclass instances, as required by the project design document.
@dataclass
class State:
    player_name: str
    fantasy_type: str
    gender: str
    character_class: str
    primary_ability: str
    homeland: str
    family_background: str
    social_status: str
    include_companion: bool
    has_rival: bool
    current_character: Character
    character_history: list[Character]


# ---------------------------------------------------------------------------
# HELPER FUNCTION: make_blank_character
# ---------------------------------------------------------------------------
# This function creates an empty Character object for the website to use
# before the user has generated their first character.
#
# Drafter's State needs a value for current_character when the website starts.
# This placeholder is replaced with a completed Character after generation.
def make_blank_character() -> Character:
    return Character(
        name="Not generated yet",
        fantasy_type="",
        gender="",
        character_class="",
        primary_ability="",
        homeland="",
        family_background="",
        social_status="",
        appearance="",
        companion="",
        rival="",
        backstory=""
    )


# ---------------------------------------------------------------------------
# ROUTE 1: HOME PAGE
# ---------------------------------------------------------------------------
# The route named index is the first page Drafter displays.
# The TextBox collects the user's name. Its name, "player_name", matches the
# parameter in the save_player_name route that the button opens.
@route
def index(state: State) -> Page:
    return Page(state, [
        Header("The Fantasy Character Generator"),
        "Welcome to your own fantasy world!\n",
        "Create an original fantasy character by choosing a world, ",
        "a character type, and a personal background. The generator will ",
        "combine your choices with randomly selected details.\n",
        Header("Begin Your Adventure"),
        "What should we call you?",
        TextBox("player_name", state.player_name,
                placeholder="Enter your name"),
        "\n",
        Button("Start Creating", "save_player_name"),
        "\n",
        "You can create multiple characters and review them later."
    ])


# ---------------------------------------------------------------------------
# ROUTE 2: SAVE THE PLAYER'S NAME
# ---------------------------------------------------------------------------
# This route receives the value from TextBox("player_name").
# Saving it in State means it can be displayed on later pages.
# The route then sends the user to the fantasy-type selection page.
@route
def save_player_name(state: State, player_name: str) -> Page:
    # If the user leaves the name blank, use a friendly default instead.
    if player_name.strip() == "":
        state.player_name = "Adventurer"
    else:
        state.player_name = player_name.strip()

    return fantasy_type(state)


# ---------------------------------------------------------------------------
# ROUTE 3: FANTASY TYPE PAGE
# ---------------------------------------------------------------------------
# This page asks the user to choose the overall style of their fantasy world.
# The SelectBox sends its selected value to save_fantasy_type.
@route
def fantasy_type(state: State) -> Page:
    return Page(state, [
        Header("Step 1: Choose Your Fantasy World"),
        "Welcome, " + state.player_name + "!\n",
        "What kind of fantasy story should your character belong to?\n",
        "Classic Fantasy: A world of discovery, magic, and adventure.\n",
        "Dark Fantasy: A mysterious world with difficult choices and secrets.\n",
        SelectBox(
            "chosen_fantasy_type",
            ["Classic Fantasy", "Dark Fantasy"],
            state.fantasy_type
        ),
        "\n",
        Button("Continue", "save_fantasy_type"),
        "\n",
        Button("Return Home", "index")
    ])


# ---------------------------------------------------------------------------
# ROUTE 4: SAVE THE FANTASY TYPE
# ---------------------------------------------------------------------------
# The selected dropdown value arrives as chosen_fantasy_type.
# This route stores it in State and then opens the character-options page.
@route
def save_fantasy_type(state: State, chosen_fantasy_type: str) -> Page:
    state.fantasy_type = chosen_fantasy_type
    return character_options(state)


# ---------------------------------------------------------------------------
# ROUTE 5: CHARACTER OPTIONS PAGE
# ---------------------------------------------------------------------------
# This page contains three SelectBoxes and one CheckBox.
# The user chooses a gender, class, and main ability, and can decide whether
# the generated character should have a companion.
#
# Every input name must match a parameter in save_character_options exactly.
@route
def character_options(state: State) -> Page:
    return Page(state, [
        Header("Step 2: Choose Your Character"),
        "Now choose the main details of your character.\n",
        "Character gender:",
        SelectBox(
            "chosen_gender",
            ["Woman", "Man", "Nonbinary"],
            state.gender
        ),
        "\n",
        "Character class:",
        SelectBox(
            "chosen_class",
            ["Mage", "Ranger", "Healer", "Bard", "Knight", "Scholar"],
            state.character_class
        ),
        "\n",
        "Main ability:",
        SelectBox(
            "chosen_ability",
            [
                "Nature Magic",
                "Healing",
                "Illusion",
                "Elemental Magic",
                "Ancient Knowledge",
                "Light Magic"
            ],
            state.primary_ability
        ),
        "\n",
        CheckBox("wants_companion", state.include_companion),
        " Give my character a companion\n",
        Button("Save Character Choices", "save_character_options"),
        "\n",
        Button("Back to Fantasy Type", "fantasy_type")
    ])


# ---------------------------------------------------------------------------
# ROUTE 6: SAVE CHARACTER OPTIONS
# ---------------------------------------------------------------------------
# This route receives the values from all four inputs on the previous page.
# The three dropdown values arrive as strings. The checkbox arrives as True
# or False because its parameter is annotated with bool.
# The choices are stored in State before moving to the background page.
@route
def save_character_options(
    state: State,
    chosen_gender: str,
    chosen_class: str,
    chosen_ability: str,
    wants_companion: bool
) -> Page:
    state.gender = chosen_gender
    state.character_class = chosen_class
    state.primary_ability = chosen_ability
    state.include_companion = wants_companion

    return character_background(state)


# ---------------------------------------------------------------------------
# ROUTE 7: CHARACTER BACKGROUND PAGE
# ---------------------------------------------------------------------------
# This page uses a TextBox, a TextArea, a SelectBox, and a CheckBox.
# The TextBox collects a homeland, while the TextArea gives the user room
# to describe the character's family history.
# The checkbox determines whether the character will have a rival.
@route
def character_background(state: State) -> Page:
    return Page(state, [
        Header("Step 3: Build Your Character's Background"),
        "Where did your character grow up?",
        TextBox(
            "chosen_homeland",
            state.homeland,
            placeholder="Example: The Silverwood Kingdom"
        ),
        "\n",
        "Describe your character's family or early life:",
        TextArea(
            "chosen_family_background",
            state.family_background,
            rows=4
        ),
        "\n",
        "What was your character's family's social status?",
        SelectBox(
            "chosen_social_status",
            ["Commoner", "Merchant Family", "Noble Family", "Outcast"],
            state.social_status
        ),
        "\n",
        CheckBox("wants_rival", state.has_rival),
        " Give my character a rival\n",
        Button("Save Background", "save_character_background"),
        "\n",
        Button("Back to Character Options", "character_options")
    ])


# ---------------------------------------------------------------------------
# ROUTE 8: SAVE CHARACTER BACKGROUND
# ---------------------------------------------------------------------------
# The input names on character_background match the parameters below.
# The route saves all four values in State. If the user leaves the homeland
# empty, a default location is used so the generated story still makes sense.
@route
def save_character_background(
    state: State,
    chosen_homeland: str,
    chosen_family_background: str,
    chosen_social_status: str,
    wants_rival: bool
) -> Page:
    if chosen_homeland.strip() == "":
        state.homeland = "the Uncharted Lands"
    else:
        state.homeland = chosen_homeland.strip()

    state.family_background = chosen_family_background.strip()
    state.social_status = chosen_social_status
    state.has_rival = wants_rival

    return generate_character(state)


# ---------------------------------------------------------------------------
# ROUTE 9: GENERATE CHARACTER PAGE
# ---------------------------------------------------------------------------
# This is a separate confirmation page. It lets the user review their choices
# before the program randomly creates the final character.
# The Generate Character button opens the build_character route.
@route
def generate_character(state: State) -> Page:
    return Page(state, [
        Header("Step 4: Ready to Generate"),
        "Here is a summary of your choices:\n",
        "Fantasy world: " + state.fantasy_type + "\n",
        "Gender: " + state.gender + "\n",
        "Class: " + state.character_class + "\n",
        "Main ability: " + state.primary_ability + "\n",
        "Homeland: " + state.homeland + "\n",
        "Social status: " + state.social_status + "\n",
        "Companion included: " + str(state.include_companion) + "\n",
        "Rival included: " + str(state.has_rival) + "\n",
        Button("Generate My Character", "build_character"),
        "\n",
        Button("Edit Background", "character_background")
    ])


# ---------------------------------------------------------------------------
# HELPER FUNCTION: create_character
# ---------------------------------------------------------------------------
# This function combines the user's saved choices with randomly selected
# details. It returns one complete Character dataclass instance.
#
# Keeping character creation in its own function makes the code easier to
# understand and allows the build_character route to stay short.
def create_character(state: State) -> Character:
    # These name lists let the program choose a name that matches the
    # gender option selected by the user.
    if state.gender == "Woman":
        possible_names = ["Elara", "Mira", "Rowan", "Lyra", "Seren"]
    elif state.gender == "Man":
        possible_names = ["Alden", "Finn", "Cedric", "Orin", "Tarin"]
    else:
        possible_names = ["Ash", "Sage", "River", "Ari", "Morgan"]

    # random.choice selects one item from the appropriate name list.
    character_name = random.choice(possible_names)

    # These lists provide possible visual details for the character.
    hair_choices = ["dark braided hair", "short silver hair",
                    "curly auburn hair", "long black hair",
                    "wavy golden hair"]
    eye_choices = ["green eyes", "gray eyes", "brown eyes",
                   "blue eyes", "amber eyes"]
    clothing_choices = ["a traveling cloak", "scholar's robes",
                        "a forest-green coat", "a decorated tunic",
                        "simple clothes marked with family colors"]

    # Choose one detail from each list to make the appearance feel different
    # each time the user generates a character.
    hair = random.choice(hair_choices)
    eyes = random.choice(eye_choices)
    clothing = random.choice(clothing_choices)

    # Conditional logic changes the description based on the fantasy type.
    # Dark Fantasy gets a more mysterious description; Classic Fantasy gets
    # a more adventurous description.
    if state.fantasy_type == "Dark Fantasy":
        appearance = (
            "They have " + hair + ", " + eyes +
            ", and wear " + clothing +
            ". Their look has a mysterious, weathered quality."
        )
        story_setting = (
            "Their homeland is filled with old secrets and forgotten places."
        )
    else:
        appearance = (
            "They have " + hair + ", " + eyes +
            ", and wear " + clothing +
            ". Their look suggests a curious and determined traveler."
        )
        story_setting = (
            "Their homeland is known for its colorful festivals and old legends."
        )

    # A second ability is randomly selected to give each character an extra
    # detail beyond the main ability selected by the user.
    extra_abilities = [
        "speaking with animals",
        "reading ancient maps",
        "creating clever illusions",
        "understanding forgotten languages",
        "finding hidden paths"
    ]
    extra_ability = random.choice(extra_abilities)

    # The companion is only selected if the user checked the companion box.
    # Otherwise the program stores a sentence explaining that there is none.
    if state.include_companion:
        companion = random.choice([
            "a small owl named Pebble",
            "a clever fox named Bramble",
            "a tiny dragon named Cinder",
            "a loyal dog named Fern"
        ])
    else:
        companion = "No companion was selected."

    # The rival is only generated if the user checked the rival box.
    if state.has_rival:
        rival = random.choice([
            "a former friend who became a competitor",
            "a mysterious traveler with the same goal",
            "a noble who doubts the character's abilities",
            "a rival scholar searching for the same secret"
        ])
    else:
        rival = "No rival was selected."

    # If the user did not write a family background, the program supplies
    # a simple default so the final story is never missing this detail.
    if state.family_background == "":
        family_story = "Their early life remains a mystery."
    else:
        family_story = state.family_background

    # Build a backstory by combining the user's choices and generated details.
    backstory = (
        character_name + " comes from " + state.homeland + ". " +
        family_story + " " +
        story_setting + " As a " + state.character_class +
        ", they are known for " + state.primary_ability +
        " and for " + extra_ability + "."
    )

    # Add an extra sentence when the user selected a rival.
    if state.has_rival:
        backstory = backstory + " Their journey is complicated by " + rival + "."

    # Create and return a Character object containing all generated details.
    return Character(
        name=character_name,
        fantasy_type=state.fantasy_type,
        gender=state.gender,
        character_class=state.character_class,
        primary_ability=state.primary_ability,
        homeland=state.homeland,
        family_background=family_story,
        social_status=state.social_status,
        appearance=appearance,
        companion=companion,
        rival=rival,
        backstory=backstory
    )


# ---------------------------------------------------------------------------
# ROUTE 10: BUILD THE CHARACTER
# ---------------------------------------------------------------------------
# This route calls create_character, stores the returned Character object as
# the current character, and adds it to the character_history list.
# Appending the object to the list allows the website to keep a record of
# every character generated during this visit.
@route
def build_character(state: State) -> Page:
    new_character = create_character(state)

    state.current_character = new_character
    state.character_history.append(new_character)

    return character_results(state)


# ---------------------------------------------------------------------------
# ROUTE 11: CHARACTER RESULTS PAGE
# ---------------------------------------------------------------------------
# This page displays the completed character.
# It reads the information from state.current_character, which is a Character
# dataclass instance created by create_character.
@route
def character_results(state: State) -> Page:
    character = state.current_character

    return Page(state, [
        Header("Your Character Has Been Created!"),
        Header(character.name),
        "Fantasy type: " + character.fantasy_type + "\n",
        "Gender: " + character.gender + "\n",
        "Class: " + character.character_class + "\n",
        "Main ability: " + character.primary_ability + "\n",
        "Homeland: " + character.homeland + "\n",
        "Family background: " + character.family_background + "\n",
        "Social status: " + character.social_status + "\n",
        Header("Appearance"),
        character.appearance + "\n",
        Header("Companion"),
        character.companion + "\n",
        Header("Rival"),
        character.rival + "\n",
        Header("Character Backstory"),
        character.backstory + "\n",
        "Characters created so far: " + str(len(state.character_history)),
        "\n",
        Button("Continue to Final Options", "final_options"),
        "\n",
        Button("Create Another Character", "new_character")
    ])


# ---------------------------------------------------------------------------
# ROUTE 12: FINAL OPTIONS PAGE
# ---------------------------------------------------------------------------
# This page gives the user the two choices shown in the original site diagram:
# create another character or return to the home page.
#
# The for loop below iterates through character_history. Each item in that
# list is a Character dataclass instance. This fulfills the requirement that
# the project use a meaningful loop over the State list of dataclass objects.
@route
def final_options(state: State) -> Page:
    page_content = [
        Header("Final Options"),
        "You have created " + str(len(state.character_history)) +
        " character(s).\n",
        "Your character collection:\n"
    ]

    # Loop through every saved Character object and add a short summary.
    for character in state.character_history:
        page_content.append(
            character.name + " - " + character.character_class +
            " (" + character.fantasy_type + ")\n"
        )

    # These buttons let the user either continue creating or return home.
    page_content.append(Button("Create Another Character", "new_character"))
    page_content.append("\n")
    page_content.append(Button("Return to Home", "index"))

    return Page(state, page_content)


# ---------------------------------------------------------------------------
# ROUTE 13: START A NEW CHARACTER
# ---------------------------------------------------------------------------
# This route clears the choices from the previous character but keeps
# character_history. That way, the user can create several characters and
# still see all of them on the Final Options page.
@route
def new_character(state: State) -> Page:
    state.fantasy_type = "Classic Fantasy"
    state.gender = "Woman"
    state.character_class = "Ranger"
    state.primary_ability = "Nature Magic"
    state.homeland = ""
    state.family_background = ""
    state.social_status = "Commoner"
    state.include_companion = False
    state.has_rival = False
    state.current_character = make_blank_character()

    # Go back to the first choice page for the next character.
    return fantasy_type(state)


# ---------------------------------------------------------------------------
# START THE WEBSITE
# ---------------------------------------------------------------------------
# This creates the initial State object and starts Drafter.
# start_server must be the last statement in the file because Drafter takes
# control of the program after this point.
start_server(
    State(
        player_name="",
        fantasy_type="Classic Fantasy",
        gender="Woman",
        character_class="Ranger",
        primary_ability="Nature Magic",
        homeland="",
        family_background="",
        social_status="Commoner",
        include_companion=False,
        has_rival=False,
        current_character=make_blank_character(),
        character_history=[]
    ),
    site_title="Fantasy Character Generator",
    # Drafter has no theme named "dark". Valid themes are: default, none, mvp,
    # sakura, simple, skeleton, 98, xp, 7, tacit, almond, brutal, daub, latex,
    # magick, pico, retro, terminal, water, yorha.
    # "yorha" is a dark theme. Other dark-looking options to try:
    # "terminal", "water", "pico".
    theme="yorha"
)

