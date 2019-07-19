import os
import random

from flask import Flask, render_template, request

import tarot


app = Flask(__name__)
symboliek = tarot.Symboliek()
deck = tarot.Deck(symboliek)


@app.route("/")
def index():
    return render_template("index.jinja2")


@app.route("/overview", defaults={"order": "klassiek", "num": False})
@app.route("/overview/num", defaults={"order": "klassiek", "num": True})
@app.route(
    '/overview/<any("klassiek", "waite", "hersteld"):order>', defaults={"num": False}
)
@app.route(
    '/overview/num/<any("klassiek", "waite", "hersteld"):order>', defaults={"num": True}
)
def overview(order, num):
    template = "overview"

    suits = dict(
        klassiek=["staven", "pentakels", "zwaarden", "kelken"],
        waite=["staven", "kelken", "zwaarden", "pentakels"],
    )
    cards = [deck.cards[n] for n in deck.order[order]]
    if num:
        template += "_num"
    elif order == "hersteld":
        template += "_hersteld"
    return render_template(
        template + ".jinja2",
        cards=dict(
            groot=cards[0:22],
            staven=cards[22:36],
            pentakels=cards[36:50],
            zwaarden=cards[50:64],
            kelken=cards[64:78],
        ),
        symbols=symboliek,
        order=order,
        suits=suits[order],
        num=num,
    )


@app.route("/card/<int:nr>")
def card(nr):
    hidden = request.args.get("hidden", default=1, type=int)
    return render_template(
        "info.jinja2",
        card=deck.cards[nr],
        symbols=symboliek,
        hidden="hidden" if hidden else "",
    )


@app.route("/cards/", defaults=dict(turned=False, cards=None, nr=3))
@app.route("/cards/<int:nr>", defaults=dict(turned=False, cards=None))
def cards(nr, turned=False, flipped=False, cards=None):
    hidden = request.args.get("hidden", default=1, type=int)
    cards = cards or deck.pick(nr)
    return render_template(
        "cards.jinja2",
        cards=cards,
        nr=nr,
        deck=deck,
        symbols=symboliek,
        turned=turned,
        hidden=hidden,
        flipped=flipped,
    )


@app.route("/turned/", defaults=dict(nr=3))
@app.route("/turned/<int:nr>")
def turned(nr):
    return cards(nr, True)


@app.route("/perma/<nrs>")
def perma(nrs):
    nrs = [int(nr) for nr in nrs.split("-")]
    return cards(len(nrs), flipped=True, cards=[deck.cards[nr] for nr in nrs])


@app.route("/related/", defaults=dict(nr=3))
@app.route("/related/<int:nr>")
def related(nr):
    return render_template(
        "related.jinja2", card=deck.cards[nr], symbols=symboliek, deck=deck
    )


@app.route("/symbols")
def symbols():
    return render_template("symbols.jinja2", symbols=symboliek, deck=deck)


@app.route("/quiz")
def question():
    q_src = random.choice([deck, symboliek])
    q = q_src.question()
    return render_template(
        "question.jinja2", question=q, url="%s?hidden=0" % q_src.url(q.answer)
    )


@app.route("/study")
def study():
    return render_template("study.jinja2", deck=deck, symbols=symboliek)


@app.route("/env")
def env():
    return "\n".join(
        ["<li>%s: %s</li>" % (key, val) for key, val in os.environ.items()]
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
