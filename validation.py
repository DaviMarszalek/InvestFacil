# validation.py
import re

def formatar_cpf(cpf):
    """Remove caracteres não numéricos do CPF."""
    return re.sub(r'[^0-9]', '', cpf)

def validar_cpf(cpf):
    """Valida um CPF brasileiro."""
    cpf = formatar_cpf(cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    if resto == 10: resto = 0
    if resto != int(cpf[9]):
        return False
        
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    if resto == 10: resto = 0
    if resto != int(cpf[10]):
        return False
        
    return True