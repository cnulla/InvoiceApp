from .models import Item

class InvoiceMixins(object):
    """ Add item/order
    """
    def add_item(self, invoice, item):
        item = Item(
            invoice=invoice, order_number=item.get('order_number'), order_description=item.get('order_description'),
            order_date=item.get('order_date'), end_date=item.get('end_date'), rate=item.get('rate'), total_hours=item.get('total_hours'),
            amount=item.get('amount'), total_amount=item.get('total_amount'), remarks=item.get('remarks'), item_type=item.get('item_type'),
            )
        item.save()




