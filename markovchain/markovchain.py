from random import random


class MarkovChain(object):
	def __init__(self, order=1, split=" ", analyzer="word"):
		self.order = order
		self.split = split
		self.analyzer = analyzer

		self.START = "<START>"
		self.END = "<END>"

		self.states = {}

	def tokenize(self, sequence):
		if self.analyzer == "word":
			return [self.START] + sequence.split(self.split) + [self.END]
		if self.analyzer == "char":
			return [self.START] + list(sequence) + [self.END]

	def find_state(self, memory):
		state = self.states[memory[0]]
		for token in memory[1:]:
			state = state.get_state(token)
		return state

	def accumulate(self, sequence):
		order = self.order
		for i, token in enumerate(sequence):
			memory = tuple(sequence[max(i-order, 0):i])

			if memory not in self.states:
				self.states[memory] = {}
			if token not in self.states[memory]:
				self.states[memory][token] = 0

			self.states[memory][token] += 1

	def fit(self, fname, reversed=False):
		direction = -1 if reversed else 1
		with open(fname) as f:
			for line in f.readlines():
				tokens = self.tokenize(line.strip()[::direction])
				self.accumulate(tokens)

	def weighted_random_step(self, state):
		total = sum(state.values())
		r = random()
		acc = 0.0
		for key, value in state.items():
			acc += value/total
			if r < acc:
				return key

	def generate(self, seed=""):
		sequence = self.tokenize(seed)[:-1]
		while sequence[-1] != self.END:
			memory = tuple(sequence[-self.order:])
			next = self.weighted_random_step(self.states[memory])
			sequence.append(next)
		return sequence


def main():
	mc = MarkovChain(order=4, analyzer="char")
	mc.fit("vatnaornefni.txt")

	for _ in range(10):
		print("".join(mc.generate(seed="")[1:-1]))


if __name__ == "__main__":
	main()
