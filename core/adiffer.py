import difflib

def show_diff(oldtext, text):
	sm= difflib.SequenceMatcher(None, oldtext, text)
	high_light(sm)

def high_light(seqm):
	green= '\033[32m'
	red = '\033[91m'
	end = '\033[0m'
	bold = '\033[1m'
	underline = '\033[4m'
	bu = bold+underline
	output= []
	for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
		if opcode == 'equal':
			output.append(seqm.a[a0:a1])
		elif opcode == 'insert':
			output.append(bu + green + seqm.b[b0:b1] + end)
		elif opcode == 'delete':
			output.append(bu + red + seqm.a[a0:a1] + end)
		elif opcode == 'replace':
			output.append(bu + green + seqm.b[b0:b1] + end)
		else:
			print("unexpected opcode")
	print(''.join(output))
