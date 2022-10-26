import unidecode

class QuizBrain:

    def __init__(self, player_list):
        self.question_number = 0
        self.score = 0
        self.player_list = player_list
        self.current_player = None

    def still_has_questions(self):
        return self.question_number < len(self.player_list)

    def next_question(self):
        self.current_player = self.player_list[self.question_number]
        self.question_number += 1
        return self.current_player.career

    def check_answer(self, user_answer):
        user_answer = unidecode.unidecode(user_answer.lower())
        correct_answer = unidecode.unidecode(self.current_player.name.lower())
        if user_answer == correct_answer:
            self.score += 1
            return f"Yes! That's the correct answer. Your score is {self.score}"
        else:
            return f"No! The correct answer is {self.current_player.name}. Your score is {self.score}"