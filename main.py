from flask import Flask, render_template, request
from player import Player
from quiz_brain import QuizBrain
from player_list import \
    longoria_era, \
    eyraud_era, \
    labrune_era, \
    diouf_dassier_era, \
    bouchet_era, \
    rld_era, \
    l2_era, \
    tapie_era, \
    all_players
import random

app = Flask(__name__)

players = [Player(player) for player in random.sample(all_players, 10)]
# players = [Player(player) for player in longoria_era]
# players = [Player(player) for player in eyraud_era]
# players = [Player(player) for player in labrune_era]
# players = [Player(player) for player in diouf_dassier_era]
# players = [Player(player) for player in bouchet_era]
# players = [Player(player) for player in rld_era]
# players = [Player(player) for player in l2_era]
# players = [Player(player) for player in tapie_era]
quiz = QuizBrain(players)
answered = []

class DataStore():
    question = None

data = DataStore()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["GET"])
def ask():
    try:
        question = quiz.next_question()
        data.question = question
        position = quiz.current_player.position
        pob = quiz.current_player.pob
        return render_template("ask.html", pob=pob, position=position, answered=answered, question=question.to_html(classes='table table-sm table-responsive', col_space=[0,300,0,0], index=False, justify="center"))
    except IndexError:
        return render_template("end.html", score=quiz.score)

@app.route("/check", methods=["POST"])
def check_answer():
    question = data.question
    position = quiz.current_player.position
    pob = quiz.current_player.pob
    response = quiz.check_answer(request.form["answer"])
    if "Yes!" in response:
        name_to_append = "<p class='true'>" + str(quiz.current_player.name) + "</p>"
        answered.append(name_to_append)
    else:
        name_to_append = "<p class='false'>" + str(quiz.current_player.name) + "</p>"
        answered.append(name_to_append)
    return render_template("answer.html", pob=pob, position=position, response=response, answered=answered, question=question.to_html(classes='table table-sm table-responsive', col_space=[0,300,0,0], index=False, justify="center"))

if __name__ == "__main__":
    app.run()
