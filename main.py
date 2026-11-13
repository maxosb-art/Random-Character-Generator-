
# page flow home -> fantasy type -> character options -> background
# -> generate -> results -> final options

import random  # need this for random.choice things like (names, hair, companion, etc)
from dataclasses import dataclass  
from drafter import *  # all the drafter stuff (Page, Button, TextBox, route...)


# dataclass #1 (character)
# one Character object = one finished character
# i made this one first because State needs to use it
# every field is a str because i'm just storing text to show on the results page
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


# dataclass #2 (state)
# state is basically the website's memory
# character_history is a list of Character objects. this is the list i loop
# through later on the final options page
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


# route 1 home page
# TextBox name is "player_name" and that has to match the parameter in
# save_player_name below or drafter won't pass the value in
# state.player_name is the default text so if they come back it's still filled
@route
def index(state: State) -> Page:
    return Page(state, [
        Header("The Fantasy Character Generator"),
        "Welcome to your own fantasy world!\n",
        "Pick some options and we'll mix them with random details.\n",
        "What should we call you?",
        TextBox("player_name", state.player_name, placeholder="Enter your name"),
        "\n",
        # second thing in Button is the NAME of the route it opens (a string)
        Button("Start Creating", "save_player_name")
    ])


# route 2 save the name
# how this works: button on index -> drafter calls this route and passes the
# textbox value in as player_name
# .strip() removes extra spaces so "   " counts as empty
@route
def save_player_name(state: State, player_name: str) -> Page:
    # blank name -> use "Adventurer" so later pages don't say "Welcome, !"
    if player_name.strip() == "":
        state.player_name = "Adventurer"
    else:
        state.player_name = player_name.strip()
    # return the next page by calling that route function directly
    return fantasy_type(state)


# route 3 pick the fantasy world
# SelectBox name, list of options, default choice
# the default is state.fantasy_type so it remembers what they picked before
@route
def fantasy_type(state: State) -> Page:
    return Page(state, [
        Header("Step 1: Choose Your Fantasy World"),
        "Welcome, " + state.player_name + "!\n",
        "Classic Fantasy: discovery, magic, and adventure.\n",
        "Dark Fantasy: secrets and hard choices.\n",
        SelectBox("chosen_fantasy_type", ["Classic Fantasy", "Dark Fantasy"],
                  state.fantasy_type),
        "\n",
        Button("Continue", "save_fantasy_type"),
        Button("Return Home", "index")
    ])


# route 4 save fantasy type
# parameter name chosen_fantasy_type matches the SelectBox name above
@route
def save_fantasy_type(state: State, chosen_fantasy_type: str) -> Page:
    state.fantasy_type = chosen_fantasy_type
    return character_options(state)


# route 5: character options page
# 3 dropdowns + 1 checkbox
# each input name needs its own matching parameter in save_character_options
# chosen_gender, chosen_class, chosen_ability, wants_companion
# CheckBox name, starting value -> text next to it is just a normal string
@route
def character_options(state: State) -> Page:
    return Page(state, [
        Header("Step 2: Choose Your Character"),
        "Character gender:",
        SelectBox("chosen_gender", ["Woman", "Man", "Nonbinary"], state.gender),
        "\n",
        "Character class:",
        SelectBox("chosen_class",
                  ["Mage", "Ranger", "Healer", "Bard", "Knight", "Scholar"],
                  state.character_class),
        "\n",
        "Main ability:",
        SelectBox("chosen_ability",
                  ["Nature Magic", "Healing", "Illusion", "Elemental Magic",
                   "Ancient Knowledge", "Light Magic"],
                  state.primary_ability),
        "\n",
        CheckBox("wants_companion", state.include_companion),
        " Give my character a companion\n",
        Button("Save Character Choices", "save_character_options"),
        Button("Back to Fantasy Type", "fantasy_type")
    ])


# route 6 save character options
# dropdown values come in as strings. the checkbox comes in as True/False
# because the parameter is annotated with bool forgot this at first and it
# was giving me a string
# order of the parameters doesn't matter as long as the names match
@route
def save_character_options(state: State, chosen_gender: str, chosen_class: str,
                           chosen_ability: str, wants_companion: bool) -> Page:
    state.gender = chosen_gender
    state.character_class = chosen_class
    state.primary_ability = chosen_ability
    state.include_companion = wants_companion
    return character_background(state)


