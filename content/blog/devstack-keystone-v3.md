Title: 在DevStack中使用v3版keystone API
Category: 技巧
Date: 2015-12-18 17:20
Tags: openstack, horizon, keystone
Slug: use-keystone-api-v3-in-devstack-liberty

在Liberty版DevStack中，如果需要在dashboard或命令行中使用RBAC（基于角色的访问控制），需要启用v3版keystone API。

Horizon的openstack dashboard默认仍然使用keystone API v2.0，需要修改horizon/openstack_dashboard/local/local_settings.py以指定API版本。

    :::python
    OPENSTACK_API_VERSIONS = {
    #   "data-processing": 1.1,
        "identity": 3,
    #   "volume": 2,
    }

    OPENSTACK_KEYSTONE_URL="http://(keystone_server_ip):5000/v3"

另外，位于devstack/accrc/下的用户环境设置文件也需要进行修改，如admin/admin文件：

    :::bash
    export OS_AUTH_URL="http://(keystone_server_ip):35357/v3"

    export OS_AUTH_TYPE=v3password
