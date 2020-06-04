# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Alignment(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alignment'


class Campaign(models.Model):
    campaign_id = models.IntegerField(primary_key=True)
    pc_id_pc = models.ForeignKey('Pc', models.DO_NOTHING, db_column='pc_id_pc', blank=True, null=True)
    dm_id_dm = models.ForeignKey('Dm', models.DO_NOTHING, db_column='dm_id_dm', blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    dates = models.TextField(blank=True, null=True)  # This field type is a guess.
    rating = models.SmallIntegerField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'campaign'


class Dm(models.Model):
    dm_id = models.IntegerField(primary_key=True)
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    discord_id = models.TextField(blank=True, null=True)
    zoom_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dm'


class Pc(models.Model):
    pc_id = models.IntegerField(primary_key=True)
    player_id_player = models.ForeignKey('Player', models.DO_NOTHING, db_column='player_id_player', blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    class_level = models.SmallIntegerField(blank=True, null=True)
    id_pc_class = models.ForeignKey('PcClass', models.DO_NOTHING, db_column='id_pc_class')
    id_alignment = models.ForeignKey(Alignment, models.DO_NOTHING, db_column='id_alignment')
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
        managed = False
        db_table = 'pc'


class PcClass(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pc_class'


class Player(models.Model):
    player_id = models.IntegerField(primary_key=True)
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    discord_id = models.TextField(blank=True, null=True)
    zoom_id = models.TextField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'player'


class Race(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'race'

