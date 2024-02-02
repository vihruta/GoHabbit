from tortoise import fields
from tortoise.models import Model
import json


class BotUser(Model):
    id = fields.BigIntField(pk=True, unique=True, generated=False)  # telegram user id
    username = fields.TextField(null=True)
    full_name = fields.TextField()
    joined_at = fields.DatetimeField(auto_now_add=True)
    timezone = fields.IntField(null=True)
    left_at = fields.DatetimeField(null=True)
    trial_requests_remaining = fields.IntField(default=10, null=True)
    subscription_started_at = fields.DatetimeField(null=True)
    subscription_expires_at = fields.DatetimeField(null=True)
    habit_schedule = fields.JSONField(null=True)

    async def set_habit_schedule(self, habit_type, habit_date_list):
        current_reminder_data = self.habit_schedule or {}
        current_reminder_data[habit_type] = habit_date_list
        self.habit_schedule = json.dumps(current_reminder_data)
        await self.save()

    @property
    def mention(self):
        if self.username:
            return f"@{self.username}"

        return f'<a href="tg://user?id={self.id}">{self.full_name}</a>'

    @property
    def url(self):
        if self.username:
            return f"https://t.me/{self.username}"

        return f"tg://user?id={self.id}"


class BotChat(Model):
    id = fields.BigIntField(
        pk=True, unique=True, generated=False
    )  # telegram chat id signed
    title = fields.TextField()
    username = fields.TextField(null=True)
    type = fields.TextField()


class StateBucket(Model):
    id = fields.IntField(pk=True, unique=True)
    bot_id = fields.BigIntField()
    chat_id = fields.BigIntField()
    user_id = fields.BigIntField()
    state = fields.TextField(null=True)
    data = fields.JSONField(default={})
