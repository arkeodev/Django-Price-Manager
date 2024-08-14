"""
Database router module for directing database operations to specific databases.

This module defines a custom database router to control database operations on models 
in the `data_provider` and `dashboard_service` applications.
"""

from typing import Optional, Type

from django.db.models import Model


class DatabaseRouter:
    """
    A router to control database operations on models in the
    data_provider and dashboard_service applications.
    """

    def db_for_read(self, model: Type[Model], **hints: dict) -> Optional[str]:
        """
        Direct read operations to the appropriate database.

        Args:
            model (Type[Model]): The model class for the database operation.
            **hints (dict): Additional hints provided for the database operation.

        Returns:
            Optional[str]: The name of the database to use for read operations.
        """
        if model._meta.app_label == "data_provider":
            return "data_provider"
        elif model._meta.app_label == "dashboard_service":
            return "dashboard_service"
        return None

    def db_for_write(self, model: Type[Model], **hints: dict) -> Optional[str]:
        """
        Direct write operations to the appropriate database.

        Args:
            model (Type[Model]): The model class for the database operation.
            **hints (dict): Additional hints provided for the database operation.

        Returns:
            Optional[str]: The name of the database to use for write operations.
        """
        if model._meta.app_label == "data_provider":
            return "data_provider"
        elif model._meta.app_label == "dashboard_service":
            return "dashboard_service"
        return None

    def allow_relation(self, obj1: Model, obj2: Model, **hints: dict) -> Optional[bool]:
        """
        Allow relations between models if they are in the same application.

        Args:
            obj1 (Model): The first model instance.
            obj2 (Model): The second model instance.
            **hints (dict): Additional hints provided for the database operation.

        Returns:
            Optional[bool]: True if the relation should be allowed, None otherwise.
        """
        if (
            obj1._meta.app_label == "data_provider"
            or obj2._meta.app_label == "data_provider"
        ):
            return True
        if (
            obj1._meta.app_label == "dashboard_service"
            or obj2._meta.app_label == "dashboard_service"
        ):
            return True
        return None

    def allow_migrate(
        self, db: str, app_label: str, model_name: Optional[str] = None, **hints: dict
    ) -> Optional[bool]:
        """
        Ensure that models get created on the right database.

        Args:
            db (str): The name of the database.
            app_label (str): The label of the application.
            model_name (Optional[str]): The name of the model (default is None).
            **hints (dict): Additional hints provided for the database operation.

        Returns:
            Optional[bool]: True if the migration should be allowed, None otherwise.
        """
        if app_label == "data_provider":
            return db == "data_provider"
        elif app_label == "dashboard_service":
            return db == "dashboard_service"
        return None
