service_on = True

def get_service_on() -> bool:
    global service_on
    return service_on

def set_service_on(status: bool):
    global service_on
    service_on = status