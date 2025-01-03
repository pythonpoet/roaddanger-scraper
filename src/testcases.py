
roaddanger_dehumanisation_eval = """
An article passes this test if all questions below are answered 'Yes':
1) Does the headline mention all involved parties?
2) ...as humans, not transportation modes?
3) ... and the subject of the sentence is also human?
4) ... and the sentence is written in active grammar?
5) And the full article mentions specific physical and/or psychological consequences for all involved parties?
6) ... and the full article places the crash in a larger pattern of crashes?
"""
roaddanger_dehumanisation_eval_modified = """
An article's evaluation :
1) Does the headline mention all involved parties?
2) ...as humans, not transportation modes?
3) ... and the subject of the sentence is also human?
4) ... and the sentence is written in active grammar?
5) And the full article mentions specific physical and/or psychological consequences for all involved parties?
6) ... and the full article places the crash in a larger pattern of crashes?
"""

roaddanger_dehumanisation_question_list=[
    "Does the headline mention all involved parties?",
    "Does the headline refere to all involved parties as humans, not transportation modes?",
    "Is the headline  subject of the sentence also human?",
    "Is headline written in active grammar?",
    "Does the full article mentions either physical or psychological consequences for all involved parties?"
    "Does the full article places the crash in a larger pattern of crashes?"
]

