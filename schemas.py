from tortoise import fields, Model


class URL(Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=32, unique=True)

    lists: fields.ManyToManyRelation['URLList'] = fields.ManyToManyField('models.URLList', related_name='urls')

    def __str__(self):
        return self.url


class URLList(Model):
    id = fields.IntField(pk=True)
    url_list = fields.CharField(max_length=32, unique=True)
    urls: fields.ManyToManyRelation[URL]


class APIKey(Model):
    id = fields.UUIDField(pk=True)
    key = fields.CharField(max_length=32, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    is_active = fields.BooleanField(default=True)
