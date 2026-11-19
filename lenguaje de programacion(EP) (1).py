# ==========================================
# TRABAJO FINAL - LENGUAJES DE PROGRAMACIÓN
# Sistema de Salud Rural - UPN (UAIN1288P)
# Versión Funcional y Definitiva
# ==========================================

from functools import reduce

class ErrorSalud(Exception):
    """Excepción personalizada para el control de errores del sistema."""
    pass

class Paciente:
    def __init__(self, dni: str, nombre: str, edad: int, diagnostico: str):
        # Aplicación de la Ley N.º 29733 (Protección de Datos Personales)
        self.__dni = self.__ocultar_dni(dni)
        self.nombre = nombre
        self.edad = self.__validar_edad(edad)
        self.diagnostico = diagnostico

    @property
    def dni(self) -> str:
        """Getter seguro para acceder al DNI enmascarado."""
        return self.__dni

    def __validar_edad(self, edad: int) -> int:
        if not isinstance(edad, int) or edad < 0 or edad > 120:
            raise ErrorSalud(f"Edad '{edad}' no válida. Debe estar entre 0 y 120.")
        return edad

    def __ocultar_dni(self, dni: str) -> str:
        """Enmascara el DNI para cumplir con la normativa peruana de datos personales."""
        if not dni or len(str(dni)) != 8 or not str(dni).isdigit():
            raise ErrorSalud("El DNI debe contener exactamente 8 dígitos numéricos.")
        # Oculta los primeros 6 dígitos (Ley N.º 29733)
        return f"***-***-{str(dni)[-2:]}"

    def to_dict(self) -> dict:
        return {
            "dni_protegido": self.__dni,
            "nombre": self.nombre,
            "edad": self.edad,
            "diagnostico": self.diagnostico
        }

class AtencionMedica:
    def __init__(self, id_atencion: int, paciente: Paciente, costo: float):
        self.id_atencion = id_atencion
        self.paciente = paciente
        self.costo = float(costo)

class GestorSaludRural:
    def __init__(self):
        self._atenciones = []

    def registrar_atencion(self, atencion: AtencionMedica) -> None:
        if not isinstance(atencion, AtencionMedica):
            raise ErrorSalud("Objeto de atención médica inválido.")
        self._atenciones.append(atencion)

    def buscar_mayores_de(self, edad_minima: int) -> list:
        """Paradigma funcional: uso de filter y map sobre colecciones del sistema."""
        pacientes = [a.paciente for a in self._atenciones]
        filtrados = filter(lambda p: p.edad > edad_minima, pacientes)
        return list(map(lambda p: p.to_dict(), filtrados))

    def calcular_recaudacion_total(self) -> float:
        """Paradigma funcional: uso de reduce para sumar los costos acumulados."""
        if not self._atenciones:
            return 0.0
        costos = [a.costo for a in self._atenciones]
        return reduce(lambda acumulado, actual: acumulado + actual, costos)

def ejecutar_pruebas_automaticas():
    """Pruebas automatizadas requeridas por la rúbrica (Evidencia para el informe)."""
    print("\n[TEST] Ejecutando pruebas automatizadas del sistema...")
    gestor = GestorSaludRural()

    # 1. Prueba de Ley 29733 (Enmascaramiento de DNI)
    p1 = Paciente("45678912", "Carlos Mendoza", 45, "Infección respiratoria")
    assert p1.dni == "***-***-12", "Error en la protección de datos del DNI."
    
    at1 = AtencionMedica(1, p1, 45.00)
    gestor.registrar_atencion(at1)

    p2 = Paciente("12345678", "María Rojas", 60, "Control hipertensión")
    at2 = AtencionMedica(2, p2, 30.50)
    gestor.registrar_atencion(at2)

    # 2. Prueba de funciones de orden superior (filter / map)
    mayores = gestor.buscar_mayores_de(50)
    assert len(mayores) == 1
    assert mayores[0]["nombre"] == "María Rojas"

    # 3. Prueba de reduce (Cálculo total)
    total = gestor.calcular_recaudacion_total()
    assert total == 75.50

    # 4. Prueba de manejo de excepciones
    excepcion_capturada = False
    try:
        Paciente("123", "Error", 20, "Ninguno")
    except ErrorSalud:
        excepcion_capturada = True
    assert excepcion_capturada, "El sistema no atrapó el error de DNI inválido."

    print("[TEST] ¡Todas las pruebas automatizadas pasaron con éxito!\n")

def menu_interactivo():
    # Ejecutamos las pruebas automáticas primero como exige la rúbrica
    ejecutar_pruebas_automaticas()
    
    gestor = GestorSaludRural()
    print("=" * 50)
    print(" SISTEMA DE GESTIÓN DE SALUD RURAL - UPIN")
    print("=" * 50)

    while True:
        print("\n--- MENÚ DE OPERACIONES ---")
        print("1. Registrar nuevo paciente y atención")
        print("2. Buscar pacientes por edad mínima (Filtro Funcional)")
        print("3. Ver recaudación total (Reduce Funcional)")
        print("4. Salir del programa")

        opcion = input("Seleccione una opción (1-4): ").strip()

        if opcion == "1":
            try:
                print("\n--- NUEVO REGISTRO ---")
                dni = input("Ingrese DNI (8 dígitos): ").strip()
                nombre = input("Ingrese Nombre completo: ").strip()
                edad = int(input("Ingrese Edad: "))
                diagnostico = input("Ingrese Diagnóstico médico: ").strip()
                costo = float(input("Ingrese Costo de la atención (S/): "))

                paciente = Paciente(dni, nombre, edad, diagnostico)
                id_nuevo = len(gestor._atenciones) + 1
                atencion = AtencionMedica(id_nuevo, paciente, costo)
                gestor.registrar_atencion(atencion)

                print(f"\n[ÉXITO] Paciente registrado correctamente.")
                print(f"-> DNI protegido por Ley 29733: {paciente.dni}")
            except ValueError:
                print("\n[ERROR] Ingrese valores numéricos válidos para la edad y el costo.")
            except ErrorSalud as e:
                print(f"\n[ERROR DE VALIDACIÓN] {e}")

        elif opcion == "2":
            try:
                edad_min = int(input("\nIngrese la edad mínima de búsqueda: "))
                resultados = gestor.buscar_mayores_de(edad_min)
                print(f"\n--- PACIENTES MAYORES DE {edad_min} AÑOS ---")
                if not resultados:
                    print("No se encontraron registros que cumplan la condición.")
                else:
                    for r in resultados:
                        print(f"• Nombre: {r['nombre']} | Edad: {r['edad']} | DNI: {r['dni_protegido']} | Diagnóstico: {r['diagnostico']}")
            except ValueError:
                print("\n[ERROR] Ingrese un número entero válido.")

        elif opcion == "3":
            total = gestor.calcular_recaudacion_total()
            print(f"\n--- RECAUDACIÓN TOTAL ACUMULADA ---")
            print(f"S/ {total:.2f}")

        elif opcion == "4":
            print("\nSaliendo del sistema. ¡Mucho éxito en tu presentación final!")
            break
        else:
            print("\n[AVISO] Opción no válida. Elija un número entre 1 y 4.")

if __name__ == "__main__":
    menu_interactivo()