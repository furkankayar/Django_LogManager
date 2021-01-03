class CheckerRouter:

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'log_manager_db':
            return 'log_manager_db'
        else:
            return 'default'
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'log_manager_db':
            return 'log_manager_db'
        else:
            return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label != 'log_manager_db' and obj2._meta.app_label != 'log_manager_db':
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'default':
            return db == 'default'
        elif app_label == 'log_manager_db':
            return db == 'log_manager_db'
        return None