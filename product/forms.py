from  django.forms import ModelForm
from .models import Client


class ClientForm(ModelForm):
	class Meta:
		model = Client
		fields = ['name', 'adres', 'contract_number', 'inn_number','reg_code','director','counter']
		labels = {'name': 'Tashkilot *','adres':"Tashkilot manzili *", 'contract_number':'Shartnoma raqami', 'inn_number':'INN raqami(Идентификационный номер ИНН)','reg_code':'QQS kodi (Регистрационный код плательщика НДС)',
			'director':'Direktor','counter':'Xisobchi'}
		help__texts = {'name': 'Tashkilot nomini kiriting!'}


	def __init__(self, *args, **kwargs):
		super(ClientForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs={'placeholder': 'Tashkilot nomi','class':'form-control'}	
		self.fields['adres'].widget.attrs={'placeholder': 'Tashkilot manzili'}	
		self.fields['contract_number'].widget.attrs={'placeholder': 'Shartnoma raqami'}	
		self.fields['inn_number'].widget.attrs={'placeholder': 'INN raqami'}	
		self.fields['reg_code'].widget.attrs={'placeholder': 'QQS kodi'}	
		self.fields['director'].widget.attrs={'placeholder': 'Tashkilot raxbari I.F'}	
		self.fields['counter'].widget.attrs={'placeholder': 'Xisobchi I.F'}	
		