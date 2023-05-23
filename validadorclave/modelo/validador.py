from abc import ABC, abstractmethod

from validadorclave.modelo.errores import *


class ReglaValidacion(ABC):
    def __init__(self, longitud_esperada: int):
        self.longitud_esperada: int = longitud_esperada

    def _validar_longitud(self, clave: str) -> bool:
        if len(clave) > self.longitud_esperada:
            return True
        return False

    def _contiene_mayuscula(self, clave: str) -> bool:
        if not any(letra.isupper() for letra in clave):
            return False
        return True

    def _contiene_minuscula(self, clave: str) -> bool:
        if not any(letra.islower() for letra in clave):
            return False
        return True

    def _contiene_numero(self, clave: str) -> bool:
        if not any(letra.isdigit() for letra in clave):
            return False
        return True

    @abstractmethod
    def es_valida(self, clave: str) -> bool:
        pass


class ReglaValidacionGanimedes(ReglaValidacion):
    def __init__(self):
        super().__init__(longitud_esperada = 8)

    def contiene_caracter_especial(self, clave: str) -> bool:
        caracteres = "@_#%$"

        for letra in clave:
            if letra in caracteres:
                return True
            continue
        return False

    def es_valida(self, clave: str) -> bool:
        if not self._validar_longitud(clave):
            raise NoCumpleLongitudMinimaError
        elif not self._contiene_mayuscula(clave):
            raise NoTieneLetraMayusculaError
        elif not self._contiene_minuscula(clave):
            raise NoTieneLetraMinusculaError
        elif not self._contiene_numero(clave):
            raise NoTieneNumeroError
        elif not self.contiene_caracter_especial(clave):
            raise NoTieneCaracterEspecialError
        else:
            return True


class ReglaValidacionCalisto(ReglaValidacion):
    def __init__(self):
        super().__init__(longitud_esperada = 6)

    def contiene_calisto(self, clave: str) -> bool:
        clave_lower = clave.lower()
        indice = clave_lower.find('calisto')
        while indice != -1:
            calisto = clave[indice: indice + 7]
            num_mayusculas = sum(1 for letra in calisto if letra.isupper())
            if 2 <= num_mayusculas < len(calisto):
                return True
            indice = clave_lower.find('calisto', indice + 1)
        return False

    def es_valida(self, clave: str) -> bool:
        if not self._validar_longitud(clave):
            raise NoCumpleLongitudMinimaError
        elif not self._contiene_numero(clave):
            raise NoTieneNumeroError
        elif not self.contiene_calisto(clave):
            raise NoTienePalabraSecretaError
        else:
            return True


class Validador:

    def __init__(self, regla: ReglaValidacion):
        self.regla: ReglaValidacion = regla

    def es_valida(self, clave: str) -> bool:
        return self.regla.es_valida(clave)
