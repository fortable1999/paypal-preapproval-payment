"""
payment forms generated by template

template author: Meng Zhao fortable1999@gmail.com
"""

from django import forms
from payment.models import Payment


class PaymentModelForm(forms.ModelForm):
	"""
	model form using Payment model
	"""
	class Meta:
		model = Payment
		fields = (
			'text',
		)


class PaymentForm(forms.Form):
	"""
	form using Payment model
	"""
	text = forms.CharField(widget=forms.Textarea)

