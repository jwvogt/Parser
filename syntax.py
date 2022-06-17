

# This file defines classes for AST nodes representing the WhileProc language.
# The CFG for WhileProc can be defined as follows (this includes extra credit):
#
# (starting symbol P)
# P -> S ";" P | S
# S -> "proc" f "(" L ")" "{" P "}"
#    | "if" C "{" P "}" "else" "{" P "}"
#    | "while" C "{" P "}"
#    | "print" C
#    | C
# L -> x "," X | x | Ɛ
# X -> x "," X | x
# C -> E | E "<" E | E "=" E
# E -> T | T M
# M -> "+" T M | "-" T M | Ɛ
# T -> F | F N
# N -> "*" F N | "/" F N | Ɛ
# F -> A | A "^" F
# A -> "(" C ")"
#    | x B
#    | f "(" R ")"
#    | n
# B -> ":" "=" C | Ɛ  ## this was added in order to left-factor A
# R -> C "," Q | C | Ɛ
# Q -> C "," Q | C
#
# You should follow this grammar, but will want to perform some implicit
# left-factoring (e.g., in nonterminal A), inlining (e.g., of L), and conversion
# of right-recursion into loops (e.g., M, N) when writing your top-down parser


class ASTNode:
    def run(self):
        (v,env,out) = self.interp({},"")
        return out
class SeqStmt(ASTNode):
    def __init__(self, lhs, rhs):
        # lhs and rhs are statements (ProcStmt,IfStmt,Plus,etc) sequenced with a semi-colon
        self.lhs = lhs
        self.rhs = rhs
    def interp(self,env,out):
        (v0,env0,out0) = self.lhs.interp(env,out)
        return self.rhs.interp(env0,out0)
    def __str__(self):
        return str(self.lhs) + ";" + str(self.rhs)
class ProcStmt(ASTNode):
    def __init__(self, f, params, body):
        # f is a Var object, params is a list of Var objects, body is a statement
        self.f = f
        self.params = params
        self.body = body
    def interp(self,env,out):
        env0 = env.copy()
        env0.update({self.f.id : self})
        return (1,env0,out)
    def __str__(self):
        return "proc "+str(self.f) + "(" + ",".join(map(str,self.params))+"){" + str(self.body) + "}"
class IfStmt(ASTNode):
    def __init__(self, guard, thenbody, elsebody):
        # guard is an expression object (Equal, LessThan, Mult, etc), thenbody is a Prog object, elsebody is a statement
        self.guard = guard
        self.thenbody = thenbody
        self.elsebody = elsebody
    def interp(self,env,out):
        (v0,env0,out0) = self.guard.interp(env,out)
        if v0 == 0:
            return self.elsebody.interp(env0,out0)
        else:
            return self.thenbody.interp(env0,out0)
    def __str__(self):
        return "if "+str(self.guard) + " {" + str(self.thenbody) + "} else {" + str(self.elsebody)+"}"
class WhileStmt(ASTNode):
    def __init__(self, guard, body):
        # guard is a Cond (or Plus, Lit, etc) object, body is a statement
        self.guard = guard
        self.body = body
    def interp(self,env,out):
        (v0,env0,out0) = self.guard.interp(env,out)
        if v0 != 0:
            (v0,env0,out0) = self.body.interp(env0,out0)
            return self.interp(env0,out0)
        else:
            return (0,env,out)
    def __str__(self):
        return "while "+str(self.guard)+" {"+str(self.body)+"}"
class PrintStmt(ASTNode):
    def __init__(self, rhs):
        # rhs is an expression (LessThan, Div, Expo, etc) object
        self.rhs = rhs
    def interp(self,env,out):
        (v0,env0,out0) = self.rhs.interp(env,out)
        return (0,env0,out0+str(v0)+"\n")
    def __str__(self):
        return "print " + str(self.rhs)
class LessThan(ASTNode):
    def __init__(self, lhs, rhs):
        # lhs and rhs are expressions (Plus, Mult, etc) objects
        self.lhs = lhs
        self.rhs = rhs
    def interp(self,env,out):
        (v0,env0,out0) = self.lhs.interp(env,out)
        (v1,env1,out1) = self.rhs.interp(env0,out0)
        if v0 < v1:
            return (1,env1,out1)
        else:
            return (0,env1,out1)
    def __str__(self):
        return "("+str(self.lhs) + "<" + str(self.rhs)+")"
class Equal(ASTNode):
    def __init__(self, lhs, rhs):
        # lhs and rhs are expression (Plus, Mult, etc) objects
        self.lhs = lhs
        self.rhs = rhs
    def interp(self,env,out):
        (v0,env0,out0) = self.lhs.interp(env,out)
        (v1,env1,out1) = self.rhs.interp(env0,out0)
        if v0 == v1:
            return (1,env1,out1)
        else:
            return (0,env1,out1)
    def __str__(self):
        return "("+str(self.lhs) + "=" + str(self.rhs)+")"
