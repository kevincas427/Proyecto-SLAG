def total_carrito(request):
    total = 0
    if request.user.is_authenticated:
        if 'carrito' in request.session.keys():
            for clave, valor in request.session['carrito'].items():
                total += int(valor['precio'])
    return {'total_carrito': total}
    