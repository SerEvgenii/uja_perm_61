# from src.auth_user.adapters.orm import User
# from django.db.models import Model
#
# p = ['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__',
# '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__',
# '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
# '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__',
# '_check_column_name_clashes', '_check_constraints', '_check_default_pk', '_check_field_name_clashes',
# '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields',
# '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model',
# '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes',
# '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update',
# '_get_FIELD_display', '_get_expr_references', '_get_field_value_map', '_get_next_or_previous_by_FIELD',
# '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_perform_date_checks',
# '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents', '_save_table', '_set_pk_val',
# 'check', 'clean', 'clean_fields', 'date_error_message', 'delete', 'from_db', 'full_clean', 'get_constraints',
# 'get_deferred_fields', 'id', 'objects', 'pk', 'prepare_database_save', 'refresh_from_db', 'save', 'save_base',
# 'serializable_value', 'unique_error_message', 'validate_constraints', 'validate_unique']
#
# list_models = [User]
# for model_cls in list_models:
#
# globals()[f'class.{model_cls.__name__}'] = type(f'{model_cls.__name__}', (Model,), {key: model_cls.key for key in
# dir(model_cls) if key not in p})


# from django.db import models
# from django.db.models import Model
#
#
# class User(Model):
#     class Meta:
#         db_table = 'user'
#
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     patronymic = models.CharField(max_length=255)
#     email = models.EmailField(max_length=255, unique=True)
#     login = models.CharField(max_length=255, unique=True)
#     is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