# route 7 background page
# this one has all 4 input types: TextBox, TextArea, SelectBox, CheckBox
# TextArea is like TextBox but bigger, rows=4 is how tall the box is
# the rival checkbox decides if a rival gets generated later
@route
def character_background(state: State) -> Page:
    return Page(state, [
        Header("Step 3: Build Your Character's Background"),
        "Where did your character grow up?",
        TextBox("chosen_homeland", state.homeland,
                placeholder="Example: The Silverwood Kingdom"),
        "\n",
        "Describe your character's family or early life:",
        TextArea("chosen_family_background", state.family_background, rows=4),
        "\n",
        "Family social status:",
        SelectBox("chosen_social_status",
                  ["Commoner", "Merchant Family", "Noble Family", "Outcast"],
                  state.social_status),
        "\n",
        CheckBox("wants_rival", state.has_rival),
        " Give my character a rival\n",
        Button("Save Background", "save_character_background"),
        Button("Back to Character Options", "character_options")
    ])


# route 8 save background
# saves all 4 values into state, then goes to the summary page
@route
def save_character_background(state: State, chosen_homeland: str,
                              chosen_family_background: str,
                              chosen_social_status: str,
                              wants_rival: bool) -> Page:
    # empty homeland would make the backstory sentence read weird
    # "comes from . " so i use a default place instead
    if chosen_homeland.strip() == "":
        state.homeland = "the Uncharted Lands"
    else:
        state.homeland = chosen_homeland.strip()

    # empty family background is handled later in build_character
    state.family_background = chosen_family_background.strip()
    state.social_status = chosen_social_status
    state.has_rival = wants_rival
    return generate_character(state)


# route 9 summary page before generating
# this just shows what they picked so they can go back and change stuff
# str() is needed on the bools because you can't add a bool to a string with +
@route
def generate_character(state: State) -> Page:
    return Page(state, [
        Header("Step 4: Ready to Generate"),
        "Fantasy world: " + state.fantasy_type + "\n",
        "Gender: " + state.gender + "\n",
        "Class: " + state.character_class + "\n",
        "Main ability: " + state.primary_ability + "\n",
        "Homeland: " + state.homeland + "\n",
        "Social status: " + state.social_status + "\n",
        "Companion included: " + str(state.include_companion) + "\n",
        "Rival included: " + str(state.has_rival) + "\n",
        Button("Generate My Character", "build_character"),
        Button("Edit Background", "character_background")
    ])


