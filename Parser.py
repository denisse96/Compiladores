import ply.yacc as yacc
import ply.lex as lex
import sys


reserved = {
    'program': 'PROGRAM',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'function': 'FUNCTION',
    'input': 'INPUT',
    'output': 'OUTPUT',
    'array': 'ARRAY',
    'int': 'INT',
    'float': 'FLOAT',
    'and': 'AND',
    'or': 'OR'

}

tokens = ['ID',
          'PLUS', 'MINUS', 'TIMES', 'DIVIDE',  'DOTCOMA', 'EQUALS',
          'GTHAN', 'LTHAN', 'GLTHAN',
          'CTESTRING', 'CTEINT', 'CTEFLOAT', 'LPAREN', 'RPAREN', 'LCOR', 'RCOR', 'COMA', 'DOSPUNTOS',  'LBRACKET',
                                    'RBRACKET'] + list(reserved.values())


t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
#t_CTEINT = r = r'[0-9]+'
#t_CTEFLOAT = r'[0-9]+.[0-9]+'
t_LCOR = r'{'
t_RCOR = r'}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_DOTCOMA = r';'
t_GTHAN = r'<'
t_LTHAN = r'>'
t_GLTHAN = r'<(.*)>'
#t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_CTESTRING = r'\"(.*)\"'
t_COMA = r','
t_DOSPUNTOS = r':'

print(sys.argv)
# Ignored characters
t_ignore = " \t"


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t


def t_CTEINT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_CTEFLOAT(t):
    r'(\d+|(\-)\d+)(\.)(\d+)'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Double value too large %d", t.value)
        t.value = 0.0
    return t


def t_ccode_comment(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    pass


def p_empty(p):
    'empty :'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


# Build the lexer
lexer = lex.lex()


def p_programa(t):
    'programa :  Declaracion LCOR Bloque RCOR AuxPrograma'
    print("entro a programa")


def p_error(t):
    print("Syntax error at '%s'" % t.value)


def p_AuxPrograma(t):
    '''AuxPrograma : Fc AuxPrograma
                   | empty'''


def p_Bloque(t):
    '''Bloque :  Statement DOTCOMA
            | Statement DOTCOMA Bloque '''


def p_Statement(t):  # | Asignacion | While
    '''Statement : Condicion
                   | Read
                   | Write'''


def p_Declaracion(t):
    '''Declaracion : DeclaracionArray
                | DeclaracionVariable
                | empty'''
    print("eentro a declaracion")


def p_DeclaracionArray(t):
    '''DeclaracionArray : ARRAY ID LBRACKET CTEINT RBRACKET DOTCOMA'''


def p_DeclaracionVariable(t):
    '''DeclaracionVariable :  Tipo ID DOTCOMA
                            |  Tipo ID DOTCOMA DeclaracionVariable'''


def p_Tipo(t):
    '''Tipo : INT
                | FLOAT'''
    print("\t tipo CORRECTO")


def p_Fc(t):
    '''Fc : FUNCTION ID LPAREN AuxFC RPAREN LCOR Declaracion Bloque RCOR'''


def p_AuxFC(t):
    '''AuxFC : Tipo ID 
             | Tipo ID COMA AuxFC
             | empty'''


def p_Read(t):
    '''Read : INPUT ID AuxRead'''


def p_AuxRead(t):
    '''AuxRead : LBRACKET Expresion RBRACKET
                | empty'''


def p_Write(t):
    '''Write : OUTPUT AuxWrite'''


def p_AuxWrite(t):  # | Letrero
    '''AuxWrite : Expresion
                '''


def p_Condicion(t):
    '''Condicion : IF LPAREN ExpresionLogica RPAREN LCOR Bloque RCOR AuxCondicion'''


def p_AuxCondicion(t):
    '''AuxCondicion : ELSE LCOR Bloque RCOR
                    | empty'''


def p_ExpresionLogica(t):
    '''ExpresionLogica : TerminoLogico
                        | ExpresionLogica OR TerminoLogico '''


def p_TerminoLogico(t):
    '''TerminoLogico : FactorLogico
                        | TerminoLogico AND FactorLogico'''


def p_Factor(t):
    '''Factor : LPAREN Expresion RPAREN
                    | CTEINT
                    | ID LBRACKET Expresion RBRACKET
                    | ID LPAREN AuxFactor RPAREN
                    | ID'''


def p_AuxFactor(t):
    '''AuxFactor : Expresion
                | Expresion COMA AuxFactor'''


def p_Termino(t):
    '''Termino : Factor
                | Termino TIMES Factor
                | Termino DIVIDE Factor'''


def p_Expresion(t):
    '''Expresion : Termino
                | Expresion PLUS Termino
                | Expresion MINUS Termino'''


def p_FactorLogico(t):
    '''FactorLogico : LPAREN ExpresionLogica RPAREN
                | AuxFactorLogico GTHAN AuxFactorLogico
                | AuxFactorLogico LTHAN AuxFactorLogico'''


def p_AuxFactorLogico(t):
    '''AuxFactorLogico : ID
                | CTEINT
                | CTEFLOAT'''


parser = yacc.yacc(start='programa')

print("VERIFICANDO CÓDIGO")


while 1:
    try:
        s = input('input> ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s)

print("VERIFICACIÓN TERMINADA")
