class DatabaseRouter:
    """
    A router to control database operations on models in the
    data_provider and dashboard_service applications.
    """

    def db_for_read(self, model, **hints):
        """Point all read operations to the specific database."""
        if model._meta.app_label == "data_provider":
            return "data_provider"
        elif model._meta.app_label == "dashboard_service":
            return "dashboard_service"
        return None

    def db_for_write(self, model, **hints):
        """Point all write operations to the specific database."""
        if model._meta.app_label == "data_provider":
            return "data_provider"
        elif model._meta.app_label == "dashboard_service":
            return "dashboard_service"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations if a model in the data_provider or dashboard_service apps is involved."""
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

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that models get created on the right database."""
        if app_label == "data_provider":
            return db == "data_provider"
        elif app_label == "dashboard_service":
            return db == "dashboard_service"
        return None
