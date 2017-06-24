from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.

'''
import pdb
pdb.set_trace()
'''

def backchain_to_goal_tree(rules, hypothesis):
	hypothesis= OR(hypothesis)
	for rule in rules:
		var_list= match(rule.consequent()[0], hypothesis[0]) #assume that rule.consequent() and hypothesis have exactly one string
		if var_list==None:
			continue

		else:
			if isinstance(rule.antecedent(), basestring):
				appendage= [backchain_to_goal_tree(rules, populate(rule.antecedent(), var_list))]
			else:
				appendage= [backchain_to_goal_tree(rules, populate(data, var_list)) 
							for data in rule.antecedent()]

			if isinstance(rule.antecedent(), AND):
				appendage= AND(appendage)
			else:	
			#catch if class= basestring also, because it will be removed in simplify()
				appendage= OR(appendage)

			hypothesis.append(appendage)

	return simplify(hypothesis)

# Here's an example of running the backward chainer - uncomment
# it to see it work:
print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
