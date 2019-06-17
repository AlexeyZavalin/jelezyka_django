from django import forms
from catalogapp.models import StockProduct


class AddForm(forms.Form):
    def __init__(self, product_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_id = product_id
        stocks = StockProduct.objects.filter(product__id=self.product_id)
        for stock_item in stocks:
            count = 'count_%s' % (stock_item.stock.key,)
            choose = 'choose_%s' % (stock_item.stock.key,)
            address = 'address_%s' % (stock_item.stock.address)
            self.fields[choose] = forms.BooleanField()
            self.fields[address] = forms.CharField()
            self.fields[count] = forms.IntegerField(required=True, initial=1, max_value=stock_item.count, min_value=1)
