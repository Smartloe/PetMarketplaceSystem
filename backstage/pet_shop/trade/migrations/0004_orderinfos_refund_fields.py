from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('trade', '0003_alter_ordergoods_goods_num'),
	]

	operations = [
		migrations.AddField(
			model_name='orderinfos',
			name='refund_reason',
			field=models.CharField(blank=True, max_length=255, verbose_name='退款原因'),
		),
		migrations.AddField(
			model_name='orderinfos',
			name='refund_status',
			field=models.SmallIntegerField(choices=[(0, '无'), (1, '待审核'), (2, '已通过'), (3, '已拒绝')], default=0, verbose_name='退款状态'),
		),
	]
