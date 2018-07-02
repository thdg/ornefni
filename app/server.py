from flask import Flask, abort, jsonify, request

from markovchain import MarkovChain

app = Flask(__name__)

name_files = [
    ("sjor", "data/usjavarornefni.txt", 3),
    ("sveit", "data/usveit.txt", 3),
    ("borg", "data/uthettbyli.txt", 3),
    ("vatn", "data/uvatnaornefni.txt", 4),
    ("land", "data/ulandornefni.txt", 4),
    ("jokull", "data/ujoklaornefni.txt", 3),
    ("kvk", "data/ukvknofn.txt", 3),
    ("kk", "data/ukknofn.txt", 3),
    ("milli", "data/umillinofn.txt", 3)
]


CHAINS = {}
for name, fname, order in name_files:
    mc = MarkovChain(order=order, analyzer="char")
    mc.fit(fname)
    CHAINS[name] = mc


NAMES = {}
for chain, fname, _ in name_files:
    NAMES[chain] = set()
    with open(fname) as f:
        for name in f.readlines():
            NAMES[chain].add(name.strip())


def is_bool(value):
    return value in ["True", "true", "1", 1, True]


@app.route('/<chain>/', defaults={"n": 10, "seed": ""})
@app.route('/<chain>/<int:n>/', defaults={"seed": ""})
@app.route('/<chain>/<int:n>/<seed>/')
def chains(chain, n, seed):
    if chain not in CHAINS:
        return abort(404)

    if n < 0 or 50 < n:
        return abort(400)

    filter_known = is_bool(request.args.get("ekkitil"))

    names = set()
    mc = CHAINS[chain]

    max_tries = 100
    for _ in range(max_tries):
        try:
            name = "".join(mc.generate(seed=seed.capitalize())[1:-1])
        except:
            return abort(400)

        if (filter_known and name not in NAMES[chain]) or not filter_known:
            names.add(name)

        if len(names) > n:
            break

    response = {"names": sorted(list(names))}
    return jsonify(response)
