
from django import forms
from django.db.models import CharField
from django.forms import ChoiceField, ModelMultipleChoiceField

DIAS = { 
    '1' : 'Lunes', 
    '2' : 'Martes', 
    '3' : 'Miércoles', 
    '4' : 'Jueves', 
    '5' : 'Viernes', 
    '6' : 'Sábado', 
    '7' : 'Domingo', 
} 

companhias = {  '1' : 'Iberia',
                '2' : 'Air Dream',
                '3' : 'Fly Eminem',
                '4' : 'Astro Drum',
                '5' : 'Aerolineas Continental',
                '6' : 'Americans Air Dream',
                '7' : 'Fly ForFly'}

#dias = ['Lunes','Martes',  'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'  ]

class DayWeekField(CharField): 
    def __init__(self, *args, **kwargs): 
        kwargs['choices']=tuple(sorted(DIAS.items())) 
        kwargs['max_length']=1 
        super(DayWeekField,self).__init__(*args, **kwargs) 

class FlyCompanyModelField(CharField): 
    def __init__(self, *args, **kwargs): 
        kwargs['choices']=tuple(sorted(companhias.items())) 
        kwargs['max_length'] = 1 
        kwargs['default'] = 1
        super(FlyCompanyModelField,self).__init__(*args, **kwargs) 

class FlyCompanyFormField(ChoiceField): 
    def __init__(self, *args, **kwargs): 
        kwargs['choices']= tuple(sorted(companhias.items())) 
        kwargs['label'] = 'Compañía aérea'
        super(FlyCompanyFormField,self).__init__(*args, **kwargs) 

class ExcursionModelMultipleChoiceField(ModelMultipleChoiceField):
    def __init__(self, queryset,**kwargs) -> None:
        kwargs['label'] = 'Excursiones'
        kwargs['required'] = False
        kwargs['widget'] = forms.SelectMultiple(attrs={"onchange":"exc_opcionChange(this);"})
        super().__init__(queryset, **kwargs)
    
    def label_from_instance(self, obj) -> str:
        return f'{obj}   -->  {obj.precio}'