from django import template

register = template.Library()

@register.inclusion_tag('chart/tags/chart.html', takes_context=True)
def chart_render(context, chart):
    print chart.title
    
    return {'chart': chart, 'STATIC_URL': context['STATIC_URL']}