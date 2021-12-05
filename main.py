import requests
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator, ValidationError

class NumberValidator(Validator):
    def validate(self, document):
        text = document.text

        if text and not text.isdigit():
            i = 0
            for i, c in enumerate(text):
                if not c.isdigit():
                    break

            raise ValidationError(message='Please enter a number.', cursor_position=i)

API_KEY = "2d6aaed040df2785a5129a3c7c097c10"

baseurl = "http://data.fixer.io/api/{}?access_key=" + API_KEY

print(" > Welcome to the currency converter!")
print(" > Getting List of Available Currencies...")
r = requests.get(baseurl.format("symbols"))

choices = []

for x in r.json()["symbols"].keys():
    choices.append("{} - {}".format(x, r.json()["symbols"][x]))
    choices.append("{} - {}".format(r.json()["symbols"][x], x))

curcompleter = WordCompleter(choices)

cur_from = prompt(" > Select the currency you want to convert from: ", completer=curcompleter)

a, b = cur_from.split(" - ")

from_cur = a if len(a) == 3 else b

amt = int(prompt(" > Enter the amount you want to convert: ", validator=NumberValidator()))

choices.remove("{} - {}".format(a, b))
choices.remove("{} - {}".format(b, a))

curcompleter = WordCompleter(choices)

cur_to = prompt(" > Select the currency you want to convert to: ", completer=curcompleter)

c, d = cur_to.split(" - ")

to_cur = c if len(c) == 3 else d

print(" > Getting Latest Exchange Rates...")
r = requests.get(baseurl.format("latest")) #+ "&from={}&to={}&amount={}".format(from_cur, to_cur, amt))
# print(r.json())
rate = r.json()['rates'][from_cur]
rate2 = r.json()['rates'][to_cur]
base = amt / rate
result = base * rate2
print(" > Converting {} {} to {}...".format(amt, from_cur, to_cur))
print(" > {} {} = {} {}".format(amt, from_cur, result, to_cur))

