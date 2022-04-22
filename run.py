from flask import Flask, request

app = Flask(__name__)

HTML_START = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Guess The Number</title>
</head>
<body>
<h1>Think of a whole number from range {min_number} to {max_number} and 
I will try to guess it in {attempts} tries.</h1>
<form action="" method="POST">
    <input type="submit" value="OK">
</form>
</body>
</html>
"""

HTML_GAME = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Guess The Number</title>
</head>
<body>
<h1>Attempt {computer_attempt} from {attempts}</h1>
<h1>Is this number is {current_guess} ?</h1>
<form action="" method="POST">
    <input type="hidden" name="min" value={min_number}></input>
    <input type="hidden" name="max" value={max_number}></input>
    <input type="hidden" name="guess" value={guess}></input>
    <input type="hidden" name="computer_attempt" value={computer_attempt}></input>
    <input type="submit" value="too small" name="guess_action">
    <input type="submit" value="too big" name="guess_action">
    <input type="submit" value="you win" name="guess_action">
</form>
</body>
</html>
"""

HTML_FINISH = """
<!DOCTYPE html>
<html lang="en">
<body>
<h1>{score}</h1>
</body>
</html>
"""


@app.route('/', methods=["GET", "POST"])
def game():
    if request.method == "GET":
        return HTML_START.format(min_number=MIN_NUMBER, max_number=MAX_NUMBER, attempts=ATTEMPTS)
    else:
        guess = 0
        user_action = request.form.get('guess_action')
        if not user_action:
            min_num = MIN_NUMBER
            max_num = MAX_NUMBER
            computer_attempt = 1
        else:
            min_num = int(request.form.get('min'))
            max_num = int(request.form.get('max'))
            computer_attempt = int(request.form.get('computer_attempt'))
            guess = int(request.form.get('guess'))
            computer_attempt += 1
        if computer_attempt > 10:
            return HTML_FINISH.format(score="It is impossible I have lost this game!!!")
        elif user_action == "you win":
            return HTML_FINISH.format(score="I always win ha ha ha!!!")
        elif user_action == "too big":
            max_num = guess
        elif user_action == "too small":
            min_num = guess
        guess = int((max_num - min_num) / 2) + min_num
        return HTML_GAME.format(min_number=min_num, max_number=max_num, current_guess=guess,
                                computer_attempt=computer_attempt, attempts=ATTEMPTS, guess=guess)


if __name__ == '__main__':
    MIN_NUMBER = 0
    MAX_NUMBER = 1000
    ATTEMPTS = 10
    app.run(debug=True)
