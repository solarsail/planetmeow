Title: 在使用XenServer的DevStack中部署Neutron
Category: 经验
Date: 2016-01-14 13:18
Tags: devstack, xenserver, neutron
Slug: neutron-devstack-xenserver

### 部署环境

- XenServer 6.5

- DevStack Liberty

- Dom0需要连接2块物理网卡

### 安装Neutron
1. 下载devstack的stable/liberty分支到dom0。

2. 应用补丁[217651](https://review.openstack.org/#/c/217651/)。

3. 在`localrc`或`local.conf`文件的`[[local|localrc]]`中加入以下neutron相关配置（如果使用`local.conf`， 需要应用补丁[260861](https://review.openstack.org/#/c/260861/)）。

        Q_PLUGIN=ml2
        Q_AGENT=openvswitch
        Q_ML2_PLUGIN_TYPE_DRIVERS=vlan # 如果添加其他驱动，需要保证vlan在第一位
        Q_ML2_PLUGIN_MECHANISM_DRIVERS=openvswitch
        Q_ML2_TENANT_NETWORK_TYPE=vlan
        Q_USE_SECGROUP=False
        ENABLE_TENANT_VLANS=True
        ENABLE_TENANT_TUNNELS=False
        OVS_VLAN_RANGES="physnet1:1000:1024"
        ML2_VLAN_RANGES="physnet1:1000:1024"
        ENABLED_SERVICES+=,q-svc,q-agt,q-dhcp,q-l3,q-meta,q-domua,q-metering,-n-net

    注意，即使应用了[260861](https://review.openstack.org/#/c/260861/)补丁，dom0的`local.conf`文件中依然不能使用`enable_service`命令。另外，该补丁仅用于从dom0中使用`local.conf`安装，在虚拟机中执行`stack.sh`是可以使用`local.conf`的。

4. 执行`tools/xen/install_os_domU.sh`。

5. 安装完成后， 通过dashboard建立虚拟机，可以获取到10.0.0.x的内网ip。

### 配置外网

1. 使用路由器组建一个局域网，LAN口ip为172.24.4.1，WAN口连接外网。将XenServer的第二块网卡连接到该路由器上。

2. 在XenCenter中，打开服务器的networking页面，设置OpenStack Public Network的属性，NIC设为连接到172网段的网卡，VLAN设为0。

3. 在同一页面中，点击最下方的“Configure...”按钮，添加IP配置，名称随意，网络选择OpenStack Public Network，ip为172.24.4.253（不是1,2,10或与其他虚拟机的浮动ip冲突即可，建议往后配一些），掩码255.255.255.0，网关172.24.4.1。

4. 在OpenStack domU中，执行

        sudo ifconfig br-ex 172.24.4.10 netmask 255.255.255.0 # 172.24.4.10是eth2的ip
        sudo ifconfig eth2 0.0.0.0 # 取消eth2的ip
        sudo service openvswitch-switch restart # 重启ovs服务

    `br-ex`是负责连接外部网络的网桥，`eth2`是连接到OpenStack Public Network的虚拟网卡，已经被设置为网桥的一个端口。[261164](https://review.openstack.org/#/c/261164/)中涉及到了前两步操作，但是该patch被放弃，说明为“不需要”。可能有更简单的配置方法，或者M版的其他补丁已经处理了该问题，尚不清楚。

5. 在dashboard中为虚拟机分配172.24.4.x的浮动ip。虚拟机和XenServer服务器应可以互相ping通。

6. 在虚拟机中设置dns，可以访问外网。

