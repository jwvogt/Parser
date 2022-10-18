#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from syntax import *


# I *Jack Vogt* have written all of this project myself, without any
# unauthorized assistance, and have followed the academic honor code.


def lex(s):
    def match_groups(s):
        m1 = re.match(r'^\s*(([a-z]|[A-Z]|\_)([a-z]|[A-Z]|[0-9])*)', s)
        m2 = re.match(r'^\s*([0-9]*\.?[0-9]+)', s)
        m3 = re.match(r'^\s*(proc|if|else|while|print)', s)
        m4 = re.match(r'^\s*(\+|\-|\/|\*|\^|\,|\:|\=|\<|\{|\}|\(|\)|\;)', s)
        return m1, m2, m3, m4

    toks = []
    m1, m2, m3, m4 = match_groups(s)
    
    while m1 is not None or m2 is not None or m3 is not None or m4 is not None:

        while m1 is not None:
            toks.append(m1.group(1))
            s = s[len(m1.group(0)):]
            m1, m2, m3, m4 = match_groups(s)
        while m2 is not None:
            toks.append(m2.group(1))
            s = s[len(m2.group(0)):]
            m1, m2, m3, m4 = match_groups(s)
        while m3 is not None:
            toks.append(m3.group(1))
            s = s[len(m3.group(0)):]
            m1, m2, m3, m4 = match_groups(s)
        while m4 is not None:
            toks.append(m4.group(1))
            s = s[len(m4.group(0)):]
            m1, m2, m3, m4 = match_groups(s)
    return toks

def parse(toks):
    # TODO: parse and return an AST node or ErrorMsg object
    def peek(n):
        # looks at next token in toks
        nonlocal toks
        if n < len(toks):
            return toks[n]
        else:
            return ''
    def expect(tok):
        nonlocal toks
        if peek(0) == tok:
            toks = toks[1:]
        else:
            print('Error, expected token "' + str(tok) + '", got: "' + str(toks) + '"')
            exit(1)
    
    def parseP():
        p = parseS()
        while peek(0) == ';':
            expect(';')
            p = SeqStmt(p, parseS())
        return p

    def parseS():
        s = ''
        if peek(0) == 'proc':
            expect('proc')
            f = Var(peek(0))
            expect(peek(0))
            expect('(')
            params = parseL()
            expect(')')
            expect('{')
            body = parseP()
            expect('}')
            s = ProcStmt(f, params, body)
        elif peek(0) == 'if':
            expect('if')
            guard = parseC()
            expect('{')
            thenbody = parseP()
            expect('}')
            expect('else')
            expect('{')
            elsebody = parseP()
            expect('}')
            s = IfStmt(guard, thenbody, elsebody)
        elif peek(0) == 'while':
            expect('while')
            guard = parseC()
            expect('{')
            body = parseP()
            expect('}')
            s = WhileStmt(guard, body)
        elif peek(0) == 'print':
            expect('print')
            rhs = parseC()
            s = PrintStmt(rhs)
        else:
            s = parseC()
        return s
            
    def parseL():
        l = []
        if peek(0) == ')':
            return l
        else:
            l.append(Var(peek(0)))
            expect(peek(0))
            while peek(0) == ',':
                expect(',')
                l.append(Var(peek(0)))
                expect(peek(0))
        return l

    def parseC():
        c = parseE()
        if peek(0) == '<':
            expect('<')
            c = LessThan(c, parseE())
        elif peek(0) == '=':
            expect('=')
            c = Equal(c, parseE())
        return c
    
    def parseE():
        e = parseT()
        if peek(0) == '+':
            e = Plus(e, parseM())
        elif peek(0) == '-':
            e = Minus(e, parseM())
        return e
    
    def parseM():
        m = ''
        if peek(0) == '+':
            expect('+')
            m = parseT()
        elif peek(0) == '-':
            expect('-')
            m = parseT()
        while peek(0) == '+' or peek(0) == '-':
            if peek(0) == '+':
                expect('+')
                m = Plus(m, parseT())
            if peek(0) == '-':
                expect('-')
                m = Minus(m, parseT())
        return m

    def parseT():
        t = parseF()
        if peek(0) == '*':
            t = Mult(t, parseN())
        elif peek(0) == '/':
            t = Div(t, parseN())
        return t
    
    def parseN():
        n = ''
        if peek(0) == '*':
            expect('*')
            n = parseF()
        elif peek(0) == '/':
            expect('/')
            n = parseF()
        while peek(0) == '*' or peek(0) == '/':
            if peek(0) == '*':
                expect('*')
                n = Mult(n, parseF())
            elif peek(0) == '/':
                expect('/')
                n = Div(n, parseF())
        return n
    
    def parseF():
        f = parseA()
        while peek(0) == '^':
            expect('^')
            f = Expo(parseA(), f)
        return f
    
    def parseA():
        a = ''
        if peek(0) == '(':
            expect('(')
            a = parseC()
            expect(')')
        if re.match(r'[0-9]*\.?[0-9]+', peek(0)):
            a = Lit(peek(0))
            expect(peek(0))
        elif re.match(r'([a-z]|[A-Z]|\_)([a-z]|[A-Z]|[0-9])*', peek(0)):
            a = Var(peek(0))
            expect(peek(0))
            if peek(0) == '(':
                expect('(')
                a = Call(a, parseR())
                expect(')')
            elif peek(0) == ':':
                while peek(0) == ':':
                    expect(':')
                    expect('=')
                    a = Assign(a, parseC())
        return a

    def parseR():
        r = []
        if peek(0) == ')':
            return r
        else:
            r.append(parseC())
            while peek(0) == ',':
                expect(',')
                r.append(parseC())
                # expect(peek(0))
        return r

    return parseP()


# Some example tests:
#
# print(parse(lex('proc test() {print 7 < 6; print 4 < 5}; test()')).run())
# print(parse(lex('proc assign(a, b){ a := b := 0 }; sum1 := 100; sum2 := 100; print assign(sum1,sum2)')).run())
# print(parse(lex('proc sum(n,s){sum := i := 0; while i < n {i := i+s;sum := sum + i};sum};n := 100;step := 0.5;print sum(n,step)')).run())
