import copy, math, random

class State:
	grid = []
	words = []

# a. Assign an empty mxn grid and the full list of words
#    {word[0],..., word[k-1]} to initialState.
def initializeState(nrows, ncols, words=[]):
	state = State()
	state.grid = [['' for y in range(ncols)] for x in range(nrows)]
	state.words = words
	return state

# b. Write a function goal(state) which returns true if state.words equals
#    the empty list.
def goal(state):
	return state.words == []

# c. Write a function applyRule(rule,state) which returns the value of
#    applying a rule to a given state. This does not change the value of state.
#
#    We copy the state, put the word in its location according to rule, remove
#    the word from the list, and return the new state.
def applyRule(rule,state):
	state = copy.deepcopy(state)
	i,row,col,dh,dv = rule
	for j in range(len(state.words[i])):
		state.grid[row][col] = state.words[i][j]
		row += dv
		col += dh
	state.words.remove(state.words[i])
	return state

# d. Write a function precondition(rule,state) which returns True if the given
#    rule may be applied to state, that is, the preconditions are satisfied.
#    For instance, given the value of initialState, the precondition for rule 
#    (7,0,0,1,0) is satisfied (and True is returned) because the word fits in
#    the grid and there are no other words in the grid that conflict with it. 
#    Note, however that False is returned for the rule (7,0,8,1,0), because 
#    the word does not fit in the grid when starting at position [0,8] and 
#    filling forward in the positive direction. Likewise, suppose "heuristic" 
#    has been placed successfully with the first rule and the new state is 
#    state2. Then if rule2 is (0,9,10,-1,-1) , precondition(rule2,state2) 
#    returns True because the final letter 'e' overlaps with the letter 'e' in 
#    position [0,1]. However, the rule (0,9,11,-1,-1) would not satisfy the 
#    preconditions for this state because it does not overlap properly with 
#    existing words in the grid.
#
#    For each character in the word, we test the row and col boundary 
#    conditions, then test the cell for conflict conditions.
#
#    That is, we check that we each character falls in the grid, and that the 
#    cell with which the character overlaps is either empty or already holds 
#    the same character.
#
#    We return False as soon as one of the conditions is violated, and return 
#    True if the conditions hold for all characters in the word.
def precondition(rule,state):
	i,row,col,dh,dv = rule
	for j in range(len(state.words[i])):
		if row >= len(state.grid) or col >= len(state.grid[row]) or (state.grid[row][col] != '' and state.grid[row][col] != state.words[i][j]):
			return False
		else:
			row += dv
			col += dh
	return True

# e. Write a function generateRules(state) which calls precondition and
#    returns a list of all possible rules that may be applied to the current 
#    state, where rules have the form described above. This should be a list 
#    of all possible words, starting positions and directions which satisfy 
#    the preconditions for the given state.
def generateRules(state):
	rules = []

	#[['','','']
	# ['','','']
	# ['','','']
	# ['','','']]

	for i in range(len(state.words)):
		word = state.words[i]

		# forward rows
		for row in range(len(state.grid)):
			for col in range(len(state.grid[row])):
				# columns forward
				if row + (len(word)-1) <= (len(state.grid)-1):
					r = (i,row,col,0,1)
					if precondition(r,state):
						rules.append(r)

				# columns backwards
				if row - (len(word)-1) >= 0:
					r = (i,row,col,0,-1)
					if precondition(r,state):
						rules.append(r)

				# rows forward
				if col + (len(word)-1) <= (len(state.grid[row])-1):
					r = (i,row,col,1,0)
					if precondition(r,state):
						rules.append(r)

				# rows backwards
				if col - (len(word)-1) >= 0:
					r = (i,row,col,-1,0)
					if precondition(r,state):
						rules.append(r)

				# diagonals forward
				if row + (len(word)-1) <= (len(state.grid)-1) and col + (len(word)-1) <= (len(state.grid[row])-1):
					r = (i,row,col,1,1)
					if precondition(r,state):
						rules.append(r)

				# diagonals backward
				if row - (len(word)-1) >= 0 and col - (len(word)-1) >= 0:
					r = (i,row,col,-1,-1)
					if precondition(r,state):
						rules.append(r)

	return rules

# f. Write a function describeState(state), which shows the partially filled 
#    in grid and lists words still remaining to be placed in the grid.
def describeState(state,printit=True):
	#print state.grid
	msg = ""
	for r in state.grid:
		for c in r:
			if c == '':
				msg += '_ '
			else:
				msg += c+' '
		msg += '\n'
	msg += str(state.words)
	if printit:
		print msg
	return msg
	
# g. Write a function describeRule(rule), which explains the meaning of the 
#    given rule, e.g., 
#
#    Place the word "admissible" in the grid starting at position (9,10) and 
#    proceeding in the direction [-1,-1].
# XXX had to add 'state' parameter to get the word
def describeRule(rule,state,printit=True):
	msg = "Place the word \"%s\" in the grid starting at position (%d,%d) and proceeding in the direction [%d,%d]"% (state.words[rule[0]], rule[1], rule[2], rule[3], rule[4])
	if printit:
		print msg
	return msg

