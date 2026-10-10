# ai/missions.py

# 1. Create the mission-generation function
def generate_missions(environment, difficulty, biodiversity_type):

    # 2. Create the prompt
    prompt = f"""
    You are EcoPulse, an AI-powered biodiversity exploration assistant.

    Create 5 outdoor biodiversity missions.

    User context:
    - Environment: {environment}
    - Difficulty: {difficulty}
    - Biodiversity type: {biodiversity_type}

    Requirements:
    1. Generate exactly 5 missions.
    2. Make every mission different.
    3. Encourage different types of observation such as:
       appearance, behavior, interaction, habitat, comparison,
       texture, sound, or change over time.
    4. Missions must be realistic for the given environment.
    5. Missions must match the requested difficulty.
    6. Do not ask the user to touch, collect, feed, disturb,
       or harm plants or animals.
    7. Missions should be possible without special equipment.
    8. Keep each mission short and easy to understand.

    Return the missions as a JSON list of 5 strings.
    Do not include any other text.
    """

    # 3. For now, print the prompt so you can inspect it
    print(prompt)

    # 4. Temporary return value
    return []


if __name__ == "__main__":

    missions = generate_missions(
        "college campus",
        "easy",
        "general biodiversity"
    )

    print(missions)