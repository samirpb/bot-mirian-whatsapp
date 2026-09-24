def get_horarios(fecha):
    # Por ahora simulado, luego conectamos a Gesden real
    return ["09:00", "10:30", "15:00", "16:30"]

def agendar_cita(nombre, telefono, servicio, fecha, hora):
    print(f"Agendando en Gesden: {nombre} - {servicio} {fecha} {hora}")
    return True

def cancelar_cita(telefono, fecha):
    return True