# h. Test these primitives by writing a routine flailWildly(state), which 
#    repeatedly tests goal(state) and if a goal has not been reached, 
#    determines all applicable rules for the current state, chooses one 
#    randomly and applies it. At each step, describe the current state, 
#    describe each applicable rule, and describe which rule has been chosen.
def flailWildly(state):
	random.seed(1271202865)

	rules = []
	while goal(state) != True:
		rules = generateRules(state)

		if not len(rules):
			print "FAILURE! No applicable rules found for state:"
			describeState(state)
			return

		n = random.randrange(0,len(rules))
		rule = rules[n]
		
		print "The current state is as follows:"
		describeState(state)
		
		#print "Applicable rules are as follows."
		for r in rules:
			False#describeRule(r,state)

		print "We chose the following rule:"
		describeRule(rule,state)
		
		state = applyRule(rule,state)

	if goal(state):
		print "SUCCESS!"
		describeState(state)
		
# In order to find a solution to the Word Morph problem, it is necessary to
# implement a control strategy. Use the backtracking algorithm described
# above. Use your describeState and describeRule functions to report which
# rules are tried and which states are reached. You may find it beneficial to
# print occasional blank or dotted lines, to enhance readability. Output
# should also include the solution path and a report on the number of calls to
# backTrack, and number of failures before finding the solution.
calls_to_backtrack = states_not_goal = 0
def backTrack(stateList,depthBound=100,printit=False):
	global calls_to_backtrack, states_not_goal
	calls_to_backtrack = calls_to_backtrack+1
	
	state = stateList[0]
	if stateList.count(state) > 1: return 'FAILED-1'
	if deadEnd(state): return 'FAILED-2'
	if goal(state):
		if printit:
			print "\n\nReached a goal state:"
		return []
	else:
		states_not_goal = states_not_goal+1
	if len(stateList) > depthBound: return 'FAILED-3'
	
	ruleSet = generateRules(state) 
	if ruleSet == []: return 'FAILED-4'   
	
	for r in ruleSet:
		newState = applyRule(r,state)
		stateList.insert(0,newState)
		path = backTrack(stateList,depthBound,printit)
		
		if printit:
			print describeState(newState,False),"\n"
			print describeRule(r,state,False),"\n"
		
		if type(path) == list:
			path.append(r) 
			return path
		if printit and type(path) == str and path.startswith('FAILED'):
			print path
	
	return 'FAILED-5'

def deadEnd(state):
	return False

# Unit Testing

def testInitializeState():
	state = initializeState(3,4,['dog','ball'])
	if len(state.grid) != 3:
		print 'error in testInitializeState-1'
	else:
		print 'success in testInitializeState-1'

	error = False
	for row in range(len(state.grid)):
		if len(state.grid[row]) != 4:
			error = True

	if error:
		print 'error in testInitializeState-2'
	else:
		print 'success in testInitializeState-2'
	
	if len(state.words) != 2:
		print 'error in testInitializeState-3'
	else:
		print 'success in testInitializeState-3'
		
	if state.words[0] != 'dog' or state.words[1] != 'ball':
		print 'error in testInitializeState-4'
	else:
		print 'success in testInitializeState-4'		

def testGoal():
	state = State()
	state.words = ['dog','ball']
	errorTestGoal(state,False,1)
	state.words = []
	errorTestGoal(state,True,2)
	state.words = None
	errorTestGoal(state,False,3)

def errorTestGoal(state,expected,num):
	if goal(state) != expected:
		print 'error in testGoal-%d' % num
	else:
		print 'success in testGoal-%d' % num

def testPrecondition():
	state = State()
	state.grid = [['','',''],['','',''],['','',''],['','','']]
	state.words = ['dog','ball']
	
	# test boundary conditions
	errorTestPrecondition((0,0,0,1,0),state,True,1)
	errorTestPrecondition((1,0,0,1,0),state,False,2)
	errorTestPrecondition((1,0,0,0,1),state,True,3)
	
	# test conflict conditions
	state.grid[0] = ['b','o','y']
	errorTestPrecondition((1,0,0,0,1),state,True,4)
	state.grid[3] = ['m','a','n']
	errorTestPrecondition((1,0,0,0,1),state,False,5)

def errorTestPrecondition(rule,state,expected,num):
	if precondition(rule,state) != expected:
		print 'error in testPrecondition-%d' % num
	else:
		print 'success in testPrecondition-%d' % num		

