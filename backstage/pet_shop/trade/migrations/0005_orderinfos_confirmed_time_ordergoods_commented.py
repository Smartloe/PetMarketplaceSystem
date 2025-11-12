from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('trade', '0004_orderinfos_refund_fields'),
	]

	operations = [
		migrations.AddField(
			model_name='orderinfos',
			name='confirmed_time',
			field=models.DateTimeField(blank=True, null=True, verbose_name='确认收货时间'),
		),
		migrations.AddField(
			model_name='ordergoods',
			name='commented',
			field=models.BooleanField(default=False, verbose_name='已评论'),
		),
	]
