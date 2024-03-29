from ast import Expression, Lambda
import sys
import os
from turtle import xcor
from typing import Type

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

##############
# Eval/Apply #
##############


def scheme_eval(expr, env, _=None):  # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr
    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:
        return scheme_forms.SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 3
        "*** YOUR CODE HERE ***"
        # apply scheme eval to all parts of the expression, in which if its a multiple procedure, it will return that expr and apply it

        symbol = scheme_eval(expr.first, env)
        rest = expr.rest.map(lambda x: scheme_eval(x, env))
        return scheme_apply(symbol, rest, env)
        # END PROBLEM 3


def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    validate_procedure(procedure)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        "*** YOUR CODE HERE ***"
        py_list = []
        while args is not nil:
            py_list += [args.first]
            args = args.rest
        if procedure.expect_env is True:
            py_list += [env]
        try:
            return procedure.py_func(*py_list)
        except TypeError:
            raise SchemeError('incorrect number of arguments')
        # END PROBLEM 2
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        "*** YOUR CODE HERE ***"
        # env is where the procedure is called frame possibly (GF), the frame should be a new frame below the definition of the frame (f1)
        # so it should be the procedure's env and the child of that env where lambda is called and the body is evaluated 
        new_env = procedure.env.make_child_frame(procedure.formals, args)
        return eval_all(procedure.body, new_env)         
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        "*** YOUR CODE HERE ***"
        new_env = env.make_child_frame(procedure.formals, args)
        return eval_all(procedure.body, new_env)
        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)


def eval_all(expressions, env):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last.

    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    # BEGIN PROBLEM 6
    if expressions == nil:
        return None
    while expressions.rest is not nil:
        scheme_eval(expressions.first, env)
        expressions = expressions.rest
    return scheme_eval(expressions.first, env, True)
    # END PROBLEM 6


##################
# Tail Recursion #
##################

class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env


def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val

def optimize_tail_calls(original_scheme_eval):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        # evaluates to another expression for further evaluation
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)
        result = Unevaluated(expr, env)
        # BEGIN PROBLEM EC
        "*** YOUR CODE HERE ***"
        #  
        # calling on original scheme expression until it evaluates to some value, then returning that value at the end which is making it sort of alike a retrival rather than computation
        # stores expression until the next one evaluates to that value  
        # so by the end we can call unevaluated and evaluate it, until we recieve a value which is what we return
        # when we do this we only store the value into result, discarding the rest of the frames, this is tail recursive because at the end of the implementation, we can just return the answer
        # in comparison with the other, where we would need to keep the frames since we're doing some recursive call to them here keeping it (active), we only return at the end of the result
        # keeping the stack retrieval at constant time 
        while isinstance(result, Unevaluated):
            result = original_scheme_eval(result.expr, result.env)
        return result
        # END PROBLEM EC
    return optimized_eval
################################################################
# Uncomment the following line to apply tail call optimization #
################################################################
scheme_eval = optimize_tail_calls(scheme_eval)
