class InitService:

    @staticmethod
    def init_permission():
        from user.models import Permission

        # 全部的權限
        permission_list = Permission.admin_permission_list + \
                          Permission.rider_permission_list
        # 已經在DB的權限
        db_name_list = [it['name'] for it in Permission.objects.all().values('name')]

        # 未儲存的權限(通常是新的)
        unsaved_name_list = list(set(permission_list).difference(set(db_name_list)))

        new_permission_list = []
        for name in unsaved_name_list:
            p = Permission()
            p.name = name
            new_permission_list.append(p)

        if len(new_permission_list) == 0:
            print('No permission created')
        else:
            Permission.objects.bulk_create(new_permission_list)
            print(f'Create permission : {unsaved_name_list}')

    @staticmethod
    def init_role():
        from user.models import Role
        from user.models import Permission

        # 新增admin角色
        admin_role = Role.objects.filter(name=Role.ADMIN).first()
        admin_permission_qs = Permission.objects.filter(name__in=Permission.admin_permission_list)
        if admin_role:
            for perm in admin_permission_qs:
                try:
                    admin_role.permissions.add(perm)
                    print(f'Add permission "{perm.name}"')
                except Exception as e:
                    print(f'error:{str(e)}')
            print(f'Update role "{Role.ADMIN}"')
        else:
            admin_role = Role.objects.create(name=Role.ADMIN,
                                             main_name=Role.ADMIN)
            admin_role.permissions.add(*list(admin_permission_qs))
            print(f'Create role "{Role.ADMIN}"')

        # 新增rider角色
        rider_role = Role.objects.filter(name=Role.USER).first()
        rider_permission_qs = Permission.objects.filter(name__in=Permission.rider_permission_list)
        if rider_role:
            for perm in rider_permission_qs:
                try:
                    rider_role.permissions.add(perm)
                    print(f'Add permission "{perm.name}"')
                except Exception as e:
                    print(f'error:{str(e)}')
            print(f'Update role "{Role.USER}"')
        else:
            rider_role = Role.objects.create(name=Role.USER,
                                             main_name=Role.USER)
            rider_role.permissions.add(*list(rider_permission_qs))
            print(f'Create role "{Role.USER}"')
