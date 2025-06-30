# modulo_demo/__init__.py

def saludar(nombre="usuario"):
    return {"mensaje": f"Hola, {nombre}. Soy el módulo demo de H-Brain."}

def sumar(a=0, b=0):
    return {"resultado": float(a) + float(b)}
