
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
    "Does the full article mentions either physical or psychological consequences for all involved parties?)"
    "Does the full article places the crash in a larger pattern of crashes?"
]