class Plus(ASTNode):
    def __init__(self, lhs, rhs):
        # lhs and rhs are expression (Plus, Mult, etc) objects
        self.lhs = lhs
        self.rhs = rhs
    def interp(self,env,out):
        (v0,env0,out0) = self.lhs.interp(env,out)
        (v1,env1,out1) = self.rhs.interp(env0,out0)
        return (v0+v1,env1,out1)
    def __str__(self):
        return "("+str(self.lhs) + "+" + str(self.rhs)+")"
class Minus(ASTNode):
    def __init__(self, lhs, rhs):
        # lhs and rhs are expression (Plus, Mult, etc) objects
        self.lhs = lhs
        self.rhs = rhs
    def interp(self,env,out):
        (v0,env0,out0) = self.lhs.interp(env,out)
        (v1,env1,out1) = self.rhs.interp(env0,out0)
        return (v0-v1,env1,out1)
    def __str__(self):
        return "("+str(self.lhs) + "-" + str(self.rhs)+")"
class Mult(ASTNode):
    def __init__(self, lhs, rhs):
        # lhs and rhs are expression (Div, Mult, etc) objects
        self.lhs = lhs
        self.rhs = rhs
    def interp(self,env,out):
        (v0,env0,out0) = self.lhs.interp(env,out)
        (v1,env1,out1) = self.rhs.interp(env0,out0)
        return (v0*v1,env1,out1)
    def __str__(self):
        return "("+str(self.lhs) + "*" + str(self.rhs)+")"
class Div(ASTNode):
    def __init__(self, lhs, rhs):
        # lhs and rhs are expression (Div, Mult, etc) objects
        self.lhs = lhs
        self.rhs = rhs
    def interp(self,env,out):
        (v0,env0,out0) = self.lhs.interp(env,out)
        (v1,env1,out1) = self.rhs.interp(env0,out0)
        if v1 == 0:
            return (float('nan'),env1,out1)
        return (v0/v1,env1,out1)
    def __str__(self):
        return "("+str(self.lhs) + "/" + str(self.rhs)+")"
class Expo(ASTNode):
    def __init__(self, lhs, rhs):
        # lhs and rhs are expression (Expo, Assign, etc) objects
        self.lhs = lhs
        self.rhs = rhs
    def interp(self,env,out):
        (v0,env0,out0) = self.lhs.interp(env,out)
        (v1,env1,out1) = self.rhs.interp(env0,out0)
        return (v0**v1,env1,out1)
    def __str__(self):
        return "("+str(self.lhs) + "^" + str(self.rhs)+")"
class Assign(ASTNode):
    def __init__(self, lhs, rhs):
        # lhs is a Var object, and rhs is an expression (Plus, Assign, Mult, etc) object
        self.lhs = lhs
        self.rhs = rhs
    def interp(self,env,out):
        (v0,env0,out0) = self.rhs.interp(env,out)
        env1 = env0.copy()
        env1.update({self.lhs.id : v0})
        return (v0,env1,out0)
    def __str__(self):
        return "("+str(self.lhs) + ":=" + str(self.rhs)+")"
class Call(ASTNode):
    def __init__(self, f, args):
        # f is a Var object and args is a list of expression objects (LessThan, Mult, etc)
        self.f = f
        self.args = args
    def interp(self,env,out):
        pr = env[self.f.id]
        if isinstance(pr, ProcStmt):
            if len(pr.params) == len(self.args):
                evalargs = []
                lastenv = env
                lastout = out
                for v in self.args:
                    (v0,env0,out0) = v.interp(lastenv,lastout)
                    lastenv = env0
                    lastout = out0
                    evalargs.append(v0)
                (v0,env0,out0) = pr.body.interp({ k.id : v for (k,v) in zip(pr.params,evalargs)}, out)
                return (v0,env,out0)
            else:
                print("Runtime error: procedure call with wrong arity.")
        else:
            print("Runtime error: invoked value is not a procedure.")
        exit(1)
    def __str__(self):
        return str(self.f) + "(" + ",".join(map(str,self.args)) + ")"
class Var(ASTNode):
    def __init__(self, ident): 
        # ident is a string encoding the variable's identifier               
        self.id = ident
    def interp(self,env,out):
        return (env[self.id],env,out)
    def __str__(self):
        return str(self.id)
class Lit(ASTNode):
    def __init__(self, s):
        # s is a string encoding the literal integer or floating point value 
        self.n = float(s)
    def interp(self,env,out):
        return (self.n,env,out)
    def __str__(self):
        return str(self.n)
class ErrorMsg(ASTNode):
    def __init__(self, s):
        # This node should be returned when parsing malformed input (e.g., "proc f(){}")
        # s is an error string
        self.s = s
    def interp(self,env,out):
        print(self.s)
        return (0,env,out+self.s+"\n")
    def __str__(self):
        return self.s
    

    