# route 10 build the character ,all the random stuff happens here
# plan: use the user's choices + random picks -> make a Character object ->
# save it in state -> show the results page
@route
def build_character(state: State) -> Page:
    # name 
    # pick the name list based on the gender they chose
    # the else covers nonbinary since it's the only option left
    if state.gender == "Woman":
        name = random.choice(["Elara", "Mira", "Rowan", "Lyra", "Seren"])
    elif state.gender == "Man":
        name = random.choice(["Alden", "Finn", "Cedric", "Orin", "Tarin"])
    else:
        name = random.choice(["Ash", "Sage", "River", "Ari", "Morgan"])

    # appearance pieces 
    # random.choice grabs one item out of the list
    hair = random.choice(["dark braided hair", "short silver hair",
                          "curly auburn hair", "long black hair",
                          "wavy golden hair"])
    eyes = random.choice(["green eyes", "gray eyes", "brown eyes",
                          "blue eyes", "amber eyes"])
    clothing = random.choice(["a traveling cloak", "scholar's robes",
                              "a forest-green coat", "a decorated tunic",
                              "simple clothes marked with family colors"])

    # dark fantasy gets a spooky description, anything else classic gets the
    # adventurous one. the first part of each sentence is the same, only the
    # ending changes. setting is a sentence used in the backstory later
    if state.fantasy_type == "Dark Fantasy":
        appearance = ("They have " + hair + ", " + eyes + ", and wear " +
                      clothing + ". Their look has a mysterious, weathered quality.")
        setting = "Their homeland is filled with old secrets and forgotten places."
    else:
        appearance = ("They have " + hair + ", " + eyes + ", and wear " +
                      clothing + ". Their look suggests a curious and determined traveler.")
        setting = "Their homeland is known for its colorful festivals and old legends."

    # extra ability is separate from the main ability they picked
    # it just adds a bit more detail to the backstory
    extra_ability = random.choice(["speaking with animals", "reading ancient maps",
                                   "creating clever illusions",
                                   "understanding forgotten languages",
                                   "finding hidden paths"])

    # companion 
    # only random pick if the checkbox was checked (True)
    # otherwise store a message so the results page isn't blank
    if state.include_companion:
        companion = random.choice(["a small owl named Pebble",
                                   "a clever fox named Bramble",
                                   "a tiny dragon named Cinder",
                                   "a loyal dog named Fern"])
    else:
        companion = "No companion was selected."

    # rival 
    if state.has_rival:
        rival = random.choice(["a former friend who became a competitor",
                               "a mysterious traveler with the same goal",
                               "a noble who doubts the character's abilities",
                               "a rival scholar searching for the same secret"])
    else:
        rival = "No rival was selected."

    # if they skipped the family box, fill in a default sentence
    # family_story is what gets saved 
    if state.family_background == "":
        family_story = "Their early life remains a mystery."
    else:
        family_story = state.family_background

    # backstory
    # building one long string by adding pieces together with +
    backstory = (name + " comes from " + state.homeland + ". " + family_story +
                 " " + setting + " As a " + state.character_class +
                 ", they are known for " + state.primary_ability +
                 " and for " + extra_ability + ".")

    # only mention the rival if picked
    if state.has_rival:
        backstory = backstory + " Their journey is complicated by " + rival + "."

    # make the Character object. the order here has to match the order of the
    # fields in the dataclass up top
    new_character = Character(name, state.fantasy_type, state.gender,
                              state.character_class, state.primary_ability,
                              state.homeland, family_story, state.social_status,
                              appearance, companion, rival, backstory)

    # current_character is the one shown on the results page
    # append adds it to the history list so older characters aren't lost
    state.current_character = new_character
    state.character_history.append(new_character)
    return character_results(state)


# route 11 results page
# pulls everything from state.current_character (a Character object)
# dot notation gets each field, like character.name
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
        # len() gives how many characters are in the list
        "Characters created so far: " + str(len(state.character_history)) + "\n",
        Button("Continue to Final Options", "final_options"),
        Button("Create Another Character", "new_character")
    ])


# route 12 final options
# THE LOOP (project requirement): goes through every Character in
# character_history and adds a one line summary to the page
# i build the page as a list first (content) since a for loop can't go inside
# the Page([...]) list directly. then i add the buttons at the end
@route
def final_options(state: State) -> Page:
    content = [
        Header("Final Options"),
        "You have created " + str(len(state.character_history)) + " character(s).\n",
        "Your character collection:\n"
    ]

    for character in state.character_history:
        content.append(character.name + " - " + character.character_class +
                       " (" + character.fantasy_type + ")\n")

    content.append(Button("Create Another Character", "new_character"))
    content.append(Button("Return to Home", "index"))
    return Page(state, content)


# route 13 new character
# resets the choices back to the starting defaults so the old character's
# options don't carry over. does NOT touch character_history, so the
# final options page still lists every character made so far
# (player_name also stays so they don't have to retype it)
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
    return fantasy_type(state)


# start the site this gotta be the last thing in the file
# the State(...) values are the starting values, in the same order as the
# fields in the State dataclass. current_character starts as a blank
# placeholder Character and history starts as an empty list []
# theme: there's no "dark" theme in drafter, yorha is a dark one
start_server(
    State("", "Classic Fantasy", "Woman", "Ranger", "Nature Magic", "", "",
          "Commoner", False, False,
          Character("Not generated yet", "", "", "", "", "", "", "", "", "", "", ""),
          []),
    site_title="Fantasy Character Generator",
    theme="yorha"
)