def testGenerateRules():
	state = initializeState(4,3,  	#[['','','']
	['dog','ball'])                 # ['','','']
	                                # ['','','']
	                                # ['','','']]
	expected_rules = [
	(0,0,0,1,0),(0,1,0,1,0),(0,2,0,1,0),(0,3,0,1,0), # dog in any row-forwards
	(0,0,0,0,1),(0,0,1,0,1),(0,0,2,0,1), # dog in any col-forwards (starting row-0)
	(0,1,0,0,1),(0,1,1,0,1),(0,1,2,0,1), # dog in any col-forwards (starting row-1)
	(0,0,0,1,1),(0,1,0,1,1), # dog in the diagonals-forwards
	(0,0,2,-1,0),(0,1,2,-1,0),(0,2,2,-1,0),(0,3,2,-1,0), # dog in any row-backwards
	(0,2,0,0,-1),(0,2,1,0,-1),(0,2,2,0,-1), # dog in any col-backwards (starting row-2)
	(0,3,0,0,-1),(0,3,1,0,-1),(0,3,2,0,-1), # dog in any col-backwards (starting row-3)
	(0,2,2,-1,-1),(0,3,2,-1,-1), # dog in the diagonals-backwards
	(1,0,0,0,1),(1,0,1,0,1),(1,0,2,0,1), # ball in any col-forwards
	(1,3,0,0,-1),(1,3,1,0,-1),(1,3,2,0,-1), # ball in any col-backwards
	]
	
	received_rules = generateRules(state)

	expected_rules.sort()
	received_rules.sort()

	if received_rules != expected_rules:
		print 'error in testGenerateRules-1'
		#print [item for item in expected_rules if not item in received_rules]
	else:
		print 'success in testGenerateRules-1'
	
def testDescribeState():
	#print 'error in testDescribeState-not yet implemented'
	state = initializeState(4,3,['bog','ball'])
	recvd_msg = describeState(state,False)
	print recvd_msg
	xpctd_msg = "_ _ _ \n_ _ _ \n_ _ _ \n_ _ _ \n['bog', 'ball']"
	errorTestDescribeState(recvd_msg, xpctd_msg, 1)

	state.words = ['bog']
	state.grid = [['b','',''],['a','',''],['l','',''],['l','','']]
	recvd_msg = describeState(state,False)
	xpctd_msg = "b _ _ \na _ _ \nl _ _ \nl _ _ \n['bog']"
	errorTestDescribeState(recvd_msg, xpctd_msg, 2)

	state.words = ['ball']
	state.grid = [['b','o','g'],['','',''],['','',''],['','','']]
	recvd_msg = describeState(state,False)
	xpctd_msg = "b o g \n_ _ _ \n_ _ _ \n_ _ _ \n['ball']"
	errorTestDescribeState(recvd_msg, xpctd_msg, 3)

def errorTestDescribeState(recvd_msg,xpctd_msg,num):
	if recvd_msg != xpctd_msg:
		print 'error in testDescribeState-%d' % num
	else:
		print 'success in testDescribeState-%d' % num
		
def testDescribeRule():
	state = initializeState(4,3,['bog','ball'])
	rule = (1,1,0,1,1)
	recvd_msg = describeRule(rule,state,False)
	xpctd_msg = "Place the word \"ball\" in the grid starting at position (1,0) and proceeding in the direction [1,1]"
	if recvd_msg != xpctd_msg:
		print 'error in testDescribeRule-1'
	else:
		print 'success in testDescribeRule-1'

def testAll():
	testInitializeState()
	testGoal()
	testPrecondition()
	testGenerateRules()
	testDescribeState()
	testDescribeRule()
	
# Sanity checks helper functions
	
def checkWordsAssumptions(state):
	# we assume that any given word only appears once in the list
	# (we call list.remove)
	return True

def checkGridAssumptions(state):
	# empty cells in the grid are represented as empty strings ''
	# the multidimensional list is a grid (not a jagged list of lists of different sizes)
	return True

# Experiment Utilities

def describePath(path):
	if type(path) == str:
		print path
	else:
		path.reverse()
		print "--------------------------"
		print "Productions to reach goal: ", path
	print "We called backTrack %d times and failed %d times" % (calls_to_backtrack, states_not_goal)

# Experiments

def experimentFlailWildly():
	state = initializeState(4,3,['bog','ball'])
	flailWildly(state)

def experimentBackTrackSimple():
	state = initializeState(4,3,['bog','ball'])
	path = backTrack([state],10,True)
	describePath(path)
	
def experimentBackTrackExample():
	state = initializeState(12,12,
		['Admissible', 'Agent', 'Backtrack', 'Cannibal', 'Deadend',
		'Global', 'Graphsearch', 'Heuristic', 'Hill', 'LISP', 'Local',
		'Missionary', 'Optimum', 'Search', 'Symmetry'])
	path = backTrack([state],100,True)
	describePath(path)

def experimentBackTrackHard():
	# Ideal: bog, bal, god, aim, gal, lid, lam
	# b o g
	# a a o
	# l i d
	# l a m
	state = initializeState(4,3,['bog','ball','god','aim','lid'])
	path = backTrack([state],1000,True)
	describePath(path)
	# note that it doesn't 'notice' that `lid` is already there, so it adds
	# another copy of `lid` into it

# this doesn't converge, like ever. (1.5+ hrs @ depthBound = 10000000)
def experimentBackTrackSuperHard():
	# b o g
	# a a o
	# l i d
	# l a m
	state = initializeState(4,3,['bog','ball','aim','gal','god','lid','lam'])
	path = backTrack([state],10000000,True)
	describePath(path)

#experimentBackTrackExample()
experimentBackTrackHard()