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
    ("gata", "data/ugotunofn.txt", 4)
    ("hus", "data/uhusanofn.txt", 3)
]


CHAINS = {}
for name, fname, order in name_files:
    mc = MarkovChain(order=order, analyzer="char")
    mc.fit(fname)
    CHAINS[name] = mc
    mc = MarkovChain(order=order, analyzer="char")
    mc.fit(fname, reversed=True)
    CHAINS[name + "_r"] = mc


NAMES = {}
for chain, fname, _ in name_files:
    NAMES[chain] = set()
    with open(fname) as f:
        for name in f.readlines():
            NAMES[chain].add(name.strip())


def is_bool(value):
    return value in ["True", "true", "1", 1, True]


def clean_seed(value, reversed):
    if reversed:
        return value[::-1].lower()
    else:
        return value.capitalize()

@app.route('/<chain>/', defaults={"n": 10, "seed": ""})
@app.route('/<chain>/<int:n>/', defaults={"seed": ""})
@app.route('/<chain>/<int:n>/<seed>/')
def chains(chain, n, seed):
    if chain not in CHAINS:
        return abort(404)

    if n < 0 or 50 < n:
        return abort(400)

    filter_known = is_bool(request.args.get("ekkitil"))
    reversed = is_bool(request.args.get("aftur"))

    names = set()
    chain_name = chain + ("_r" if reversed else "")
    mc = CHAINS[chain_name]

    max_tries = 100
    direction = -1 if reversed else 1
    seed = clean_seed(seed, reversed)

    for _ in range(max_tries):
        try:
            name = "".join(mc.generate(seed=seed)[1:-1])
        except:
            continue

        if (filter_known and name not in NAMES[chain]) or not filter_known:
            names.add(name[::direction])

        if len(names) > n:
            break

    response = {"names": sorted(list(names))}
    return jsonify(response)
