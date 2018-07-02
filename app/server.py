from flask import Flask, abort, jsonify

from markovchain import MarkovChain

app = Flask(__name__)

name_files = [
    ("sjor", "data/usjavarornefni.txt", 3),
    ("sveit", "data/usveit.txt", 2),
    ("borg", "data/uthettbyli.txt", 2),
    ("vatn", "data/uvatnaornefni.txt", 4),
    ("land", "data/ulandornefni.txt", 4),
    ("jokull", "data/ujoklaornefni.txt", 2),
    ("kvk", "data/ukvknofn.txt", 3),
    ("kk", "data/ukknofn.txt", 3),
    ("milli", "data/umillinofn.txt", 3)
]

CHAINS = {}
for name, fname, order in name_files:
    mc = MarkovChain(order=order, analyzer="char")
    mc.fit(fname)
    CHAINS[name] = mc

@app.route('/<chain>/', defaults={"n": 10, "seed": ""})
@app.route('/<chain>/<int:n>/', defaults={"seed": ""})
@app.route('/<chain>/<int:n>/<seed>/')
def chains(chain, n, seed):
    if chain not in CHAINS:
        return abort(404)

    if n < 0 or 50 < n:
        return abort(400)

    names = []
    mc = CHAINS[chain]
    for _ in range(n):
        names.append("".join(mc.generate(seed=seed)[1:-1]))

    response = {"names": names}
    return jsonify(response)
