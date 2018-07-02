from flask import Flask, abort, jsonify

from markovchain import MarkovChain

app = Flask(__name__)

name_files = [
    ("see", "sjavarornefni.txt"),
    ("farm", "sveit.txt"),
    ("town", "thettbyli.txt"),
    ("water", "vatnaornefni.txt"),
    ("land", "landornefni.txt"),
    ("ice", "joklaornefni.txt"),
    ("kvk", "kvennmannsnofn.txt"),
    ("kk", "karlmannsnofn.txt"),
]

CHAINS = {}
for name, fname in name_files:
    mc = MarkovChain(order=4, analyzer="char")
    mc.fit(fname)
    CHAINS[name] = mc

@app.route('/<chain>/', defaults={"n": 10, "seed": ""})
@app.route('/<chain>/<int:n>/', defaults={"seed": ""})
@app.route('/<chain>/<int:n>/<seed>/')
def chains(chain, n, seed):
    if chain not in CHAINS:
        return abort(404)

    if n > 50:
        return abort(422)

    names = []
    mc = CHAINS[chain]
    for _ in range(n):
        names.append("".join(mc.generate(seed=seed)[1:-1]))

    response = {"names": names}
    return jsonify(response)


@app.route('/docs/')
def docs():
    return "docs"