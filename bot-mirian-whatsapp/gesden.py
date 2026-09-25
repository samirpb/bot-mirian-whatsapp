def get_horarios(fecha=None):
    # Versión compatible con app.py - si no le pasas fecha, te da los de hoy
    # Luego aquí conectamos a Gesden real de Bellness / Linda Valencia
    horarios_base = ["09:00", "10:30", "11:30", "15:00", "16:30"]
    if fecha:
        return f"Horarios para {fecha}: " + ", ".join(horarios_base)
    return ", ".join(horarios_base)

def agendar_cita(numero=None, mensaje=None, nombre=None, telefono=None, servicio=None, fecha=None, hora=None):
    # Versión compatible con app.py - acepta 2 argumentos o 5
    # Para no romper Render mientras integramos Gesden real
    
    # Caso 1: viene del app.py nuevo (numero, mensaje)
    if numero and mensaje:
        print(f"[MIRIAN] Agendando solicitud de {numero}: {mensaje}")
        # Aquí luego parseas el mensaje y llamas a Gesden real
        return f"Cita pre-agendada para {numero}. Mensaje: '{mensaje}'. Te confirmo en 5 min por WhatsApp ✅"

    # Caso 2: viene del formato antiguo (nombre, telefono, etc)
    print(f"Agendando en Gesden: {nombre} - {servicio} {fecha} {hora} - Tel: {telefono}")
    return True

def cancelar_cita(telefono, fecha=None):
    print(f"Cancelando cita de {telefono} para {fecha}")
    return True
