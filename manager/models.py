# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
#   *   This includes altering keys etc
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.postgres.fields import DateRangeField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Alignment(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alignment'

    def __str__(self):
        return self.name


class Campaign(models.Model):
    campaign_id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    dates = DateRangeField(blank=True, null=True)
    rating = models.SmallIntegerField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'campaign'

    def __str__(self):
        return self.name


class Pc(models.Model):
    pc_id = models.AutoField(primary_key=True)
    user_id_person = models.ForeignKey('Person', models.DO_NOTHING, db_column='user_id_person', blank=True, null=True)
    campaign_id_campaign = models.ForeignKey('Campaign', models.DO_NOTHING, db_column='campaign_id_campaign', blank=True,
                                             null=True)
    name = models.TextField(blank=True, null=True)
    class_level = models.SmallIntegerField(blank=True, null=True)
    id_pc_class = models.ForeignKey('PcClass', models.DO_NOTHING, db_column='id_pc_class')
    id_alignment = models.ForeignKey(Alignment, models.DO_NOTHING, db_column='id_alignment', to_field='id')
    id_race = models.ForeignKey('Race', models.DO_NOTHING, db_column='id_race')
    strength = models.SmallIntegerField(blank=True, null=True)
    dexterity = models.SmallIntegerField(blank=True, null=True)
    constitution = models.SmallIntegerField(blank=True, null=True)
    intelligence = models.SmallIntegerField(blank=True, null=True)
    wisdom = models.SmallIntegerField(blank=True, null=True)
    charisma = models.SmallIntegerField(blank=True, null=True)
    armor_class = models.SmallIntegerField(blank=True, null=True)
    initiative = models.SmallIntegerField(blank=True, null=True)
    hp = models.SmallIntegerField(blank=True, null=True)
    xp = models.SmallIntegerField(blank=True, null=True)
    equipment = models.TextField(blank=True, null=True)
    spells = models.TextField(blank=True, null=True)
    treasure = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'pc'

    def __str__(self):
        return f'{self.name} ({self.id_pc_class.name}, Lvl: {self.class_level})'

    def get_absolute_url(self):
        return reverse('character-detail', args=[str(self.pc_id)])

    def get_edit_url(self):
        return reverse('character-edit', args=[str(self.pc_id)])


class PcClass(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pc_class'

    def __str__(self):
        return self.name

# We want our persons (players) to be able to log in as users, update their
# profiles etc. For our authentication needs we are going with the Profile/One-to-One
# model, which allows us to store extra information about User but we don't
# need to go as far as using an entirely custom User model.
# It's best to decide on this before the database tables are created since it
# affects table relationships
class Person(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    # We only need these extra fields defined since User already has email, first_name, etc
    discord_id = models.TextField(blank=True, null=True)
    zoom_id = models.TextField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'person'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


# We use signals to hook update_profile_signal method to the User model
# (specifically after save() occurs. This will create a new Person from
# a new user registration (RegisterForm submitted).
# We do also have to write our register function so that it handles
# saving to the extra Person fields (e.g. birthdate) after the Person is created
# e.g. https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:     # created = True if new record was created
        Person.objects.create(user=instance)
    instance.person.save()

# Many-to-many intermediate table
class PersonCampaign(models.Model):
    # Since Django doesn't handle composite PKs, we add a new PK field
    # We had to drop the existing PK constraint in the db first as well so this new field could be added
    person_campaign_id = models.AutoField(primary_key=True)
    is_dm = models.BooleanField(blank=True, null=True)
    # The auto generated model had this set as a OnetoOne so we changed it to FK
    campaign_id_campaign = models.ForeignKey(Campaign, models.DO_NOTHING, db_column='campaign_id_campaign')
    notes = models.TextField(blank=True, null=True)
    user_id_person = models.ForeignKey(Person, models.DO_NOTHING, db_column='user_id_person')

    class Meta:
        managed = False
        db_table = 'person_campaign'
        unique_together = (('campaign_id_campaign', 'user_id_person'),)


class Race(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'race'

    def __str__(self):
        return self.name