deh_list=[
    "Does the text mention all involved parties?",
    "Does the text refere to all involved parties as humans, not transportation modes?",
    "Identify whether the subject of the following sentence is a human. Answer with '1' for yes or '0' for no."
    "Is the text written in active grammar?",
    "Does the article mentions either physical or psychological consequences for all involved parties?"
    "Does the article places the crash in a larger pattern of crashes?"
]
improved_prompts = {
    "prompt_all_parties": {
        "standard": [
            {
                'role': 'user',
                'content': 
                """For the following headline, determine if all parties that were involved in the accident are mentioned. Answer with '1' for yes or '0' for no.
                    Example 1: 'Two Drivers and a Pedestrian Injured in Collision at Downtown Intersection' → Explanation: All parties (two drivers and a pedestrian) are mentioned. → Answer: 1
                    Example 2: 'Driver Hospitalized After Early Morning Crash' → Explanation: Only one party (the driver) is mentioned; other potential parties are not referenced. → Answer: 0
                    Headline: Motorcyclist and Truck Driver Injured in Highway Collision
                """
            },
            {
                'role': 'assistant',
                'content': "1"  # Example response
            },
            {
                'role': 'user',
                'content': 
                """For the following headline, determine if all parties that were involved in the accident are mentioned. Answer with '1' for yes or '0' for no.
                   Headline: {Text}
                """
            },
        ],
        "explanation": [
            {
                'role': 'user',
                'content': 
                """For the following headline, determine if all parties that were involved in the accident are mentioned. Answer with a JSON object containing 'answer' (1 for yes, 0 for no) and 'explanation' (a short reason).
                    Example 1: 'Two Drivers and a Pedestrian Injured in Collision at Downtown Intersection' → {"answer": 1, "explanation": "All parties (two drivers and a pedestrian) are mentioned."}
                    Example 2: 'Driver Hospitalized After Early Morning Crash' → {"answer": 0, "explanation": "Only one party (the driver) is mentioned."}
                    Headline: Motorcyclist and Truck Driver Injured in Highway Collision
                """
            },
            {
                'role': 'assistant',
                'content': '{"answer": 1, "explanation": "All parties (motorcyclist and truck driver) are mentioned."}'  # Example response
            },
            {
                'role': 'user',
                'content': 
                """For the following headline, determine if all parties that were involved in the accident are mentioned. Answer with a JSON object containing 'answer' (1 for yes, 0 for no) and 'explanation' (a short reason).
                   Headline: {Text}
                """
            },
        ]
    },
    "prompt_human_reference": {
        "standard": [
            {
                'role': 'user',
                'content': 
                """Determine if all parties in the following headline are referred to as humans (e.g., driver, pedestrian) and not as transportation modes (e.g., car, truck). 
                Answer with '1' for yes or '0' for no.

                Examples:
                - 'Two Drivers and a Pedestrian Injured in Collision at Downtown Intersection' → Explanation: All parties (two drivers and a pedestrian) are referred to as humans. → Answer: 1
                - 'Car and Truck Collide on Highway, Causing Traffic Jam' → Explanation: The parties (car and truck) are referred to as transportation modes, not humans. → Answer: 0
                - 'Cyclist and Motorcyclist Injured in Downtown Accident' → Explanation: All parties (cyclist and motorcyclist) are referred to as humans. → Answer: 1

                Headline: Motorcyclist and Truck Driver Injured in Highway Collision
                """
            },
            {
                'role': 'assistant',
                'content': "1"  # Example response
            },
            {
                'role': 'user',
                'content': 
                """Determine if all parties in the following headline are referred to as humans (e.g., driver, pedestrian) and not as transportation modes (e.g., car, truck). 
                Answer with '1' for yes or '0' for no.

                Headline: {Text}
                """
            },
        ],

        "explanation": [
            {
                'role': 'user',
                'content': 
                """Determine if all parties in the following headline are referred to as humans (e.g., driver, pedestrian) and not as transportation modes (e.g., car, truck). 
                Provide a JSON object with:
                - 'answer': 1 for yes, 0 for no
                - 'explanation': A short reason why.

                Examples:
                - 'Two Drivers and a Pedestrian Injured in Collision at Downtown Intersection' → {"answer": 1, "explanation": "All parties (two drivers and a pedestrian) are referred to as humans."}
                - 'Car and Truck Collide on Highway, Causing Traffic Jam' → {"answer": 0, "explanation": "The parties (car and truck) are referred to as transportation modes."}
                - 'Cyclist and Motorcyclist Injured in Downtown Accident' → {"answer": 1, "explanation": "All parties (cyclist and motorcyclist) are referred to as humans."}

                Headline: Motorcyclist and Truck Driver Injured in Highway Collision
                """
            },
            {
                'role': 'assistant',
                'content': '{"answer": 1, "explanation": "All parties (motorcyclist and truck driver) are referred to as humans."}'  # Example response
            },
            {
                'role': 'user',
                'content': 
                """Determine if all parties in the following headline are referred to as humans (e.g., driver, pedestrian) and not as transportation modes (e.g., car, truck). 
                Provide a JSON object with:
                - 'answer': 1 for yes, 0 for no
                - 'explanation': A short reason why.

                Headline: {Text}
                """
            },
        ]

    },
    "prompt_subject": {
        "standard": [
            {
                'role': 'user',
                'content': 
                """Determine if the grammatical subject in the following headline refers to a human. 
                Answer with '1' for yes or '0' for no.

                Examples:
                1. 'John is a teacher.' → Subject: John → Answer: 1
                2. 'The car is fast.' → Subject: The car → Answer: 0
                3. 'Cyclist Injured in Collision' → Subject: Cyclist → Answer: 1
                4. 'Car Hits Pedestrian on Crosswalk' → Subject: Car → Answer: 0
                5. 'Authorities Investigate Crash Site' → Subject: Authorities → Answer: 1

                Headline: Two Drivers Injured in Collision at Downtown Intersection
                """
            },
            {
                'role': 'assistant',
                'content': "1"  # Example response
            },
            {
                'role': 'user',
                'content': 
                """Determine if the grammatical subject in the following headline refers to a human. 
                Answer with '1' for yes or '0' for no.

                Headline: {Text}
                """
            },
        ],
        "explanation": [
            {
                'role': 'user',
                'content': 
                """Determine if the grammatical subject in the following headline refers to a human. 
                Provide a JSON object with:
                - 'answer': 1 for yes, 0 for no
                - 'explanation': A short reason why.

                Examples:
                1. 'John is a teacher.' → {"answer": 1, "explanation": "The subject (John) is a human."}
                2. 'The car is fast.' → {"answer": 0, "explanation": "The subject (the car) is not a human."}
                3. 'Cyclist Injured in Collision' → {"answer": 1, "explanation": "The subject (cyclist) is a human."}
                4. 'Authorities Investigate Crash Site' → {"answer": 1, "explanation": "The subject (authorities) refers to a group of humans."}
                5. 'Car Hits Pedestrian on Crosswalk' → {"answer": 0, "explanation": "The subject (car) is not a human."}

                Headline: Two Drivers Injured in Collision at Downtown Intersection
                """
            },
            {
                'role': 'assistant',
                'content': '{"answer": 1, "explanation": "The subject (two drivers) is human."}'  # Example response
            },
            {
                'role': 'user',
                'content': 
                """Determine if the grammatical subject in the following headline refers to a human. 
                Provide a JSON object with:
                - 'answer': 1 for yes, 0 for no
                - 'explanation': A short reason why.

                Headline: {Text}
                """
            },
        ]

    },
    "prompt_active_grammar": {
        "standard": [
            {
                'role': 'user',
                'content': 
                """Determine if the following headline is written in active grammar. 
                Answer with '1' for yes (active voice) or '0' for no (passive voice).

                Examples:
                1. 'Company Launches New Product Line' → Explanation: Active voice (subject performs the action). → Answer: 1
                2. 'New Product Line Launched by Company' → Explanation: Passive voice (subject receives the action). → Answer: 0
                3. 'President Signs New Law' → Explanation: Active voice (subject performs the action). → Answer: 1
                4. 'New Law Signed by President' → Explanation: Passive voice (subject receives the action). → Answer: 0

                Headline: City Council Approves New Budget Plan
                """
            },
            {
                'role': 'assistant',
                'content': "1"  # Example response
            },
            {
                'role': 'user',
                'content': 
                """Determine if the following headline is written in active grammar. 
                Answer with '1' for yes (active voice) or '0' for no (passive voice).

                Headline: {Text}
                """
            },
        ],
       "explanation": [
            {
                'role': 'user',
                'content': 
                """Determine if the following headline is written in active grammar. 
                Provide a JSON object with:
                - 'answer': 1 for yes (active voice), 0 for no (passive voice)
                - 'explanation': A short reason explaining the decision.

                Examples:
                1. 'Company Launches New Product Line' → {"answer": 1, "explanation": "Active voice (subject performs the action)."}
                2. 'New Product Line Launched by Company' → {"answer": 0, "explanation": "Passive voice (subject receives the action)."}
                3. 'Cyclist Hits Pedestrian in Park' → {"answer": 1, "explanation": "Active voice (subject performs the action)."}
                4. 'Pedestrian Hit by Cyclist in Park' → {"answer": 0, "explanation": "Passive voice (subject receives the action)."}

                Headline: City Council Approves New Budget Plan
                """
            },
            {
                'role': 'assistant',
                'content': '{"answer": 1, "explanation": "Active voice (subject performs the action)."}'  # Example response
            },
            {
                'role': 'user',
                'content': 
                """Determine if the following headline is written in active grammar. 
                Provide a JSON object with:
                - 'answer': 1 for yes (active voice), 0 for no (passive voice)
                - 'explanation': A short reason explaining the decision.

                Headline: {Text}
                """
            },
        ]

    },
    "prompt_consequences_mentioned": {
        "standard": [
            {
                'role': 'user',
                'content': 
                """For the following article, determine if it mentions either physical (e.g., injuries, wounds) or psychological (e.g., shock, anxiety) consequences for all involved parties. Answer with '1' for yes or '0' for no.

                Examples:
                1. 'Two drivers sustained minor injuries, and a pedestrian was treated for shock after the collision.' 
                → Explanation: Physical and psychological consequences are mentioned for all parties (two drivers and a pedestrian). → Answer: 1
                2. 'The accident caused significant damage to both vehicles.'
                → Explanation: No physical or psychological consequences are mentioned for the involved parties. → Answer: 0
                3. 'The cyclist suffered a broken leg, but no information is provided about the driver.'
                → Explanation: Consequences are not mentioned for all involved parties (only the cyclist is mentioned). → Answer: 0

                Article: The cyclist suffered a broken leg, and the driver was treated for anxiety following the crash.
                """
            },
            {
                'role': 'assistant',
                'content': "1"  # Example response
            },
            {
                'role': 'user',
                'content': 
                """For the following article, determine if it mentions either physical or psychological consequences for all involved parties. Answer with '1' for yes or '0' for no.

                Article: {Text}
                """
            },
        ],
        "explanation": [
            {
                'role': 'user',
                'content': 
                """For the following article, determine if it mentions either physical (e.g., injuries, wounds) or psychological (e.g., shock, anxiety) consequences for all involved parties. Provide a JSON object with:
                - 'answer': 1 for yes, 0 for no
                - 'explanation': A short reason explaining the decision.

                Examples:
                1. 'Two drivers sustained minor injuries, and a pedestrian was treated for shock after the collision.' 
                → {"answer": 1, "explanation": "Physical and psychological consequences are mentioned for all parties."}
                2. 'The accident caused significant damage to both vehicles.' 
                → {"answer": 0, "explanation": "No consequences are mentioned for the involved parties."}
                3. 'The cyclist suffered a broken leg, but no information is provided about the driver.' 
                → {"answer": 0, "explanation": "Consequences are only mentioned for the cyclist, not all parties."}

                Article: The cyclist suffered a broken leg, and the driver was treated for anxiety following the crash.
                """
            },
            {
                'role': 'assistant',
                'content': '{"answer": 1, "explanation": "Physical and psychological consequences are mentioned for all parties."}'  # Example response
            },
            {
                'role': 'user',
                'content': 
                """For the following article, determine if it mentions either physical or psychological consequences for all involved parties. Provide a JSON object with:
                - 'answer': 1 for yes, 0 for no
                - 'explanation': A short reason explaining the decision.

                Article: {Text}
                """
            },
        ]

    },
    "prompt_larger_pattern": {
        "standard": [
            {
                'role': 'user',
                'content': 
                """For the following article, determine if it places the crash in a larger pattern of crashes. Answer with '1' for yes or '0' for no.

                Examples:
                1. 'This is the third accident at this intersection in the past month, raising concerns about road safety.' 
                → Explanation: The crash is placed in a larger pattern of crashes at the same intersection. → Answer: 1
                2. 'The driver lost control of the vehicle, resulting in a collision with a tree.' 
                → Explanation: The crash is described as an isolated incident with no reference to a larger pattern. → Answer: 0
                3. 'Reports indicate several crashes have occurred in the vicinity, but this one was due to a mechanical failure.' 
                → Explanation: The crash is mentioned in the context of other crashes but is described as unrelated. → Answer: 0

                Article: This crash marks the fifth incident on this highway in the last two months, prompting calls for improved signage.
                """
            },
            {
                'role': 'assistant',
                'content': "1"  # Example response
            },
            {
                'role': 'user',
                'content': 
                """For the following article, determine if it places the crash in a larger pattern of crashes. Answer with '1' for yes or '0' for no.

                Article: {Text}
                """
            },
        ],
        "explanation": [
            {
                'role': 'user',
                'content': 
                """For the following article, determine if it places the crash in a larger pattern of crashes. Provide a JSON object with:
                - 'answer': 1 for yes, 0 for no
                - 'explanation': A short reason explaining the decision.

                Examples:
                1. 'This is the third accident at this intersection in the past month, raising concerns about road safety.' 
                → {"answer": 1, "explanation": "The crash is placed in a larger pattern of crashes at the same location."}
                2. 'The driver lost control of the vehicle, resulting in a collision with a tree.' 
                → {"answer": 0, "explanation": "The crash is described as an isolated incident with no reference to a larger pattern."}
                3. 'Reports indicate several crashes have occurred in the vicinity, but this one was due to a mechanical failure.' 
                → {"answer": 0, "explanation": "The crash is mentioned in the context of other crashes but is described as unrelated."}

                Article: This crash marks the fifth incident on this highway in the last two months, prompting calls for improved signage.
                """
            },
            {
                'role': 'assistant',
                'content': '{"answer": 1, "explanation": "The crash is placed in a larger pattern of crashes."}'  # Example response
            },
            {
                'role': 'user',
                'content': 
                """For the following article, determine if it places the crash in a larger pattern of crashes. Provide a JSON object with:
                - 'answer': 1 for yes, 0 for no
                - 'explanation': A short reason explaining the decision.

                Article: {Text}
                """
            },
        ]

    }
}
proficiency_criteria = """
1. **Grammar and Syntax**: 
   - Native: Perfect understanding and application of grammar rules.
   - Advanced: Strong grasp of grammar with rare errors.
   - Intermediate: Good understanding of basic grammar.
   - Basic: Frequent grammatical errors.
   - Limited: Minimal understanding of grammar.

2. **Vocabulary and Terminology**: 
   - Native: Extensive vocabulary, including idioms and slang.
   - Advanced: Broad vocabulary with occasional gaps.
   - Intermediate: Adequate vocabulary for everyday communication.
   - Basic: Limited vocabulary.
   - Limited: Very restricted vocabulary.

3. **Fluency and Coherence**: 
   - Native: Natural, fluent, and coherent text.
   - Advanced: Highly fluent with minor inconsistencies.
   - Intermediate: Generally coherent but may have awkward phrasing.
   - Basic: Struggles to maintain coherence.
   - Limited: Disjointed or nonsensical text.

4. **Cultural and Contextual Understanding**: 
   - Native: Fully understands cultural nuances and context.
   - Advanced: Strong cultural understanding but may miss subtle nuances.
   - Intermediate: Basic cultural awareness.
   - Basic: Limited cultural understanding.
   - Limited: No meaningful cultural understanding.

5. **Task-Specific Capabilities**: 
   - Native: Excels in all linguistic tasks.
   - Advanced: Performs well in most tasks.
   - Intermediate: Handles basic tasks.
   - Basic: Can perform very simple tasks.
   - Limited: Unable to perform meaningful tasks.
"""
# Proficiency scale description
proficiency_scale = """
- "Native" (fluent like a native speaker), 
- "Advanced" (excellent understanding and response capability), 
- "Intermediate" (good understanding but limited response capability), 
- "Basic" (can understand and respond to simple phrases), 
- "Limited" (minimal understanding or response capability).
"""
output_v1= """{{
  "language_proficiency": {{
    "Language1": {{
      "Grammar and Syntax": "ProficiencyLevel",
      "Vocabulary and Terminology": "ProficiencyLevel",
      "Fluency and Coherence": "ProficiencyLevel",
      "Cultural and Contextual Understanding": "ProficiencyLevel",
      "Task-Specific Capabilities": "ProficiencyLevel"
    }},
    "Language2": {{
      "Grammar and Syntax": "ProficiencyLevel",
      "Vocabulary and Terminology": "ProficiencyLevel",
      "Fluency and Coherence": "ProficiencyLevel",
      "Cultural and Contextual Understanding": "ProficiencyLevel",
      "Task-Specific Capabilities": "ProficiencyLevel"
    }},
    ...
  }}
}}"""
output_v2="""{{
  "language_proficiency": {{
    "Language1": "ProficiencyLevel",
    "Language2": "ProficiencyLevel",
    ...
  }}
}}"""