from invoice.models import Item

class InvoiceMixins(object):

    def add_item(self, invoice, item):
        """ Add item/order
        """
        item = Item(
            invoice=invoice, order_number=item.get('order_number'), order_description=item.get('order_description'),
            order_date=item.get('order_date'), end_date=item.get('end_date'), rate=item.get('rate'),
            total_hours=item.get('total_hours'), amount=item.get('amount'), total_amount=item.get('total_amount'),
            remarks=item.get('remarks'), item_type=item.get('item_type'),
            )
        item.save()

    def update_item(self, invoice, data):
        """Update Item
        """
        item = Item.objects.get(id=data.get('id'))
        item.order_number = data.get('order_number')
        item.order_description = data.get('order_description')
        item.order_date = data.get('order_date')
        item.end_date = data.get('end_date')
        item.rate = data.get('rate')
        item.total_hours = data.get('total_hours')
        item.amount = data.get('amount')
        item.total_amount = data.get('total_amount')
        item.remarks = data.get('remarks')
        item.item_type = data.get('item_type')
        item.save()



