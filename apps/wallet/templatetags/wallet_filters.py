from django import template

register = template.Library()


@register.filter
def miles(value):
    """Formatea un número con separador de miles (punto) sin decimales.
    Ej: 1234567 → 1.234.567
    """
    try:
        formatted = '{:,.0f}'.format(float(value))
        return formatted.replace(',', '.')
    except (ValueError, TypeError):
        return value
